#!/usr/bin/env python3
"""Discover new learning research papers from arXiv API across all 20 categories.

Runs 100+ queries spanning cognitive science, neuroscience, education, ML,
and all other disciplines in the taxonomy.
"""

import argparse
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import yaml

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
ARXIV_SEARCH_API = (
    "http://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
)

QUERIES = [
    'cat:cs.AI AND abs:"learning" AND abs:"agent"',
    'cat:cs.LG AND abs:"learning" AND abs:"neural"',
    'cat:cs.CL AND abs:"language learning" AND abs:"model"',
    'cat:cs.AI AND abs:"meta-learning"',
    'cat:cs.LG AND abs:"meta-learning"',
    'cat:cs.AI AND abs:"reinforcement learning" AND abs:"agent"',
    'cat:cs.LG AND abs:"reinforcement learning"',
    'cat:cs.AI AND abs:"self-supervised learning"',
    'cat:cs.LG AND abs:"self-supervised learning"',
    'cat:cs.AI AND abs:"continual learning"',
    'cat:cs.LG AND abs:"continual learning"',
    'cat:cs.AI AND abs:"curriculum learning"',
    'cat:cs.LG AND abs:"curriculum learning"',
    'cat:cs.AI AND abs:"few-shot learning"',
    'cat:cs.LG AND abs:"few-shot learning"',
    'cat:cs.AI AND abs:"transfer learning"',
    'cat:cs.LG AND abs:"transfer learning"',
    'cat:cs.AI AND abs:"active learning"',
    'cat:cs.LG AND abs:"active learning"',
    'cat:cs.AI AND abs:"deep learning" AND abs:"survey"',
    'cat:cs.LG AND abs:"deep learning" AND abs:"survey"',
    'cat:cs.AI AND abs:"spiking neural" AND abs:"learning"',
    'cat:cs.AI AND abs:"neuromorphic" AND abs:"learning"',
    'cat:cs.LG AND abs:"neuromorphic" AND abs:"learning"',
    'cat:cs.AI AND abs:"federated learning" AND abs:"survey"',
    'cat:cs.LG AND abs:"federated learning" AND abs:"survey"',
    'cat:cs.AI AND abs:"imitation learning" AND abs:"robot"',
    'cat:cs.RO AND abs:"imitation learning"',
    'cat:cs.RO AND abs:"robot learning"',
    'cat:cs.AI AND abs:"skill acquisition" AND abs:"agent"',
    'cat:cs.AI AND abs:"in-context learning"',
    'cat:cs.CL AND abs:"in-context learning"',
    'cat:cs.AI AND abs:"instruction learning" AND abs:"LLM"',
    'cat:cs.CL AND abs:"instruction learning" AND abs:"LLM"',
    'cat:cs.AI AND abs:"learning theory" AND abs:"generalization"',
    'cat:cs.LG AND abs:"learning theory" AND abs:"generalization"',
    'cat:cs.AI AND abs:"swarm" AND abs:"learning"',
    'cat:cs.MA AND abs:"swarm" AND abs:"learning"',
    'cat:cs.AI AND abs:"collective" AND abs:"learning"',
    'cat:cs.MA AND abs:"collective" AND abs:"learning"',
    'cat:cs.AI AND abs:"multi-agent" AND abs:"learning"',
    'cat:cs.MA AND abs:"multi-agent" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"learning" AND abs:"neural plasticity"',
    'cat:q-bio.NC AND abs:"synaptic" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"memory" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"cognitive" AND abs:"learning"',
    'cat:cs.AI AND abs:"cognitive" AND abs:"model" AND abs:"learning"',
    'cat:cs.AI AND abs:"memory" AND abs:"learning" AND abs:"model"',
    'cat:cs.AI AND abs:"decision" AND abs:"learning"',
    'cat:cs.CY AND abs:"machine learning" AND abs:"education"',
    'cat:cs.HC AND abs:"learning" AND abs:"technology"',
    'cat:cs.CY AND abs:"intelligent tutoring"',
    'cat:cs.AI AND abs:"educational" AND abs:"data mining"',
    'cat:cs.CY AND abs:"gamification" AND abs:"learning"',
    'cat:cs.CL AND abs:"language acquisition" AND abs:"model"',
    'cat:cs.CL AND abs:"bilingual" AND abs:"learning"',
    'cat:cs.CL AND abs:"speech" AND abs:"learning"',
    'cat:cs.SD AND abs:"motor learning"',
    'cat:cs.RO AND abs:"motor learning" AND abs:"robot"',
    'cat:cs.AI AND abs:"creative" AND abs:"learning"',
    'cat:cs.AI AND abs:"creative" AND abs:"cognition"',
    'cat:q-bio.NC AND abs:"emotion" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"affective" AND abs:"learning"',
    'cat:cs.AI AND abs:"animal" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"comparative" AND abs:"cognition"',
    'cat:q-bio.PE AND abs:"animal" AND abs:"learning"',
    'cat:cs.AI AND abs:"evolutionary" AND abs:"learning"',
    'cat:cs.NE AND abs:"evolutionary" AND abs:"learning"',
    'cat:cs.AI AND abs:"perceptual" AND abs:"learning"',
    'cat:cs.CV AND abs:"perceptual" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"perceptual" AND abs:"learning"',
    'cat:cs.AI AND abs:"habit" AND abs:"formation" AND abs:"learning"',
    'cat:cs.AI AND abs:"behavioral" AND abs:"learning"',
    'cat:cs.SI AND abs:"social" AND abs:"learning"',
    'cat:cs.MA AND abs:"social" AND abs:"learning"',
    'cat:cs.CY AND abs:"health" AND abs:"learning"',
    'cat:cs.AI AND abs:"medical" AND abs:"training"',
    'cat:cs.HC AND abs:"patient education"',
    'cat:q-bio.NC AND abs:"infant" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"child" AND abs:"development" AND abs:"learning"',
    'cat:cs.AI AND abs:"epistemology" AND abs:"learning"',
    'cat:cs.AI AND abs:"consciousness" AND abs:"learning"',
    'cat:cs.AI AND abs:"growth mindset" AND abs:"learning"',
    'cat:cs.CY AND abs:"motivation" AND abs:"learning"',
    'cat:cs.AI AND abs:"zone of proximal" AND abs:"learning"',
    'cat:cs.AI AND abs:"self-regulation" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"forgetting" AND abs:"memory"',
    'cat:q-bio.NC AND abs:"working memory" AND abs:"learning"',
    'cat:cs.AI AND abs:"working memory" AND abs:"model"',
    'cat:q-bio.NC AND abs:"episodic memory" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"semantic memory" AND abs:"learning"',
    'cat:cs.AI AND abs:"forgetting" AND abs:"machine learning"',
    'cat:cs.LG AND abs:"catastrophic forgetting"',
    'cat:cs.CV AND abs:"continual learning" AND abs:"class"',
    'cat:cs.NE AND abs:"spiking" AND abs:"network" AND abs:"learning"',
    'cat:cs.ET AND abs:"brain-computer interface" AND abs:"learning"',
    'cat:cs.HC AND abs:"VR" AND abs:"learning"',
    'cat:cs.HC AND abs:"augmented reality" AND abs:"learning"',
    'cat:cs.AI AND abs:"organizational" AND abs:"learning"',
    'cat:cs.CY AND abs:"online learning" AND abs:"platform"',
    'cat:cs.CL AND abs:"literacy" AND abs:"learning"',
    'cat:cs.AI AND abs:"skill" AND abs:"learning" AND abs:"survey"',
    'cat:cs.AI AND abs:"learning" AND abs:"representation"',
    'cat:cs.LG AND abs:"representation learning"',
    'cat:cs.AI AND abs:"contrastive learning"',
    'cat:cs.LG AND abs:"contrastive learning"',
    'cat:cs.AI AND abs:"graph learning"',
    'cat:cs.LG AND abs:"graph learning"',
    'cat:cs.AI AND abs:"world model" AND abs:"learning"',
    'cat:cs.LG AND abs:"world model" AND abs:"learning"',
]


def load_existing_papers(yaml_path):
    if not yaml_path.exists():
        return {}, []
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    by_id = {}
    titles_lower = []
    for p in papers:
        url = p.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        if match:
            by_id[match.group(1)] = p
        titles_lower.append(p.get("title", "").lower().strip())
    return by_id, titles_lower


def search_arxiv(query, months, start=0, max_results=100):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=months * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"

    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"
    try:
        resp = requests.get(
            ARXIV_SEARCH_API.format(
                requests.utils.quote(full_query), start, max_results
            ),
            timeout=30,
        )
        resp.raise_for_status()
        entries = []
        root = resp.text
        for match in re.finditer(r"<entry>(.*?)</entry>", root, re.DOTALL):
            entry_xml = match.group(1)
            entry = {}
            title_m = re.search(r"<title>(.*?)</title>", entry_xml, re.DOTALL)
            if title_m:
                entry["title"] = re.sub(r"\s+", " ", title_m.group(1).strip())
            id_m = re.search(r"<id>(.*?)</id>", entry_xml)
            if id_m:
                entry["url"] = id_m.group(1).strip().replace("http://", "https://")
            published_m = re.search(r"<published>(.*?)</published>", entry_xml)
            if published_m:
                entry["date"] = published_m.group(1).strip()[:7]
            summary_m = re.search(r"<summary>(.*?)</summary>", entry_xml, re.DOTALL)
            if summary_m:
                entry["abstract"] = re.sub(r"\s+", " ", summary_m.group(1).strip())
            if entry.get("title") and entry.get("url"):
                entries.append(entry)
        return entries
    except Exception as e:
        print(f"  WARNING: arXiv search error: {e}", flush=True)
        return []


def format_yaml_entry(entry):
    title = entry["title"].replace('"', '\\"')
    lines = [
        f'  - title: "{title}"',
        f'    date: "{entry.get("date", "")}"',
        f'    url: "{entry.get("url", "")}"',
        f'    category: ""  # TODO: see CONTRIBUTING.md for valid categories',
        f'    subcategory: ""  # TODO: see CONTRIBUTING.md for valid subcategories',
    ]
    if entry.get("abstract"):
        abstract = entry["abstract"][:200].replace('"', '\\"')
        lines.append(f'    abstract: "{abstract}..."')
    return "\n".join(lines)


def _append_local(yaml_path, all_new):
    """Append discovered papers directly to papers.yaml (no GitHub)."""
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    before = len(papers)
    for entry in all_new:
        papers.append(
            {
                "title": entry.get("title", ""),
                "date": entry.get("date", ""),
                "url": entry.get("url", ""),
                "category": "",
                "subcategory": "",
                "abstract": entry.get("abstract", ""),
            }
        )
    data["papers"] = papers
    with open(yaml_path, "w") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
    print(f"Saved {len(papers) - before} new papers to papers.yaml", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Discover new learning research papers from arXiv"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=3,
        help="Search papers from the last N months (default: 3)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without creating anything"
    )
    parser.add_argument(
        "--create-pr", action="store_true", help="Create a GitHub PR with new papers"
    )
    parser.add_argument(
        "--local", action="store_true", help="Append discovered papers locally (no GitHub)"
    )
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    by_id, titles_lower = load_existing_papers(yaml_path)

    print(f"Loaded {len(by_id)} existing papers from papers.yaml", flush=True)
    print(
        f"Searching arXiv for papers from the last {args.months} month(s)...",
        flush=True,
    )

    all_new = []
    for qi, query in enumerate(QUERIES):
        print(f"\nQuery {qi + 1}/{len(QUERIES)}...", flush=True)
        entries = search_arxiv(query, args.months)
        for entry in entries:
            arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None

            if arxiv_id and arxiv_id in by_id:
                continue

            title_lower = entry.get("title", "").lower().strip()
            if any(title_lower == t for t in titles_lower):
                continue

            if arxiv_id and any(e.get("url", "") == entry["url"] for e in all_new):
                continue

            all_new.append(entry)

        time.sleep(3)

    print(
        f"\nFound {len(all_new)} new papers ({len(by_id)} already in list)", flush=True
    )

    if not all_new:
        print("No new papers to add.", flush=True)
        return

    print("\n--- New Papers ---", flush=True)
    for entry in all_new:
        print(format_yaml_entry(entry), flush=True)
        print(flush=True)

    if args.dry_run:
        print("\nDry run complete — no files modified", flush=True)
        return

    if args.local:
        print(f"\nAppending {len(all_new)} new papers locally...", flush=True)
        _append_local(yaml_path, all_new)
        return

    if args.create_pr:
        branch_name = f"add-new-papers-{datetime.now().strftime('%Y%m%d')}"

        print(f"\nCreating branch '{branch_name}' and PR...", flush=True)

        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name], check=True, cwd=yaml_path.parent
            )
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f) or {}
            papers = data.get("papers", [])
            for entry in all_new:
                papers.append(
                    {
                        "title": entry.get("title", ""),
                        "date": entry.get("date", ""),
                        "url": entry.get("url", ""),
                        "category": "",
                        "subcategory": "",
                        "abstract": entry.get("abstract", ""),
                    }
                )
            data["papers"] = papers
            with open(yaml_path, "w") as f:
                yaml.dump(
                    data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            subprocess.run(
                ["git", "add", "papers.yaml"], check=True, cwd=yaml_path.parent
            )
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"Add {len(all_new)} new papers from arXiv discovery",
                ],
                check=True,
                cwd=yaml_path.parent,
            )
            subprocess.run(
                ["git", "push", "origin", branch_name], check=True, cwd=yaml_path.parent
            )
            subprocess.run(
                [
                    "gh",
                    "pr",
                    "create",
                    "--title",
                    f"Add {len(all_new)} new papers from arXiv discovery",
                    "--body",
                    f"Automatically discovered {len(all_new)} new papers.\n\n**Please review taxonomy assignments.**",
                ],
                check=True,
                cwd=yaml_path.parent,
            )
            print("PR created successfully!", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to create PR: {e}", flush=True)
            sys.exit(1)
    else:
        print(
            "\nTo add these papers, re-run with --create-pr or manually add to papers.yaml",
            flush=True,
        )


if __name__ == "__main__":
    main()
