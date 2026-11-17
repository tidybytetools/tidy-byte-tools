# Changelog

What changed in tidy-byte-tools, newest first.

## 0.1.0 - 2026-11-17

- First release.
- One install that pulls in the eight free lite tools: json-repair-lite, json-shaper-lite, base64-lite, hash-lite, md-chunk-lite, doc2md-lite, pdf-table-pull-lite, and link-check-lite.
- `tidy-byte-tools` (also `tbt`) runs each lite as a subcommand. `tidy-byte-tools mcp` starts one MCP server with all 15 tools.
- The three lites that are not on PyPI yet (json-repair-lite, base64-lite, hash-lite) are installed from their GitHub tags. The others come from PyPI.
- Needs Python 3.10 or newer.
