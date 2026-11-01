"""Render a Markdown file to PDF via headless Chrome.

Usage:  .venv/bin/python code/md2pdf.py plan/ajakava.md   (writes plan/ajakava.pdf)

Sections whose heading starts with "## 4." (the SMART table) are put on a
landscape page so the wide table fits.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LANDSCAPE_HEADING = re.compile(r"^## 4\.", re.M)

CSS = """
@page { size: A4 portrait; margin: 16mm 15mm; }
@page wide { size: A4 landscape; margin: 14mm 15mm; }
.landscape { page: wide; }
html { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10pt;
       color: #1a1a1a; line-height: 1.4; }
body { margin: 0; }
h1 { font-size: 19pt; margin: 0 0 6pt; }
h2 { font-size: 13pt; margin: 16pt 0 6pt; padding-bottom: 2pt; border-bottom: 1px solid #bbb;
     break-after: avoid; }
h3 { font-size: 11pt; margin: 12pt 0 4pt; break-after: avoid; }
p { margin: 4pt 0; }
hr { display: none; }
ul { margin: 3pt 0 3pt 0; padding-left: 16pt; }
li { margin: 1.5pt 0; }
li.task { list-style: none; margin-left: -14pt; padding-left: 14pt; text-indent: -14pt; }
li.task .box { display: inline-block; width: 14pt; text-indent: 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9pt; }
th, td { border: 1px solid #c8c8c8; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #eef1f5; }
tr { break-inside: avoid; }
.landscape table { font-size: 8.6pt; }
code { font-family: Menlo, monospace; font-size: 8.5pt; }
h3 + ul { break-before: avoid; }
"""


def tasks_to_html(html: str) -> str:
    """Turn '<li>[ ] x' / '<li>[x] x' into checkbox list items."""
    html = re.sub(r"<li>\[x\]\s*", '<li class="task"><span class="box">☑</span>', html)
    return re.sub(r"<li>\[ \]\s*", '<li class="task"><span class="box">☐</span>', html)


def blank_line_before_lists(md_text: str) -> str:
    """Python-Markdown needs a blank line between a paragraph and a list; GitHub doesn't."""
    out, prev = [], ""
    for line in md_text.splitlines():
        is_item = re.match(r"\s*[-*] ", line)
        prev_is_text = prev.strip() and not re.match(r"\s*([-*] |#|\|)", prev)
        if is_item and prev_is_text:
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def render(md_text: str) -> str:
    md_text = blank_line_before_lists(md_text)
    # nl2br: single newlines inside a paragraph become line breaks (header block etc.)
    conv = lambda s: tasks_to_html(markdown.markdown(s, extensions=["tables", "sane_lists", "nl2br"]))
    m = LANDSCAPE_HEADING.search(md_text)
    if m:
        body = conv(md_text[: m.start()]) + f'<section class="landscape">{conv(md_text[m.start():])}</section>'
    else:
        body = conv(md_text)
    return f'<!doctype html><html lang="et"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


def main(src: str) -> None:
    src_path = Path(src).resolve()
    out = src_path.with_suffix(".pdf")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(render(src_path.read_text(encoding="utf-8")))
        html_path = f.name
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={out}", f"file://{html_path}"],
        check=True, capture_output=True,
    )
    Path(html_path).unlink()
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
