---
name: extracting-image-text
description: Free open-source OCR (Optical Character Recognition) using EasyOCR, PaddleOCR, and Tesseract. Covers image text extraction, multi-language OCR, structured document parsing, table extraction, and scanned PDF workflows. Apache 2.0 licensed tools.
version: 2.0.0
---

# Extracting Image Text (OCR)

## Purpose

Extract text from images, screenshots, scanned documents, and PDFs using free open-source OCR engines. The system auto-classifies image types and routes to the optimal processing pipeline for structured extraction.

---

## Pipeline System (v2.0)

The `ocr-pipeline.py` script combines image classification + OCR routing + structured extraction into one command.

### Setup

```bash
# Core (any subset works — script falls through gracefully)
pip install easyocr                               # General-purpose (recommended baseline)
pip install paddlepaddle paddleocr                 # CJK + structured docs
pip install pytesseract Pillow                     # Lightweight fallback
```

### Quick Start

```bash
# Auto-classify and extract
python .claude/skills/extracting-image-text/ocr-pipeline.py --image receipt.jpg

# Force type (skip classification)
python ocr-pipeline.py --image screenshot.png --type screenshot

# Plain text output only
python ocr-pipeline.py --image doc.jpg --output text

# Save result as JSON sidecar
python ocr-pipeline.py --image invoice.jpg --save-to invoice.json
```

### Per-Type Examples

| Image Type | Command | What Happens |
|---|---|---|
| receipt | `ocr-pipeline.py --image receipt.jpg` | Classifies → PP-Structure → vendor/date/total/items |
| screenshot | `ocr-pipeline.py --image screen.png` | Classifies → EasyOCR → clean text |
| document | `ocr-pipeline.py --image scan.pdf` | Classifies → PP-Structure → text + tables |
| idcard | `ocr-pipeline.py --image id.jpg` | Classifies → PaddleOCR → name/id/address |
| general | `ocr-pipeline.py --image photo.jpg` | Fallback → EasyOCR → raw text |

### Output Format

```json
{
  "image_path": "C:/path/to/receipt.jpg",
  "image_type": "receipt",
  "classification_confidence": 0.85,
  "pipeline_used": "paddleocr_ppstructure",
  "raw_text": "STORE NAME\n2024-01-15\nItem A  $10.00\nTotal  $10.00",
  "tables": ["<table>...</table>"],
  "extracted_data": {
    "vendor": "STORE NAME",
    "date": "2024-01-15",
    "total": 10.0,
    "tax": 0.0,
    "line_items": [{"description": "Item A", "price": 10.0}]
  },
  "ocr_confidence": 0.92,
  "processing_time_ms": 1450
}
```

### Classification Logic

The two-stage classifier works without ML:

1. **Stage 1 (zero-cost):** Filename keywords (`receipt`, `发票`, `screenshot`, `id_card`) + Pillow dimension heuristics (A4 ratio→document, wide→receipt, small CR80→ID card)
2. **Stage 2 (optional):** If Stage 1 confidence < 0.6, a quick EasyOCR pass scans for domain keywords (`total`, `姓名`, `amount due`) and measures text density
3. **Fallback:** `general` type with EasyOCR when no strong signal found

Use `--type` to override classification when the auto-detection doesn't match.

---

## Cowork Mode Automation

When `current-mode.txt` contains "cowork", the pipeline integrates with auto-orchestrator for automatic processing.

### Image Detection → Auto-Pipeline

When Claude detects new/modified `.png`/`.jpg`/`.jpeg`/`.tiff`/`.bmp` files (e.g., user drags a receipt screenshot into the project):

1. `skill-rules.json` triggers the `extracting-image-text` skill suggestion
2. In Cowork mode, Claude auto-executes:
   ```bash
   python .claude/skills/extracting-image-text/ocr-pipeline.py --image <file>
   ```
3. **If confidence ≥ 0.5:** Present structured results to the user (formatted summary for receipts/invoices, clean text for screenshots)
4. **If confidence < 0.5:** Flag for review, suggest `--type` override
5. **If sidecar JSON exists** (`receipt-01.json` alongside `receipt-01.jpg`): Offer to update or diff

### Multi-Image Batch

When multiple images appear in one change set:

```bash
# Run on each image
for img in *.jpg; do
  python .claude/skills/extracting-image-text/ocr-pipeline.py --image "$img" --save-to "${img%.*}.json"
done
```

Claude collects all outputs and presents a summary table:

| Image | Type | Confidence | Key Fields |
|---|---|---|---|
| receipt-01.jpg | receipt | 0.92 | Vendor: "Store", Total: $45.00 |
| screen-01.png | screenshot | 0.88 | (280 chars extracted) |

### Auto-Orchestrator Integration

The auto-orchestrator already maps `.png`/`.jpg`/`.jpeg`/`.tiff`/`.bmp` → `extracting-image-text`. When it detects such changes:

- Suggests running the pipeline as an action item
- On `/auto-scan full`, includes OCR results in the comprehensive report
- Logs pipeline events to `.claude/evolution/log.jsonl` for self-evolution analysis

---

## Type-Specific Extraction Templates

### Receipt / Invoice

Fields extracted: `vendor`, `date`, `total`, `tax`, `line_items`

```python
# Manual extraction if pipeline doesn't match
import re, json
from PIL import Image
import pytesseract

text = pytesseract.image_to_string(Image.open("receipt.jpg"))
# Date: ISO format
date = re.search(r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b", text)
# Total: label followed by price
total = re.search(r"(?:total|合计|金额)[:\s]*[$¥]?(\d+[.,]\d{2})", text, re.I)
print(json.dumps({"date": date.group(1) if date else "", "total": total.group(1) if total else ""}))
```

### ID Card

Fields extracted: `name`, `id_number`, `address`, `dob`

```python
text = pytesseract.image_to_string(Image.open("id.jpg"))
# Chinese ID number (18 digits)
id_no = re.search(r"\b(\d{17}[\dXx])\b", text)
# Chinese name after "姓名"
name = re.search(r"姓名[：:]?\s*(\S{2,4})", text)
```

### Document with Tables (PaddleOCR PP-Structure)

```python
from paddleocr import PPStructure
engine = PPStructure(show_log=False)
result = engine("document.jpg")
for item in result:
    if item["type"] == "table":
        print(item["res"]["html"])  # HTML table
    elif item["type"] == "text":
        print(item["res"]["text"])
```

---

## License Status

All recommended tools are **Apache 2.0** — free for commercial and personal use:

| Tool | License | Best For |
|------|---------|----------|
| **EasyOCR** | Apache 2.0 | Quick setup, general-purpose, scene text |
| **PaddleOCR** | Apache 2.0 | CJK text, structured docs, table extraction |
| **Tesseract** | Apache 2.0 | Mature engine, CPU-friendly, 100+ languages |

## Prerequisites

```bash
# EasyOCR (recommended for most tasks — single pip install)
pip install easyocr

# PaddleOCR (better for CJK and structured documents)
pip install paddlepaddle paddleocr

# Tesseract (lightweight fallback)
# Windows: download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: apt install tesseract-ocr
pip install pytesseract Pillow
```

## Tool Selection Guide

| Scenario | Recommended Tool | Why |
|----------|-----------------|-----|
| Quick text from screenshot | EasyOCR | Single pip install, works out of box |
| Chinese/Japanese/Korean text | PaddleOCR | Best CJK accuracy among open-source |
| Structured document (invoice/form) | PaddleOCR PP-Structure | Built-in layout + table analysis |
| Scene text (photos, street signs) | EasyOCR | Trained on scene text data |
| Clean printed document | Tesseract + pytesseract | Fastest, CPU-only, 100+ languages |
| Scanned PDF batch | OCRmyPDF + any OCR | Adds searchable text layer to PDFs |
| Handwriting | PaddleOCR or TrOCR (HuggingFace) | Specialized handwriting models |

## Reference: Raw OCR Engine Patterns

### Quick Text Extraction (EasyOCR)

```python
import easyocr

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
results = reader.readtext('image.jpg')

text = '\n'.join([r[1] for r in results])
for bbox, word, confidence in results:
    print(f"[{confidence:.2f}] {word} at {bbox}")
```

### Multi-Language OCR

```python
# EasyOCR
reader = easyocr.Reader(['ch_sim', 'en', 'ja', 'ko'])

# PaddleOCR
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
results = ocr.ocr('document.jpg')
```

### Structured Document Extraction (PaddleOCR)

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')
results = ocr.ocr('invoice.jpg')

for line in results[0]:
    bbox, (text, confidence) = line[:2], line[1]
    print(f"{text} (confidence: {confidence:.2f})")
```

### Table Extraction from Images

```python
from paddleocr import PPStructure
engine = PPStructure(show_log=False)
result = engine('table.jpg')
for item in result:
    if item['type'] == 'table':
        html = item['res']['html']
```

### Scanned PDF Workflow

```python
import subprocess
subprocess.run(['ocrmypdf', 'input.pdf', 'output.pdf'])
```

### Image Preprocessing (Improves Accuracy)

```python
from PIL import Image, ImageEnhance, ImageFilter

img = Image.open('dark_image.jpg')
img = img.convert('L')
img = ImageEnhance.Contrast(img).enhance(2.0)
img = img.filter(ImageFilter.SHARPEN)
img.save('enhanced.jpg')
```

## MCP Server Integration (Optional)

For Claude-native OCR without inline Python, install a free MCP OCR server:

```bash
# Option 1: rjn32s/mcp-ocr (Tesseract-based, MIT)
pip install mcp-ocr
claude mcp add ocr-tesseract --scope project -- python -m mcp_ocr

# Option 2: sandraschi/ocr-mcp (multi-backend, MIT, most features)
pip install ocr-mcp
claude mcp add ocr-mcp --scope project -- python -m ocr_mcp

# Option 3: fast-paddleocr-mcp (PaddleOCR-based, Apache 2.0)
pip install fast-paddleocr-mcp
claude mcp add ocr-paddle --scope project -- python -m fast_paddleocr_mcp
```

### Verify MCP Server

```bash
# Check if installed
pip list | grep mcp-ocr

# Test MCP tool directly
# Once added, use MCP tools in Claude: "用 OCR 工具识别这张图片"
```

## Related Skills

- **automating-browser**: Capture browser screenshots then pass to OCR
- **testing-full-pyramid**: E2E tests with visual text verification
