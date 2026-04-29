---
name: automating-browser
description: Chrome DevTools browser automation. Covers CDP integration, web navigation, form interaction, screenshot capture, network debugging, and E2E testing patterns. Integrates with chrome-devtools MCP.
---

# Automating Browser

Chrome DevTools Protocol (CDP) integration for browser automation. Bridges web interaction and programmatic control through the `chrome-devtools-mcp` server.

## Prerequisites

Chrome running with remote debugging enabled:
```bash
# Ensure Chrome is open with debugging port
chrome.exe --remote-debugging-port=9222
```

MCP server (already installed):
```
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

## Automation Patterns

### Navigation & Page Control

| Task | Pattern |
|------|---------|
| Navigate to URL | Open new tab → navigate → wait for load |
| Screenshot capture | Navigate → wait for rendering → screenshot |
| Page inspection | Snapshot accessibility tree or read DOM |
| Form filling | Find element → fill value → verify |
| Click actions | Find element → click at coordinates |

### Web Scraping

1. Navigate to target URL
2. Wait for page/content to fully load
3. Extract text via accessibility tree snapshot
4. Extract structured data via JavaScript evaluation
5. Capture screenshot for visual verification

### Network Debugging

Monitor requests and responses:
- Filter by URL pattern (`/api/`, `.json`)
- Check response status codes
- Inspect request/response payloads
- Track failed requests (4xx/5xx)

### E2E Testing Integration

Integrates with `testing-full-pyramid` as the browser automation layer:
- Playwright/Cypress for structured E2E suites
- CDP for lightweight browser inspection
- Screenshot diffs for visual regression

## Chrome DevTools MCP Tools

| Tool | Purpose | Common Use |
|------|---------|------------|
| `list_tabs` | List open tabs | Find existing page to control |
| `create_tab` | Open new tab | Navigate to URL |
| `close_tab` | Close tab | Cleanup after task |
| `navigate` | Go to URL | Core navigation |
| `take_screenshot` | Capture viewport | Visual verification |
| `page_snapshot` | Get accessibility tree | Read page content |
| `console_logs` | Read console | Debugging |
| `network_requests` | Monitor network | API inspection |
| `eval` | Execute JavaScript | Advanced interaction |

## Automation Workflows

### Simple: Open Page and Screenshot
```
create_tab → navigate(url) → take_screenshot → close_tab
```

### Medium: Form Fill and Submit
```
create_tab → navigate(url) → page_snapshot → find_form → fill_fields → click_submit → wait_for_result → take_screenshot
```

### Complex: Multi-Page Data Collection
```
for each URL in targets:
  create_tab → navigate(url) → wait_for_load → page_snapshot → extract_data → close_tab
compile_data → report
```

## Integration with Skill System

- **testing-full-pyramid**: Browser skill provides the E2E execution layer
- **auto-orchestrator**: Auto-activates on `.html` files and web-related tasks
- **evolving-system**: Logs browser automation events for evolution analysis
