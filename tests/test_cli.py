"""CLI dispatcher: help, version, subcommands, and unknown commands."""

import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CLI = os.path.join(ROOT, "tidy_byte_tools.py")


def _run(args, input_text=None):
    return subprocess.run(
        [sys.executable, CLI, *args],
        capture_output=True,
        text=True,
        input=input_text,
        cwd=ROOT,
    )


class Cli(unittest.TestCase):
    def test_version(self):
        out = _run(["--version"])
        self.assertEqual(out.returncode, 0)
        self.assertEqual(out.stdout.strip(), "0.1.1")

    def test_help_lists_commands(self):
        out = _run(["--help"])
        self.assertEqual(out.returncode, 0)
        for name in (
            "json-repair",
            "json-shaper",
            "base64",
            "hash",
            "md-chunk",
            "doc2md",
            "pdf-table-pull",
            "link-check",
            "mcp",
        ):
            self.assertIn(name, out.stdout)

    def test_unknown_command(self):
        out = _run(["not-a-tool"])
        self.assertEqual(out.returncode, 2)
        self.assertIn("Unknown command", out.stderr)

    def test_json_repair_example(self):
        out = _run(["json-repair", "-q"], input_text='{name: "Ada", city: "Austin",}')
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(
            out.stdout.strip(),
            '{\n  "name": "Ada",\n  "city": "Austin"\n}',
        )

    def test_json_shaper_notes(self):
        out = _run(["json-shaper", "-q"], input_text="name: Ada\ncity: Austin\n")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('"name": "Ada"', out.stdout)
        self.assertIn('"city": "Austin"', out.stdout)

    def test_hash_text(self):
        out = _run(["hash", "--json", "-q"], input_text="hello")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("sha256", out.stdout.lower())

    def test_base64_encode(self):
        out = _run(["base64", "--action", "encode", "--json", "-q"], input_text="hi")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("aGk=", out.stdout)

    def test_pdf_table_pull(self):
        pdf = os.path.join(HERE, "fixtures", "ruled.pdf")
        dest = os.path.join(HERE, "fixtures", "_tables_out")
        out = _run(["pdf-table-pull", pdf, "-o", dest, "-q"])
        self.assertEqual(out.returncode, 0, out.stderr)
        table = os.path.join(dest, "page1_table1.csv")
        self.assertTrue(os.path.isfile(table), out.stdout + out.stderr)
        with open(table, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("Region,Q1,Q2", text)
        self.assertIn("North", text)

    def test_doc2md_html(self):
        html = os.path.join(HERE, "fixtures", "returns-help.html")
        out = _run(["doc2md", html, "-o", "-", "-q"])
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("How returns work", out.stdout)

    def test_md_chunk_outline(self):
        md = os.path.join(HERE, "fixtures", "guide.md")
        out = _run(["md-chunk", md, "--outline", "--json", "-q"])
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("Install", out.stdout)

    def test_subcommand_help(self):
        out = _run(["json-repair", "--help"])
        self.assertEqual(out.returncode, 0)
        self.assertIn("json-repair-lite", out.stdout)


if __name__ == "__main__":
    unittest.main()
