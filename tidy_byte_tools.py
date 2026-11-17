"""One command for all Tidy Byte Tools lite CLIs, plus the combined MCP server."""

from __future__ import annotations

import importlib
import sys

__version__ = "0.1.0"

# subcommand -> (importable module with main(), argv0 so that tool's own help still makes sense)
COMMANDS = {
    "json-repair": ("json_repair_lite", "json-repair-lite"),
    "json-shaper": ("json_shaper_lite", "json-shaper-lite"),
    "base64": ("base64_lite", "base64-lite"),
    "hash": ("hash_lite", "hash-lite"),
    "md-chunk": ("md_chunk_lite", "md-chunk-lite"),
    "doc2md": ("doc2md_lite", "doc2md-lite"),
    "pdf-table-pull": ("pdf_table_pull_lite", "pdf-table-pull-lite"),
    "link-check": ("link_check_lite", "link-check-lite"),
}

HELP = f"""tidy-byte-tools {__version__}

One install for the free Tidy Byte Tools. Each subcommand is the same as
that tool's own command. `mcp` starts one MCP server with all of the tools.

Usage:
  tidy-byte-tools <command> [args]
  tbt <command> [args]

Commands:
  json-repair       Repair broken or incomplete JSON
  json-shaper       Turn notes, CSV/TSV or Markdown tables into JSON
  base64            Encode or decode Base64
  hash              Hash text or files (SHA-256, SHA-1, MD5, SHA-512)
  md-chunk          Split Markdown into chunks by heading
  doc2md            Turn a PDF or HTML file into Markdown
  pdf-table-pull    Pull tables out of a PDF into CSV
  link-check        Check web links for status codes and redirects
  mcp               Start the combined MCP server (stdio)

Examples:
  printf '{{name: "Ada", city: "Austin",}}' | tidy-byte-tools json-repair
  tidy-byte-tools pdf-table-pull report.pdf
  tidy-byte-tools mcp

Installing this package also gives you the original commands
(json-repair-lite, doc2md-lite, and so on).

Paid cloud tools:  https://apify.com/tidybytetools
HTTPS API:         https://tidybytetools.tidybytetools.workers.dev
Source:            https://github.com/tidybytetools/tidy-byte-tools
"""


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(HELP)
        return 0
    if argv[0] in ("-V", "--version"):
        print(__version__)
        return 0
    cmd, *rest = argv
    if cmd == "mcp":
        from tidy_byte_tools_mcp import main as mcp_main

        sys.argv = ["tidy-byte-tools-mcp", *rest]
        try:
            mcp_main()
        except SystemExit as exc:
            return _exit_code(exc.code)
        return 0
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print("Try `tidy-byte-tools --help`.", file=sys.stderr)
        return 2
    module_name, prog = COMMANDS[cmd]
    mod = importlib.import_module(module_name)
    sys.argv = [prog, *rest]
    try:
        result = mod.main()
    except SystemExit as exc:
        return _exit_code(exc.code)
    return 0 if result is None else int(result)


def _exit_code(code: object) -> int:
    if code is None or code is False:
        return 0
    if code is True:
        return 1
    if isinstance(code, int):
        return code
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
