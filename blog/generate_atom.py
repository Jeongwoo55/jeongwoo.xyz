#!/usr/bin/env python3
import html
import pathlib
import re
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xml_escape

BASE_URL = "https://jeongwoo.xyz"
BLOG_URL = f"{BASE_URL}/blog"
OUTPUT_FILE = "atom.xml"
MAX_ITEMS = 20
FRONTMATTER_RE = re.compile(r"^---\s*$", re.MULTILINE)


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text

    parts = FRONTMATTER_RE.split(text, maxsplit=2)
    if len(parts) < 3:
        return {}, text

    raw_meta = parts[1].strip().splitlines()
    body = parts[2].strip()
    meta = {}

    for line in raw_meta:
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"').strip("'")

    return meta, body


def extract_excerpt(body: str) -> str:
    for line in body.splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("#"):
            continue
        return re.sub(r"\s+", " ", text)
    return ""


def extract_html_content(html_text: str) -> str:
    match = re.search(r"<about>(.*?)</about>", html_text, re.S)
    if match:
        return match.group(1).strip()
    return ""


def markdown_to_html(text: str) -> str:
    text = xml_escape(text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: f'<a href="{html.escape(match.group(2), quote=True)}">{xml_escape(match.group(1))}</a>',
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    return text


def format_atom_date(date: datetime) -> str:
    utc = date.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def wrap_cdata(text: str) -> str:
    return f"<![CDATA[{text.replace(']]>', ']]]]><![CDATA[>')}]]>"


def build_atom(entries):
    updated = entries[0]["updated"] if entries else datetime.now(timezone.utc)
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">',
        f'  <title>{xml_escape("Jeongwoo\'s Blog")}</title>',
        f'  <link rel="self" type="application/atom+xml" href="{xml_escape(f"{BLOG_URL}/{OUTPUT_FILE}")}"/>',
        f'  <link rel="alternate" type="text/html" href="{xml_escape(BLOG_URL)}"/>',
        '  <generator uri="https://jeongwoo.xyz/">custom script</generator>',
        f'  <updated>{format_atom_date(updated)}</updated>',
        f'  <id>{xml_escape(f"{BLOG_URL}/{OUTPUT_FILE}")}</id>',
    ]

    for entry in entries:
        content_html = entry["content_html"]
        lines.extend(
            [
                '  <entry xml:lang="en">',
                f'    <title>{xml_escape(entry["title"])}</title>',
                f'    <link rel="alternate" type="text/html" href="{xml_escape(entry["link"])}"/>',
                f'    <id>{xml_escape(entry["link"])}</id>',
                f'    <published>{format_atom_date(entry["published"])}</published>',
                f'    <updated>{format_atom_date(entry["updated"])}</updated>',
                '    <author>',
                f'      <name>{xml_escape(entry["author"])}</name>',
                '    </author>',
                f'    <content type="html" xml:base="{xml_escape(entry["link"])}">{wrap_cdata(content_html)}</content>',
                '  </entry>',
            ]
        )

    lines.append('</feed>')
    return "\n".join(lines)


def main() -> int:
    script_dir = pathlib.Path(__file__).resolve().parent
    root = script_dir.parent
    blog_dir = root / "blog"
    output_path = blog_dir / OUTPUT_FILE

    posts = []
    for md_path in blog_dir.glob("*.md"):
        content = md_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        title = meta.get("title")
        date_text = meta.get("date")
        if not title or not date_text:
            continue

        try:
            published = datetime.fromisoformat(date_text).replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                published = datetime.strptime(date_text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue

        slug = md_path.stem
        link = f"{BLOG_URL}/{slug}/"
        html_path = blog_dir / slug / "index.html"
        if html_path.exists():
            content_html = extract_html_content(html_path.read_text(encoding="utf-8"))
        else:
            excerpt = extract_excerpt(body)
            content_html = markdown_to_html(excerpt)

        posts.append(
            {
                "title": title,
                "published": published,
                "updated": published,
                "author": "Jeongwoo Choi",
                "link": link,
                "content_html": content_html,
            }
        )

    posts.sort(key=lambda item: item["updated"], reverse=True)
    atom = build_atom(posts[:MAX_ITEMS])
    output_path.write_text(atom, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
