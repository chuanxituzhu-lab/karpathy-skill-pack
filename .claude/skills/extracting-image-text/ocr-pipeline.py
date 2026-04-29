#!/usr/bin/env python3
"""
Intelligent OCR pipeline: classify → route → extract → structured output.

Usage:
    python ocr-pipeline.py --image <path> [--type auto|receipt|screenshot|document|idcard|general]
                           [--output json|text] [--save-to <path>]

Dependencies (any subset works — script falls through gracefully):
    pip install easyocr                   # General-purpose (recommended baseline)
    pip install paddlepaddle paddleocr    # CJK + structured docs (recommended for receipts/forms)
    pip install pytesseract Pillow         # Lightweight fallback
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path


# ── Stage 1: Filename classifier ──────────────────────────────────────────────

FILENAME_KEYWORDS = {
    "receipt": ["receipt", "invoice", "bill", "payment", "收据", "发票", "账单"],
    "screenshot": ["screenshot", "screen", "snap", "截图", "capture"],
    "idcard": ["id_card", "idcard", "identity", "身份证", "passport", "驾照", "护照"],
    "document": ["scan", "document", "doc", "form", "letter", "扫描", "文件", "表格"],
}

# Keywords specific enough to score 0.8 vs the default 0.7
HIGH_SPECIFICITY: dict[str, list[str]] = {
    "receipt": ["receipt", "invoice", "收据", "发票"],
    "screenshot": ["screenshot", "截图"],
    "idcard": ["id_card", "身份证", "passport", "驾照", "护照"],
}

# Stage 1b: Dimension heuristics (Pillow)
#   A4         → ~1.414 (document)
#   Letter     → ~1.294 (document)
#   Receipt    → aspect_ratio > 2.0 or < 0.5 (long strip)
#   ID card    → ~1.586 (CR80 standard, small image)
#   Monitor    → 16:9(1.78), 16:10(1.6), with high resolution (screenshot)
DIMENSION_RULES = {
    "document":    lambda w, h, ar: 0.35 if 1.25 < ar < 1.6 and w > 800 else 0,
    "receipt":     lambda w, h, ar: 0.40 if ar > 2.0 or (h > w and ar < 0.5) else 0,
    "idcard":      lambda w, h, ar: 0.40 if 1.5 < ar < 1.7 and max(w, h) < 600 else 0,
    "screenshot":  lambda w, h, ar: 0.35 if 1.5 < ar < 2.0 and w >= 1000 else 0,
}

# Stage 2: Content keywords (EasyOCR quick pass)
CONTENT_KEYWORDS = {
    "receipt":     ["total", "subtotal", "tax", "amount due", "合计", "总计", "消费", "金额"],
    "idcard":      ["姓名", "name", "身份证号", "id number", "出生", "住址", "address", "性别"],
    "document":    ["摘要", "subject", "致", "to:", "from:", "日期", "date:"],
    "screenshot":  [],  # no specific keywords; detected by lack of other signals
}


# ── Image classification ──────────────────────────────────────────────────────

def classify_image(image_path: str, force_type: str | None = None) -> tuple[str, float]:
    """Two-stage classifier. Returns (type, confidence)."""
    if force_type and force_type != "auto":
        return force_type, 1.0

    scores: dict[str, float] = {"receipt": 0, "screenshot": 0, "document": 0, "idcard": 0, "general": 0.1}

    # Stage 1a: Filename patterns
    fname = Path(image_path).stem.lower()
    for img_type, keywords in FILENAME_KEYWORDS.items():
        for kw in keywords:
            if kw in fname:
                score = 0.8 if img_type in HIGH_SPECIFICITY and kw in HIGH_SPECIFICITY[img_type] else 0.7
                scores[img_type] = max(scores[img_type], score)

    # Stage 1b: Dimension heuristics
    try:
        from PIL import Image
        img = Image.open(image_path)
        w, h = img.size
        ar = w / h if h > 0 else 1
        for img_type, rule in DIMENSION_RULES.items():
            s = rule(w, h, ar)
            if s > scores[img_type]:
                scores[img_type] = s
    except Exception:
        pass

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    # Stage 2: Content sampling (only if Stage 1 confidence is weak)
    if best_score < 0.6:
        try:
            import easyocr
            reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
            results = reader.readtext(image_path)
            text = " ".join(r[1] for r in results).lower()
            line_count = len(results)
            avg_conf = sum(r[2] for r in results) / max(line_count, 1)

            for img_type, keywords in CONTENT_KEYWORDS.items():
                for kw in keywords:
                    if kw in text:
                        scores[img_type] = max(scores[img_type], 0.85)

            # Density heuristic: dense high-conf text → document; sparse high-conf → screenshot
            if avg_conf > 0.7:
                if line_count > 20:
                    scores["document"] = max(scores["document"], 0.75)
                elif line_count < 10:
                    scores["screenshot"] = max(scores["screenshot"], 0.75)

            # Re-evaluate best
            best_type = max(scores, key=scores.get)
            best_score = scores[best_type]
        except ImportError:
            pass  # easyocr not installed, skip content sampling
        except Exception:
            pass

    if best_score < 0.3:
        return "general", 0.3
    return best_type, min(best_score, 0.99)


# ── OCR pipelines ─────────────────────────────────────────────────────────────

def _run_easyocr(image_path: str) -> list[dict] | None:
    try:
        import easyocr
        reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
        results = reader.readtext(image_path)
        return [
            {"text": r[1], "confidence": round(r[2], 4), "bbox": r[0]}
            for r in results
        ]
    except ImportError:
        return None


def _run_paddleocr(image_path: str) -> list[dict] | None:
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        results = ocr.ocr(image_path)
        if not results or not results[0]:
            return None
        return [
            {"text": line[1][0], "confidence": round(line[1][1], 4), "bbox": line[0]}
            for line in results[0]
        ]
    except ImportError:
        return None


def _run_ppstructure(image_path: str) -> dict | None:
    """PaddleOCR PP-Structure for layout + table extraction."""
    try:
        from paddleocr import PPStructure
        engine = PPStructure(show_log=False)
        result = engine(image_path)
        texts = []
        tables = []
        for item in result:
            if item["type"] == "text":
                texts.append(item["res"]["text"])
            elif item["type"] == "table":
                tables.append(item["res"]["html"])
        return {"texts": texts, "tables": tables}
    except ImportError:
        return None


def _run_tesseract(image_path: str) -> list[dict] | None:
    try:
        import pytesseract
        from PIL import Image
        data = pytesseract.image_to_data(Image.open(image_path), output_type=pytesseract.Output.DICT)
        results = []
        for i in range(len(data["text"])):
            text = data["text"][i].strip()
            if text:
                results.append({
                    "text": text,
                    "confidence": int(data["conf"][i]) / 100.0 if data["conf"][i] != "-1" else 0,
                    "bbox": [data["left"][i], data["top"][i],
                             data["left"][i] + data["width"][i], data["top"][i] + data["height"][i]],
                })
        return results if results else None
    except ImportError:
        return None


# ── Pipeline router ───────────────────────────────────────────────────────────

def _text_from_items(items: list[dict] | None) -> str:
    if not items:
        return ""
    return "\n".join(item["text"] for item in items)


def pipeline_receipt(image_path: str) -> dict:
    """Receipt pipeline: PP-Structure → PaddleOCR → EasyOCR → Tesseract."""
    result = _run_ppstructure(image_path)
    if result and result["texts"]:
        raw_text = "\n".join(result["texts"])
        return {
            "pipeline_used": "paddleocr_ppstructure",
            "raw_text": raw_text,
            "tables": result.get("tables", []),
            "extracted_data": _parse_receipt(raw_text),
            "ocr_confidence": 0.85,
        }
    items = _run_easyocr(image_path) or _run_tesseract(image_path)
    raw_text = _text_from_items(items)
    return {
        "pipeline_used": "easyocr" if items else "none",
        "raw_text": raw_text,
        "tables": [],
        "extracted_data": _parse_receipt(raw_text),
        "ocr_confidence": round(sum(i["confidence"] for i in items) / max(len(items), 1), 4) if items else 0,
    }


def pipeline_idcard(image_path: str) -> dict:
    """ID card pipeline: PaddleOCR → EasyOCR → Tesseract."""
    items = _run_paddleocr(image_path) or _run_easyocr(image_path) or _run_tesseract(image_path)
    raw_text = _text_from_items(items)
    return {
        "pipeline_used": "paddleocr" if items else "none",
        "raw_text": raw_text,
        "tables": [],
        "extracted_data": _parse_idcard(raw_text),
        "ocr_confidence": round(sum(i["confidence"] for i in items) / max(len(items), 1), 4) if items else 0,
    }


def pipeline_document(image_path: str) -> dict:
    """Document pipeline: PP-Structure → PaddleOCR → EasyOCR → Tesseract."""
    result = _run_ppstructure(image_path)
    if result and result["texts"]:
        return {
            "pipeline_used": "paddleocr_ppstructure",
            "raw_text": "\n".join(result["texts"]),
            "tables": result.get("tables", []),
            "extracted_data": {},
            "ocr_confidence": 0.85,
        }
    items = _run_paddleocr(image_path) or _run_easyocr(image_path) or _run_tesseract(image_path)
    return {
        "pipeline_used": "paddleocr" if items else "none",
        "raw_text": _text_from_items(items),
        "tables": [],
        "extracted_data": {},
        "ocr_confidence": round(sum(i["confidence"] for i in items) / max(len(items), 1), 4) if items else 0,
    }


def pipeline_screenshot(image_path: str) -> dict:
    """Screenshot pipeline: EasyOCR → Tesseract → PaddleOCR."""
    items = _run_easyocr(image_path)
    if not items:
        items = _run_tesseract(image_path)
    if not items:
        items = _run_paddleocr(image_path)
    return {
        "pipeline_used": "easyocr" if items else "none",
        "raw_text": _text_from_items(items),
        "tables": [],
        "extracted_data": {},
        "ocr_confidence": round(sum(i["confidence"] for i in items) / max(len(items), 1), 4) if items else 0,
    }


def pipeline_general(image_path: str) -> dict:
    """General fallback: EasyOCR → Tesseract → PaddleOCR."""
    items = _run_easyocr(image_path)
    if not items:
        items = _run_tesseract(image_path)
    if not items:
        items = _run_paddleocr(image_path)
    return {
        "pipeline_used": "easyocr" if items else "none",
        "raw_text": _text_from_items(items),
        "tables": [],
        "extracted_data": {},
        "ocr_confidence": round(sum(i["confidence"] for i in items) / max(len(items), 1), 4) if items else 0,
    }


PIPELINES = {
    "receipt":    pipeline_receipt,
    "idcard":     pipeline_idcard,
    "document":   pipeline_document,
    "screenshot": pipeline_screenshot,
    "general":    pipeline_general,
}


# ── Structured parsers ────────────────────────────────────────────────────────

def _parse_receipt(text: str) -> dict:
    """Extract vendor, date, total, tax, line_items from receipt text."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    data = {"vendor": "", "date": "", "total": 0.0, "tax": 0.0, "line_items": []}

    # Date: common formats
    date_pat = re.search(r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b", text)
    if date_pat:
        data["date"] = date_pat.group(1)

    # Total: "total xxx.xx" or "合计 xxx.xx"
    total_pat = re.search(
        r"(?:total|amount due|合计|总计|总额)[:\s]*[$¥￥]?\s*(\d+[.,]\d{2})",
        text, re.IGNORECASE
    )
    if total_pat:
        data["total"] = float(total_pat.group(1).replace(",", ""))

    # Vendor: first non-empty line that looks like a vendor name (all caps or known name)
    for line in lines[:5]:
        cleaned = re.sub(r"[\s#*\-_]", "", line)
        if cleaned and len(cleaned) > 2:
            data["vendor"] = line
            break

    # Tax / VAT
    tax_pat = re.search(
        r"(?:tax|vat|gst|税)[:\s]*[$¥￥]?\s*(\d+[.,]\d{2})",
        text, re.IGNORECASE
    )
    if tax_pat:
        data["tax"] = float(tax_pat.group(1).replace(",", ""))

    # Line items: find price-pattern lines
    for line in lines:
        price_match = re.search(r"[$¥￥]?\s*(\d+[.,]\d{2})\s*$", line)
        if price_match and line not in [total_pat.group(0) if total_pat else ""]:
            data["line_items"].append({
                "description": price_match.string[:price_match.start()].strip(),
                "price": float(price_match.group(1).replace(",", "")),
            })

    return data


def _parse_idcard(text: str) -> dict:
    """Extract name, id_number, address, dob from ID card text."""
    data = {"name": "", "id_number": "", "address": "", "dob": ""}

    # Chinese name
    name_pat = re.search(r"姓名\s*[：:]?\s*(\S{2,4})", text)
    if name_pat:
        data["name"] = name_pat.group(1)
    else:
        eng_pat = re.search(r"(?:name|NAME)[：:\s]*([A-Za-z\s]+)", text)
        if eng_pat:
            data["name"] = eng_pat.group(1).strip()

    # Chinese ID number (18 digits)
    id_pat = re.search(r"\b(\d{17}[\dXx])\b", text)
    if id_pat:
        data["id_number"] = id_pat.group(1).upper()

    # Address
    addr_pat = re.search(r"(?:住址|address|ADDRESS)[：:\s]*(.+)", text)
    if addr_pat:
        data["address"] = addr_pat.group(1).strip()

    # Date of birth
    dob_pat = re.search(r"(?:出生|birth|DOB)[：:\s]*(\S+)", text)
    if dob_pat:
        data["dob"] = dob_pat.group(1).strip()

    return data


# ── CLI ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Intelligent OCR pipeline — classify image type and extract text/structured data.",
    )
    p.add_argument("--image", "-i", required=True, help="Path to image file")
    p.add_argument("--type", "-t", default="auto",
                    choices=["auto", "receipt", "screenshot", "document", "idcard", "general"],
                    help="Image type (auto=classify, otherwise force type)")
    p.add_argument("--output", "-o", default="json", choices=["json", "text"],
                    help="Output format")
    p.add_argument("--save-to", "-s", help="Save JSON output to file")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not os.path.isfile(args.image):
        print(json.dumps({"error": f"File not found: {args.image}"}))
        sys.exit(1)

    start = time.time()

    # Classify
    image_type, classification_conf = classify_image(args.image, args.type)

    # Run pipeline
    pipeline = PIPELINES.get(image_type, pipeline_general)
    result = pipeline(args.image)

    # Assemble output
    output = {
        "image_path": os.path.abspath(args.image),
        "image_type": image_type,
        "classification_confidence": round(classification_conf, 4),
        "pipeline_used": result.get("pipeline_used", "none"),
        "raw_text": result.get("raw_text", ""),
        "tables": result.get("tables", []),
        "extracted_data": result.get("extracted_data", {}),
        "ocr_confidence": result.get("ocr_confidence", 0),
        "processing_time_ms": int((time.time() - start) * 1000),
    }

    if args.output == "text":
        print(output["raw_text"] or "[No text extracted]")
    else:
        text = json.dumps(output, ensure_ascii=False, indent=2)
        print(text)
        if args.save_to:
            Path(args.save_to).write_text(text, encoding="utf-8")

    sys.exit(0 if output["raw_text"] else 1)


if __name__ == "__main__":
    main()
