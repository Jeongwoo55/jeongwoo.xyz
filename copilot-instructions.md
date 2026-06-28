# Copilot markdown to blog HTML conversion

Use this repository's blog post converter whenever you need to turn a markdown blog post into the site’s HTML format.

Usage:

```bash
python blog/convert_md_to_html.py blog/planning-my-home-server.md
```

This will create or overwrite `blog/planning-my-home-server/index.html` and preserve the same page structure, styles, and comment integration used by the existing blog examples.

If you want a custom target file, pass `--output`:

```bash
python blog/convert_md_to_html.py blog/planning-my-home-server.md --output blog/planning-my-home-server/index.html
```

## Atom feed generation

You can generate an Atom feed from the repository's markdown blog files using the script:

```bash
python blog/generate_atom.py
```

This creates or updates `blog/atom.xml` by reading the frontmatter from `blog/*.md` and converting titles, dates, and excerpts into Atom entries.
