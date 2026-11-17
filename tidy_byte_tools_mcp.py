"""One MCP server that exposes the Tidy Byte Tools lite tools over stdio.

Run:  uvx --from git+https://github.com/tidybytetools/tidy-byte-tools tidy-byte-tools mcp
  or: uvx --from git+https://github.com/tidybytetools/tidy-byte-tools tidy-byte-tools-mcp
"""

from __future__ import annotations

import base64_lite_mcp
import doc2md_lite_mcp
import hash_lite_mcp
import json_repair_lite_mcp
import json_shaper_lite_mcp
import link_check_lite_mcp
import md_chunk_lite_mcp
import pdf_table_pull_lite_mcp
from mcp.server.fastmcp import FastMCP

# Names that would collide or be unclear next to the other tools.
RENAME = {
    "convert_text": "base64_convert_text",
    "convert_file": "base64_convert_file",
}

# Explicit list so a new lite tool is not added by surprise. Metadata
# (title, description, annotations) is reused from each lite MCP server.
EXPOSE: tuple[tuple[object, str], ...] = (
    (json_repair_lite_mcp, "repair_json_text"),
    (json_repair_lite_mcp, "repair_json_file"),
    (json_shaper_lite_mcp, "shape_text_to_json"),
    (json_shaper_lite_mcp, "shape_file_to_json"),
    (base64_lite_mcp, "convert_text"),
    (base64_lite_mcp, "convert_file"),
    (hash_lite_mcp, "hash_text"),
    (hash_lite_mcp, "hash_file"),
    (md_chunk_lite_mcp, "chunk_markdown"),
    (md_chunk_lite_mcp, "outline_markdown"),
    (md_chunk_lite_mcp, "get_section"),
    (md_chunk_lite_mcp, "save_chunks_jsonl"),
    (doc2md_lite_mcp, "convert_to_markdown"),
    (pdf_table_pull_lite_mcp, "extract_pdf_tables"),
    (link_check_lite_mcp, "check_links"),
)

INSTRUCTIONS = (
    "Local tools from Tidy Byte Tools. They clean messy data on this computer: "
    "repair JSON, turn notes or tables into JSON, encode or decode Base64, "
    "hash text and files, split Markdown into chunks, convert PDFs and HTML "
    "to Markdown, pull tables out of a PDF, and check web links. "
    "Most tools only read. save_chunks_jsonl, convert_to_markdown (when you "
    "set output_path), and extract_pdf_tables can write the files you ask for. "
    "check_links makes HTTP requests to the URLs you give it. No API key."
)

mcp = FastMCP(
    "tidy-byte-tools",
    instructions=INSTRUCTIONS,
    website_url="https://github.com/tidybytetools/tidy-byte-tools",
)


def _load_tools() -> None:
    for mod, src_name in EXPOSE:
        tool = mod.mcp._tool_manager.get_tool(src_name)
        if tool is None:
            raise RuntimeError(f"lite MCP tool missing: {mod.__name__}.{src_name}")
        mcp.add_tool(
            tool.fn,
            name=RENAME.get(src_name, src_name),
            title=tool.title,
            description=tool.description,
            annotations=tool.annotations,
        )


_load_tools()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
