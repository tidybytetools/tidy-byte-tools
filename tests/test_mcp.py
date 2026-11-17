"""Starts the combined MCP server over stdio, lists tools, and calls a few."""

import asyncio
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    ClientSession = None

EXPECTED = [
    "base64_convert_file",
    "base64_convert_text",
    "check_links",
    "chunk_markdown",
    "convert_to_markdown",
    "extract_pdf_tables",
    "get_section",
    "hash_file",
    "hash_text",
    "outline_markdown",
    "repair_json_file",
    "repair_json_text",
    "save_chunks_jsonl",
    "shape_file_to_json",
    "shape_text_to_json",
]


def _data(res):
    """The tool result as Python data (structured content if present, else the JSON text)."""
    if res.structuredContent is not None:
        sc = res.structuredContent
        return sc.get("result", sc) if set(sc) == {"result"} else sc
    return json.loads(res.content[0].text)


async def _session(args, fn):
    params = StdioServerParameters(command=sys.executable, args=args, cwd=ROOT)
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            return await fn(s)


@unittest.skipIf(ClientSession is None, "mcp not installed")
class MCP(unittest.TestCase):
    def test_tools_from_module(self):
        async def go(s):
            return (await s.list_tools()).tools

        tools = asyncio.run(_session([os.path.join(ROOT, "tidy_byte_tools_mcp.py")], go))
        names = sorted(t.name for t in tools)
        self.assertEqual(names, EXPECTED)
        for t in tools:
            self.assertTrue(t.title, t.name)
            self.assertTrue(t.description, t.name)

    def test_cli_mcp_subcommand_starts_server(self):
        async def go(s):
            return sorted(t.name for t in (await s.list_tools()).tools)

        names = asyncio.run(_session([os.path.join(ROOT, "tidy_byte_tools.py"), "mcp"], go))
        self.assertEqual(names, EXPECTED)

    def test_calls(self):
        async def go(s):
            repaired = await s.call_tool(
                "repair_json_text", {"text": '{name: "Ada", city: "Austin",}'}
            )
            valid = await s.call_tool("repair_json_text", {"text": '{"a": 1}'})
            from_file = await s.call_tool(
                "repair_json_file",
                {"path": os.path.join(HERE, "fixtures", "broken.json")},
            )
            shaped = await s.call_tool(
                "shape_text_to_json", {"text": "name: Ada\ncity: Austin\n"}
            )
            hashed = await s.call_tool("hash_text", {"text": "hello"})
            b64 = await s.call_tool(
                "base64_convert_text", {"text": "hi", "action": "encode"}
            )
            outlined = await s.call_tool(
                "outline_markdown",
                {"path": os.path.join(HERE, "fixtures", "guide.md")},
            )
            md = await s.call_tool(
                "convert_to_markdown",
                {"path": os.path.join(HERE, "fixtures", "returns-help.html")},
            )
            tables = await s.call_tool(
                "extract_pdf_tables",
                {
                    "path": os.path.join(HERE, "fixtures", "ruled.pdf"),
                    "output_dir": os.path.join(HERE, "fixtures", "_mcp_tables"),
                },
            )
            missing = await s.call_tool(
                "repair_json_file", {"path": "/nope/missing.json"}
            )
            return (
                repaired,
                valid,
                from_file,
                shaped,
                hashed,
                b64,
                outlined,
                md,
                tables,
                missing,
            )

        (
            repaired,
            valid,
            from_file,
            shaped,
            hashed,
            b64,
            outlined,
            md,
            tables,
            missing,
        ) = asyncio.run(_session([os.path.join(ROOT, "tidy_byte_tools_mcp.py")], go))

        self.assertEqual(_data(repaired)["value"]["name"], "Ada")
        self.assertEqual(_data(repaired)["value"]["city"], "Austin")
        self.assertTrue(_data(repaired)["repaired"])
        self.assertTrue(_data(valid)["wasValid"])
        self.assertFalse(_data(valid)["repaired"])
        self.assertEqual(_data(from_file)["value"]["name"], "Ada")

        shaped_data = _data(shaped)
        # lite may wrap the object as {ok, format, data} or return data directly
        payload = shaped_data.get("data", shaped_data)
        if isinstance(payload, dict) and "name" not in payload and "data" in payload:
            payload = payload["data"]
        self.assertEqual(payload["name"], "Ada")

        hashed_data = _data(hashed)
        hashes = hashed_data.get("hashes", hashed_data)
        sha = hashes.get("sha256") if isinstance(hashes, dict) else None
        if isinstance(sha, dict):
            sha = sha.get("hex") or sha.get("value")
        self.assertTrue(sha, hashed_data)

        b64_data = _data(b64)
        text = b64_data.get("text") or b64_data.get("value") or b64_data.get("output") or ""
        if "aGk=" not in str(text):
            self.assertIn("aGk=", json.dumps(b64_data))

        self.assertFalse(outlined.isError, getattr(outlined, "content", None))
        self.assertIn("Install", json.dumps(_data(outlined)))

        md_text = md.content[0].text if md.content else json.dumps(_data(md))
        self.assertIn("How returns work", md_text)

        self.assertFalse(tables.isError, getattr(tables, "content", None))
        self.assertTrue(missing.isError)


if __name__ == "__main__":
    unittest.main()
