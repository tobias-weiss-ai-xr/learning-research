#!/usr/bin/env python3
"""Bulk metadata fetcher for papers.yaml.

Fetches authors, venue, and abstract from arXiv and Semantic Scholar APIs.
Supports batch processing of arXiv IDs (~50 per request).
"""

import argparse
import re
import sys
import time
from pathlib import Path

import requests
import yaml

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/"
ARXIV_BATCH_API = "http://export.arxiv.org/api/query?id_list={}"


def load_papers(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data, data.get("papers", [])


def extract_arxiv_ids(papers):
    ids = []
    for p in papers:
        url = p.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        if match:
            ids.append(match.group(1))
    return ids


def fetch_arxiv_batch(arxiv_ids):
    if not arxiv_ids:
        return {}

    results = {}
    batch_size = 50

    for i in range(0, len(arxiv_ids), batch_size):
        batch = arxiv_ids[i : i + batch_size]
        id_list = ",".join(batch)
        try:
            resp = requests.get(ARXIV_BATCH_API.format(id_list), timeout=30)
            resp.raise_for_status()
            root = resp.text

            for match in re.finditer(r"<entry>(.*?)</entry>", root, re.DOTALL):
                entry_xml = match.group(1)
                entry = {}

                id_m = re.search(r"<id>(.*?)</id>", entry_xml)
                if id_m:
                    arxiv_id = ARXIV_ID_PATTERN.search(id_m.group(1))
                    if arxiv_id:
                        entry["arxiv_id"] = arxiv_id.group(1)

                title_m = re.search(r"<title>(.*?)</title>", entry_xml, re.DOTALL)
                if title_m:
                    entry["title"] = re.sub(r"\s+", " ", title_m.group(1).strip())

                authors_match = re.findall(
                    r"<author>.*?<name>(.*?)</name>.*?</author>",
                    entry_xml,
                    re.DOTALL,
                )
                if authors_match:
                    entry["authors"] = [
                        re.sub(r"\s+", " ", a.strip()) for a in authors_match
                    ]

                summary_m = re.search(r"<summary>(.*?)</summary>", entry_xml, re.DOTALL)
                if summary_m:
                    entry["abstract"] = re.sub(r"\s+", " ", summary_m.group(1).strip())

                category_m = re.search(r"<primary_category>(.*?)</category>", entry_xml)
                if category_m:
                    entry["arxiv_category"] = category_m.group(1).strip()

                if entry.get("arxiv_id"):
                    results[entry["arxiv_id"]] = entry

            time.sleep(3)

        except Exception as e:
            print(f"  WARNING: arXiv batch fetch error: {e}", flush=True)
            time.sleep(5)

    return results


def fetch_semantic_scholar(arxiv_id):
    try:
        url = f"{SEMANTIC_SCHOLAR_API}ArXiv:{arxiv_id}"
        params = {"fields": "title,authors,venue,year,publicationDate"}
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Bulk metadata fetcher for papers.yaml"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without modifying files"
    )
    parser.add_argument(
        "--paper-id", type=int, help="Fetch for a single paper (1-based index)"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip papers that already have authors",
    )
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    data, papers = load_papers(yaml_path)

    if not papers:
        print("No papers in papers.yaml.", flush=True)
        sys.exit(0)

    if args.paper_id:
        idx = args.paper_id - 1
        if idx < 0 or idx >= len(papers):
            print(f"Invalid paper index {args.paper_id} (1-{len(papers)})", flush=True)
            sys.exit(1)
        target_papers = [papers[idx]]
    else:
        target_papers = papers

    to_fetch = target_papers
    if args.skip_existing:
        to_fetch = [p for p in target_papers if not p.get("authors")]

    print(
        f"Fetching metadata for {len(to_fetch)} papers "
        f"(skipping {len(target_papers) - len(to_fetch)} with existing data)",
        flush=True,
    )

    arxiv_ids = extract_arxiv_ids(to_fetch)
    arxiv_meta = fetch_arxiv_batch(arxiv_ids)
    print(f"  arXiv returned metadata for {len(arxiv_meta)} IDs", flush=True)

    updated = 0
    for paper in to_fetch:
        url = paper.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        arxiv_id = match.group(1) if match else None

        if arxiv_id and arxiv_id in arxiv_meta:
            meta = arxiv_meta[arxiv_id]
            if not paper.get("authors") and meta.get("authors"):
                paper["authors"] = meta["authors"]
            if not paper.get("abstract") and meta.get("abstract"):
                paper["abstract"] = meta["abstract"]
            updated += 1

    print(f"  Updated {updated} papers from arXiv", flush=True)

    if args.dry_run:
        print("Dry run complete — no files modified.", flush=True)
        return

    data["papers"] = papers
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

    print(f"Saved updated metadata to {yaml_path}", flush=True)


if __name__ == "__main__":
    main()
