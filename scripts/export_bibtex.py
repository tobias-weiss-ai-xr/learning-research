#!/usr/bin/env python3
"""Export papers from papers.yaml to BibTeX format."""

import sys
from pathlib import Path

import yaml


def make_bibtex_key(paper):
    title = paper.get("title", "").lower()
    words = [w for w in title.split() if len(w) > 2][:4]
    authors = paper.get("authors", [])
    if authors:
        last = authors[0].split()[-1].lower()
    else:
        last = "unknown"
    key = f"{last}{paper.get('date', '0000')[:4]}"
    for w in words:
        key += w[:3]
    return key


def escape_bibtex(text):
    for ch, rep in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")]:
        text = text.replace(ch, rep)
    return text


def main():
    yaml_path = Path(__file__).resolve().parent.parent / "papers.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    papers = data.get("papers", [])
    if not papers:
        print("No papers to export.", flush=True)
        sys.exit(0)

    keys_seen = set()
    entries = []

    for p in papers:
        key = make_bibtex_key(p)
        base_key = key
        suffix = 1
        while key in keys_seen:
            key = f"{base_key}{chr(96 + suffix)}"
            suffix += 1
        keys_seen.add(key)

        title = escape_bibtex(p.get("title", ""))
        authors_list = p.get("authors", [])
        authors_str = " and ".join(authors_list) if authors_list else "Unknown"
        year = p.get("date", "")[:4] or "0000"
        url = p.get("url", "")
        venue = p.get("venue", "")

        entry = f"@article{{{key},\n"
        entry += f"  title = {{{title}}},\n"
        entry += f"  author = {{{authors_str}}},\n"
        entry += f"  year = {{{year}}},\n"
        if venue:
            entry += f"  journal = {{{venue}}},\n"
        if url:
            entry += f"  url = {{{url}}},\n"
        entry += "}\n"
        entries.append(entry)

    out_path = Path(__file__).resolve().parent.parent / "docs" / "references.bib"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(entries), encoding="utf-8")
    print(f"Exported {len(entries)} entries to {out_path}")


if __name__ == "__main__":
    main()
