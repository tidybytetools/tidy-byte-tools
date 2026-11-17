# Security

## Supported versions

Only the newest release of tidy-byte-tools gets fixes.

## Report a problem

Please do not open a public issue for a security problem.

Use GitHub's private report form instead:
https://github.com/tidybytetools/tidy-byte-tools/security/advisories/new

Tell us what you found and how to make it happen again. We will reply as soon as we can, and we will credit you if you want.

## What this tool does

tidy-byte-tools runs on your own computer. It does not send your files anywhere except when you use `link-check`, which requests the URLs you give it. Most MCP tools only read. `save_chunks_jsonl`, `convert_to_markdown` (when you set an output path), and `extract_pdf_tables` can write the files you ask for. There are no accounts, no API keys, and no tracking.
