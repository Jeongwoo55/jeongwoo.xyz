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
