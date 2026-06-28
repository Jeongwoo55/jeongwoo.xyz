#!/usr/bin/env python3
"""Convert a blog markdown file into the site's HTML blog page format."""

from __future__ import annotations

import argparse
import html
import os
import pathlib
import re
from typing import Dict, List, Optional

BASE_HEAD = """<html>
  <head>
    <title>Jeongwoo's Blog</title>
    <!-- style file -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/@waline/client@v3/dist/waline.css"
    />
    <!-- script file -->
    <script type="module">
      import { init } from "https://unpkg.com/@waline/client@v3/dist/waline.js";

      init({
        el: "#waline",
        pageview: "#waline-pageview",
        serverURL: "https://waline-blog-five-snowy.vercel.app",
        lang: "en",
        dark: true,
        login: "disable",
        imageUploader: false,
      });
    </script>
    <link rel="stylesheet" href="/index.css" />
    <link rel="stylesheet" href="/blog/blog.css" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  </head>
  <body>
    <h1>Jeongwoo's Blog</h1>
    <navbar>
      <p>
        <a href="/">Home</a>
        <a href="/blog">Blog</a>
      </p>
    </navbar>
    <about>
"""

FOOTER = """
    </about>
    <!-- Waline Comments -->
    <div id="waline" style="max-width: 820px; margin: 40px auto"></div>
    <footer>
      <p>
        <a href="/">Home</a>
        <a href="/blog">Blog</a>
        <a href="mailto:jon@jeongwoo.xyz">Email</a>
        <a href="https://github.com/Jeongwoo55">GitHub</a>
        <a href="https://www.linkedin.com/in/jeongwooc">LinkedIn</a>
      </p>
      <p6>Page last updated: <time datetime="{date}">{date}</time></p6>
    </footer>
  </body>
</html>
"""


def parse_frontmatter(source: str) -> tuple[Dict[str, str], str]:
    if source.startswith("---\n"):
        lines = source.splitlines()
        metadata: Dict[str, str] = {}
        end_idx = None

        for idx, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                end_idx = idx
                break
            if ":" in line:
                key, _, value = line.partition(":")
                metadata[key.strip()] = value.strip().strip('"').strip("'")

        if end_idx is not None:
            body = "\n".join(lines[end_idx + 1 :])
            return metadata, body

    return {}, source


def sanitize_text(text: str) -> str:
    return html.escape(text, quote=True)


def inline_html(text: str) -> str:
    placeholders: List[str] = []

    def placeholder(html_fragment: str) -> str:
        placeholders.append(html_fragment)
        return f"§PLACEHOLDER{len(placeholders)-1}§"

    def replace_image(match: re.Match) -> str:
        alt_text = sanitize_text(match.group(1))
        url = sanitize_text(match.group(2))
        return placeholder(f'<img src="{url}" alt="{alt_text}" />')

    def replace_wiki_image(match: re.Match) -> str:
        src = sanitize_text(match.group(1))
        return placeholder(f'<img src="{src}" alt="{src}" />')

    def replace_link(match: re.Match) -> str:
        link_text = sanitize_text(match.group(1))
        url = sanitize_text(match.group(2))
        return placeholder(f'<a href="{url}">{link_text}</a>')

    def replace_wiki_link(match: re.Match) -> str:
        target = match.group(1).strip()
        label = sanitize_text(match.group(2).strip())
        if ". " in target:
            _, title = target.split(". ", 1)
        else:
            title = target
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        url = sanitize_text(f"/blog/{slug}")
        return placeholder(f'<a href="{url}">{label}</a>')

    def replace_bold(match: re.Match) -> str:
        return placeholder(f"<strong>{sanitize_text(match.group(1))}</strong>")

    def replace_italic(match: re.Match) -> str:
        return placeholder(f"<em>{sanitize_text(match.group(1))}</em>")

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, text)
    text = re.sub(r"!\[\[([^\]]+)\]\]", replace_wiki_image, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", replace_wiki_link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", replace_bold, text)
    text = re.sub(r"__(.+?)__", replace_bold, text)
    text = re.sub(r"\*([^*]+)\*", replace_italic, text)
    text = re.sub(r"_([^_]+)_", replace_italic, text)

    text = sanitize_text(text)
    for idx, fragment in enumerate(placeholders):
        text = text.replace(f"§PLACEHOLDER{idx}§", fragment)

    return text


def render_block(lines: List[str]) -> str:
    if not lines:
        return ""

    raw = "\n".join(lines).strip()
    heading_match = re.match(r"^(#{1,6})\s+(.*)$", raw)
    if heading_match:
        level = len(heading_match.group(1))
        return f"<h{level}>{inline_html(heading_match.group(2).strip())}</h{level}>"

    if len(lines) == 2:
        first = lines[0].strip()
        second = lines[1].strip()
        if re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", first):
            image_html = inline_html(first).strip()
            caption_html = inline_html(second)
            return (
                "<figure>\n"
                f"        {image_html}\n\n"
                f"        <figcaption>{caption_html}</figcaption>\n"
                "      </figure>"
            )

    return f"<p>{inline_html(' '.join(line.strip() for line in lines))}</p>"


def convert_markdown(body: str) -> str:
    lines = body.splitlines()
    blocks: List[str] = []
    buffer: List[str] = []
    mode: Optional[str] = None

    def flush_block() -> None:
        nonlocal buffer, mode
        if not buffer:
            return

        if mode == "list":
            items = [f"<li>{inline_html(item)}</li>" for item in buffer]
            blocks.append("<ul>" + "\n".join(items) + "</ul>")
        elif mode == "blockquote":
            paragraphs = []
            current: List[str] = []
            for line in buffer:
                if line.strip() == "":
                    if current:
                        paragraphs.append(f"<p>{inline_html(' '.join(current))}</p>")
                        current = []
                else:
                    current.append(line)
            if current:
                paragraphs.append(f"<p>{inline_html(' '.join(current))}</p>")
            blocks.append("<blockquote>" + "\n".join(paragraphs) + "</blockquote>")
        else:
            blocks.append(render_block(buffer))

        buffer = []
        mode = None

    for line in lines + [""]:
        stripped = line.strip()
        if stripped == "":
            flush_block()
            continue

        if re.match(r"^(#{1,6})\s+.*", stripped):
            flush_block()
            mode = "paragraph"
            buffer = [stripped]
            flush_block()
            continue

        if line.startswith("> "):
            if mode != "blockquote":
                flush_block()
                mode = "blockquote"
            buffer.append(line[2:])
            continue

        if re.match(r"^([-*])\s+.*", line):
            if mode != "list":
                flush_block()
                mode = "list"
            buffer.append(line.strip()[2:])
            continue

        if mode in {"list", "blockquote"}:
            flush_block()

        if mode != "paragraph":
            mode = "paragraph"
        buffer.append(line)

    return "\n      ".join(blocks)


def build_html(title: str, datetime_value: str, date_display: str, body_html: str) -> str:
    date_html = ""
    if date_display:
        datetime_attr = sanitize_text(datetime_value) if datetime_value else sanitize_text(date_display)
        date_html = f"      <p6>Posted on <time datetime=\"{datetime_attr}\">{sanitize_text(date_display)}</time></p6>\n"
    return f"{BASE_HEAD}      <h1>{sanitize_text(title)}</h1>\n{date_html}      {body_html}\n{FOOTER.format(date=sanitize_text(date_display))}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a markdown blog post to the site's HTML output.")
    parser.add_argument("source", help="Markdown file to convert")
    parser.add_argument(
        "--output",
        help="Output HTML file path. Defaults to <source-slug>/index.html",
        default=None,
    )
    args = parser.parse_args()

    source_path = pathlib.Path(args.source)
    if not source_path.exists() or not source_path.is_file():
        raise FileNotFoundError(f"Markdown file not found: {source_path}")

    content = source_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)
    title = metadata.get("title")
    published = metadata.get("published", metadata.get("date", ""))
    display_date = published.split("T", 1)[0] if published else ""

    if not title:
        first_heading = None
        for line in body.splitlines():
            if line.strip().startswith("##"):
                first_heading = line.strip().lstrip("#").strip()
                break
        inferred_title = source_path.stem.replace("-", " ").title()
        if first_heading and first_heading.lower() not in {"intro", "introduction"}:
            title = first_heading
        else:
            title = inferred_title

    html_body = convert_markdown(body)

    output_path = pathlib.Path(args.output) if args.output else source_path.with_suffix("").name
    if args.output is None:
        output_path = source_path.with_suffix("").with_name(source_path.stem) / "index.html"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(title, published, display_date, html_body), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
