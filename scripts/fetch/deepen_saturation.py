#!/usr/bin/env python3
"""Deepen learning-research: fill remaining 27 empty cells via arXiv + Semantic Scholar."""

import json, re, sys, time
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

import requests, yaml

ARXIV_API = "http://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
API_DELAY = 2
MAX_RETRIES = 5

VALID_CATEGORIES = {
    "cognitive-science",
    "neuroscience",
    "education",
    "developmental",
    "behavioral",
    "social-learning",
    "language",
    "motor",
    "emotion",
    "creative",
    "machine-learning",
    "evolutionary",
    "philosophy-of-mind",
    "educational-psychology",
    "animal-learning",
    "neuromorphic",
    "memory-science",
    "perceptual",
    "collective",
    "health",
}
ASPECTS = [
    "theory",
    "mechanism",
    "method",
    "application",
    "development",
    "individual-differences",
    "technology",
    "review",
]

YAML_PATH = Path(__file__).resolve().parent.parent.parent / "papers.yaml"


def load():
    with open(YAML_PATH) as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    by_id, titles_lower = {}, []
    for p in papers:
        m = re.search(r"(\d{4}\.\d{4,5})", p.get("url", ""))
        if m:
            by_id[m.group(1)] = p
        titles_lower.append(p.get("title", "").lower().strip())
    return data, papers, by_id, titles_lower


def similar(a, b):
    return (
        SequenceMatcher(
            None, re.sub(r"[^\w\s]", "", a.lower()), re.sub(r"[^\w\s]", "", b.lower())
        ).ratio()
        >= 0.75
    )


def save(data, papers):
    data["papers"] = papers
    with open(YAML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


ARXIV_QUERIES = [
    # Single-cell gaps with broad all: queries
    ("collective", "review", 'all:"swarm intelligence" AND all:"review"'),
    ("collective", "review", 'all:"collective intelligence" AND all:"survey"'),
    ("developmental", "review", 'all:"child development" AND all:"review"'),
    ("developmental", "review", 'all:"cognitive development" AND all:"survey"'),
    ("emotion", "development", 'all:"emotional development" AND all:"learning"'),
    ("emotion", "development", 'all:"affective development" AND all:"learning"'),
    (
        "evolutionary",
        "individual-differences",
        'all:"evolutionary psychology" AND all:"individual differences"',
    ),
    ("health", "development", 'all:"health behavior" AND all:"development"'),
    ("motor", "review", 'all:"motor learning" AND all:"review"'),
    ("motor", "review", 'all:"skill acquisition" AND all:"survey"'),
    ("neuromorphic", "development", 'all:"neuromorphic" AND all:"development"'),
    (
        "neuroscience",
        "development",
        'all:"neuroscience" AND all:"development" AND all:"learning"',
    ),
    (
        "neuroscience",
        "individual-differences",
        'all:"neuroscience" AND all:"individual differences"',
    ),
    (
        "neuroscience",
        "review",
        'all:"neuroscience" AND all:"learning" AND all:"review"',
    ),
    (
        "philosophy-of-mind",
        "development",
        'all:"philosophy" AND all:"mind" AND all:"development"',
    ),
    ("social-learning", "development", 'all:"social learning" AND all:"development"'),
    # memory-science broader queries
    (
        "memory-science",
        "mechanism",
        'all:"memory" AND all:"mechanism" AND all:"neural"',
    ),
    (
        "memory-science",
        "application",
        'all:"memory" AND all:"training" AND all:"intervention"',
    ),
    (
        "memory-science",
        "development",
        'all:"memory" AND all:"development" AND all:"cognitive"',
    ),
    (
        "memory-science",
        "individual-differences",
        'all:"working memory" AND all:"individual"',
    ),
    (
        "memory-science",
        "technology",
        'all:"memory" AND all:"technology" AND all:"learning"',
    ),
    ("memory-science", "review", 'all:"memory systems" AND all:"review"'),
    # perceptual broader queries
    ("perceptual", "method", 'all:"perceptual learning" AND all:"method"'),
    ("perceptual", "application", 'all:"perceptual learning" AND all:"application"'),
    ("perceptual", "development", 'all:"perceptual" AND all:"development"'),
    (
        "perceptual",
        "individual-differences",
        'all:"perceptual" AND all:"individual differences"',
    ),
    ("perceptual", "technology", 'all:"perceptual" AND all:"technology"'),
    ("perceptual", "review", 'all:"perceptual learning" AND all:"review"'),
    # animal-learning remaining
    (
        "animal-learning",
        "individual-differences",
        'all:"animal cognition" AND all:"individual"',
    ),
    (
        "animal-learning",
        "technology",
        'all:"animal" AND all:"tracking" AND all:"learning"',
    ),
    ("animal-learning", "review", 'all:"animal learning" AND all:"review"'),
]

S2_QUERIES_BY_CELL = {
    ("memory-science", "mechanism"): [
        "memory consolidation neural mechanism",
        "synaptic plasticity memory mechanism",
    ],
    ("memory-science", "application"): [
        "memory training intervention",
        "memory enhancement application",
    ],
    ("memory-science", "development"): [
        "memory development child adolescent",
        "working memory development lifespan",
    ],
    ("memory-science", "individual-differences"): [
        "working memory individual differences",
        "memory capacity individual differences",
    ],
    ("memory-science", "technology"): [
        "memory assistive technology",
        "memory training app technology",
    ],
    ("memory-science", "review"): ["memory systems review", "human memory review"],
    ("perceptual", "method"): [
        "perceptual learning methods",
        "perceptual training methods",
    ],
    ("perceptual", "application"): [
        "perceptual learning applications",
        "perceptual training real world",
    ],
    ("perceptual", "development"): [
        "perceptual development children",
        "visual development infancy",
    ],
    ("perceptual", "individual-differences"): [
        "perceptual abilities individual differences",
        "perceptual cognition individual",
    ],
    ("perceptual", "technology"): [
        "perceptual learning technology",
        "perceptual training virtual reality",
    ],
    ("perceptual", "review"): [
        "perceptual learning review",
        "perceptual expertise review",
    ],
    ("neuroscience", "development"): [
        "developmental neuroscience learning",
        "brain development learning",
    ],
    ("neuroscience", "individual-differences"): [
        "individual differences brain structure learning"
    ],
    ("neuroscience", "review"): [
        "neuroscience learning review",
        "brain mechanisms learning review",
    ],
}


def search_arxiv(query):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=48 * 30)
    date_range = f"submittedDate:[{cutoff.strftime('%Y%m%d0000')} TO {now.strftime('%Y%m%d')}2359]"
    full = f"({query}) AND {date_range}"
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(ARXIV_API.format(quote(full), 0, 100), timeout=60)
            if resp.status_code == 429:
                time.sleep(10 * (2**attempt))
                continue
            resp.raise_for_status()
            entries = []
            for m in re.finditer(r"<entry>(.*?)</entry>", resp.text, re.DOTALL):
                xml = m.group(1)
                e = {}
                t = re.search(r"<title>(.*?)</title>", xml, re.DOTALL)
                if t:
                    e["title"] = re.sub(r"\s+", " ", t.group(1).strip())
                i = re.search(r"<id>(.*?)</id>", xml)
                if i:
                    e["url"] = i.group(1).strip().replace("http://", "https://")
                p = re.search(r"<published>(.*?)</published>", xml)
                if p:
                    e["date"] = p.group(1).strip()[:7]
                s = re.search(r"<summary>(.*?)</summary>", xml, re.DOTALL)
                if s:
                    e["abstract"] = re.sub(r"\s+", " ", s.group(1).strip())
                if e.get("title") and e.get("url"):
                    entries.append(e)
            return entries
        except Exception as ex:
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (2**attempt))
            else:
                print(f"  arXiv failed: {ex}")
                return []
    return []


def search_s2(query):
    params = {"query": query, "limit": 100, "fields": "title,url,year,abstract,venue"}
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(
                S2_API,
                params=params,
                timeout=30,
                headers={"User-Agent": "LearningResearch/1.0"},
            )
            if resp.status_code == 429:
                time.sleep(5 * (2**attempt))
                continue
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
            data = resp.json()
            entries = []
            for p in data.get("data", []):
                e = {
                    "title": p.get("title", ""),
                    "url": p.get("url", "")
                    or f"https://api.semanticscholar.org/CorpusID:{p.get('paperId', '')}",
                    "date": str(p.get("year", "")),
                    "abstract": p.get("abstract", "") or "",
                    "venue": p.get("venue", ""),
                }
                if e["title"] and e["url"]:
                    entries.append(e)
            return entries
        except Exception as ex:
            if attempt < MAX_RETRIES - 1:
                time.sleep(3 * (2**attempt))
            else:
                print(f"  S2 failed: {ex}")
                return []
    return []


def classify(title, abstract, intended_cat, intended_sub):
    text = f"{title} {abstract}".lower()
    cat_kw = {
        "cognitive-science": [
            "cognitive",
            "mental model",
            "attention",
            "decision making",
            "working memory",
        ],
        "neuroscience": [
            "synaptic",
            "neural plasticity",
            "dopamine",
            "hippocampus",
            "fMRI",
            "brain region",
        ],
        "education": [
            "pedagogy",
            "instructional",
            "classroom",
            "educational technology",
            "assessment",
            "tutoring",
        ],
        "developmental": [
            "child development",
            "language acquisition",
            "cognitive development",
            "infant",
            "lifespan",
        ],
        "behavioral": [
            "behavioral economics",
            "habit",
            "conditioning",
            "reinforcement",
            "behavior change",
        ],
        "social-learning": [
            "social learning",
            "observational",
            "cultural transmission",
            "peer",
            "collaborative",
            "imitation",
        ],
        "language": [
            "language learning",
            "linguistic",
            "bilingual",
            "literacy",
            "speech",
            "phonological",
        ],
        "motor": [
            "motor learning",
            "skill acquisition",
            "procedural memory",
            "embodied",
            "sensorimotor",
        ],
        "emotion": [
            "emotional learning",
            "affective",
            "emotion regulation",
            "fear",
            "anxiety",
            "sentiment",
        ],
        "creative": [
            "creativity",
            "creative",
            "artistic",
            "divergent thinking",
            "innovation",
            "design",
        ],
        "machine-learning": [
            "deep learning",
            "supervised",
            "reinforcement",
            "self-supervised",
            "meta-learning",
            "transformer",
            "neural network",
        ],
        "evolutionary": [
            "evolution",
            "comparative cognition",
            "cultural evolution",
            "phylogenetic",
            "natural selection",
        ],
        "philosophy-of-mind": [
            "epistemology",
            "consciousness",
            "mental representation",
            "phenomenology",
            "intentionality",
        ],
        "educational-psychology": [
            "motivation",
            "self-regulation",
            "growth mindset",
            "scaffolding",
            "self-efficacy",
            "engagement",
        ],
        "animal-learning": [
            "animal cognition",
            "animal memory",
            "foraging",
            "animal learning",
            "primate",
            "bird song",
        ],
        "neuromorphic": [
            "neuromorphic",
            "spiking neural",
            "brain-inspired",
            "memristor",
            "event-driven",
        ],
        "memory-science": [
            "episodic memory",
            "semantic memory",
            "procedural memory",
            "forgetting",
            "memory consolidation",
            "memory retrieval",
        ],
        "perceptual": [
            "perceptual learning",
            "sensory plasticity",
            "visual learning",
            "auditory learning",
            "face recognition",
            "object recognition",
        ],
        "collective": [
            "swarm",
            "collective behavior",
            "organizational learning",
            "multi-agent",
            "particle swarm",
            "ant colony",
        ],
        "health": [
            "health behavior",
            "patient education",
            "medical training",
            "public health",
            "clinical",
            "health literacy",
        ],
    }
    scores = {c: sum(1 for k in kw if k in text) for c, kw in cat_kw.items()}
    scores[intended_cat] = scores.get(intended_cat, 0) + 5
    cat = max(scores, key=scores.get)

    sub_kw = {
        "theory": [
            "theory",
            "model",
            "framework",
            "formalism",
            "taxonomy",
            "conceptual",
        ],
        "mechanism": [
            "mechanism",
            "neural correlate",
            "process",
            "underlying",
            "pathway",
            "substrate",
        ],
        "method": [
            "method",
            "experiment",
            "measurement",
            "paradigm",
            "algorithm",
            "metric",
            "procedure",
        ],
        "application": [
            "application",
            "intervention",
            "applied",
            "real-world",
            "deploy",
            "clinical",
            "therapy",
        ],
        "development": [
            "developmental",
            "age",
            "child",
            "infant",
            "lifespan",
            "trajectory",
            "growth",
            "adolescent",
        ],
        "individual-differences": [
            "individual differences",
            "aptitude",
            "personality",
            "trait",
            "cognitive style",
        ],
        "technology": [
            "VR",
            "virtual reality",
            "augmented reality",
            "brain-computer",
            "platform",
            "tool",
            "software",
            "app",
        ],
        "review": [
            "survey",
            "review",
            "meta-analysis",
            "bibliometric",
            "systematic",
            "literature",
        ],
    }
    sub_scores = {s: sum(1 for k in kw if k in text) for s, kw in sub_kw.items()}
    sub_scores[intended_sub] = sub_scores.get(intended_sub, 0) + 5
    sub = max(sub_scores, key=sub_scores.get)

    return cat, sub


def main():
    data, papers, by_id, titles_lower = load()
    print(f"Loaded {len(papers)} papers", flush=True)

    existing_cells = defaultdict(set)
    for p in papers:
        existing_cells[p["category"]].add(p["subcategory"])

    # Filter arXiv queries to only empty cells
    arxiv_active = [
        (c, s, q) for c, s, q in ARXIV_QUERIES if s not in existing_cells.get(c, set())
    ]
    print(f"\narXiv: {len(arxiv_active)} targeted queries for empty cells", flush=True)

    total_new = 0
    seen_ids = set()
    seen_titles = set(titles_lower)

    # --- arXiv pass ---
    for qi, (cat, sub, query) in enumerate(arxiv_active):
        # Re-check if cell was filled by previous queries
        if sub in existing_cells.get(cat, set()):
            continue
        print(f"\n[arXiv {qi + 1}/{len(arxiv_active)}] {cat}/{sub}", flush=True)
        entries = search_arxiv(query)
        print(f"  {len(entries)} entries", flush=True)

        for e in entries:
            m = re.search(r"(\d{4}\.\d{4,5})", e.get("url", ""))
            aid = m.group(1) if m else None
            if aid and (aid in by_id or aid in seen_ids):
                continue
            tl = e["title"].lower().strip()
            if tl in seen_titles:
                continue
            if any(similar(tl, t) for t in titles_lower):
                continue

            ec, es = classify(e["title"], e.get("abstract", ""), cat, sub)
            np = {
                "title": e["title"],
                "date": e.get("date", ""),
                "url": e["url"],
                "category": ec,
                "subcategory": es,
                "authors": [],
                "venue": "",
                "code_url": "",
                "project_url": "",
                "abstract": e.get("abstract", ""),
                "tags": [f"auto-{ec}"],
            }
            if aid:
                seen_ids.add(aid)
                by_id[aid] = np
            seen_titles.add(tl)
            titles_lower.append(tl)
            papers.append(np)
            total_new += 1
            existing_cells[ec].add(es)

        time.sleep(API_DELAY)

        save(data, papers)
        if (qi + 1) % 5 == 0:
            print(
                f"  [checkpoint {qi + 1}/{len(arxiv_active)}] saved {len(papers)} papers, +{total_new} new so far",
                flush=True,
            )

    print(f"\nAfter arXiv pass: {len(papers)} total, +{total_new} new", flush=True)

    # --- Semantic Scholar pass for hard disciplines ---
    s2_new = 0
    for (cat, sub), queries in S2_QUERIES_BY_CELL.items():
        if sub in existing_cells.get(cat, set()):
            continue
        for q in queries:
            if sub in existing_cells.get(cat, set()):
                break
            print(f"\n[S2] {cat}/{sub}: {q[:60]}...", flush=True)
            entries = search_s2(q)
            print(f"  {len(entries)} entries", flush=True)

            for e in entries:
                tl = e["title"].lower().strip()
                if tl in seen_titles:
                    continue
                if any(similar(tl, t) for t in titles_lower):
                    continue

                ec, es = classify(e["title"], e.get("abstract", ""), cat, sub)
                np = {
                    "title": e["title"],
                    "date": e.get("date", ""),
                    "url": e["url"],
                    "category": ec,
                    "subcategory": es,
                    "authors": [],
                    "venue": e.get("venue", ""),
                    "code_url": "",
                    "project_url": "",
                    "abstract": e.get("abstract", ""),
                    "tags": [f"auto-{ec}"],
                }
                seen_titles.add(tl)
                titles_lower.append(tl)
                papers.append(np)
                s2_new += 1
                total_new += 1
                existing_cells[ec].add(es)

            time.sleep(API_DELAY)

        save(data, papers)

    save(data, papers)

    print(f"\n[S2 pass complete] +{s2_new} new papers", flush=True)
    print(f"\n{'=' * 60}", flush=True)
    print(f"Final: {len(papers)} papers (+{total_new} new)", flush=True)

    filled_cells = sum(
        1
        for c in VALID_CATEGORIES
        for a in ASPECTS
        if existing_cells.get(c) and a in existing_cells[c]
    )
    print(f"Cells: {filled_cells}/{len(VALID_CATEGORIES) * len(ASPECTS)}", flush=True)

    for cat in sorted(VALID_CATEGORIES):
        empty = [a for a in ASPECTS if a not in existing_cells.get(cat, set())]
        filled = len(ASPECTS) - len(empty)
        count = sum(1 for p in papers if p.get("category") == cat)
        status = "FULL" if not empty else f"missing {', '.join(empty)}"
        print(f"  {cat:30s} {filled:2d}/8 {count:5d} papers  [{status}]", flush=True)


if __name__ == "__main__":
    main()
