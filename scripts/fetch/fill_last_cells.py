#!/usr/bin/env python3
"""S2-only pass: fill last 6 empty cells."""

import re, sys, time, json
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import requests, yaml

YAML_PATH = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
API_DELAY = 2

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

# Only the last 6 cells that arXiv couldn't fill
LAST_CELLS = {
    ("animal-learning", "individual-differences"): [
        "individual differences in animal cognition",
        "animal intelligence individual variation",
    ],
    ("evolutionary", "individual-differences"): [
        "evolutionary psychology individual differences",
        "evolution personality individual differences",
    ],
    ("memory-science", "application"): [
        "memory training intervention cognitive",
        "memory rehabilitation clinical",
        "working memory training program",
    ],
    ("memory-science", "development"): [
        "memory development childhood adolescence",
        "working memory development lifespan",
        "memory cognitive development children",
    ],
    ("perceptual", "application"): [
        "perceptual learning real world application",
        "perceptual training clinical application",
        "visual perceptual learning training",
    ],
    ("perceptual", "review"): [
        "perceptual learning review survey",
        "visual perceptual learning review",
        "perceptual expertise review survey",
    ],
}


def similar(a, b):
    return (
        SequenceMatcher(
            None, re.sub(r"[^\w\s]", "", a.lower()), re.sub(r"[^\w\s]", "", b.lower())
        ).ratio()
        >= 0.75
    )


def search_s2(query, limit=100):
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,url,year,abstract,venue",
    }
    for attempt in range(5):
        try:
            resp = requests.get(
                S2_API,
                params=params,
                timeout=30,
                headers={"User-Agent": "LearningResearch/1.0"},
            )
            if resp.status_code == 429:
                time.sleep(10 * (2**attempt))
                continue
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "title": p.get("title", ""),
                    "url": p.get("url", "")
                    or f"https://api.semanticscholar.org/CorpusID:{p.get('paperId', '')}",
                    "date": str(p.get("year", "")),
                    "abstract": p.get("abstract", "") or "",
                    "venue": p.get("venue", ""),
                }
                for p in data.get("data", [])
                if p.get("title")
            ]
        except Exception as e:
            if attempt < 4:
                time.sleep(5 * (2**attempt))
            else:
                print(f"  S2 error: {e}")
                return []
    return []


def classify(title, abstract, icat, isub):
    text = f"{title} {abstract}".lower()
    kw = {
        "animal-learning": [
            "animal cognition",
            "animal intelligence",
            "animal learning",
            "foraging",
            "primate",
        ],
        "evolutionary": [
            "evolution",
            "evolutionary psychology",
            "natural selection",
            "adaptation",
            "phylogenetic",
        ],
        "memory-science": [
            "memory",
            "episodic",
            "semantic",
            "working memory",
            "recall",
            "recognition",
            "forgetting",
        ],
        "perceptual": [
            "perceptual",
            "visual learning",
            "auditory",
            "face recognition",
            "object recognition",
            "sensory",
        ],
        "cognitive-science": [
            "cognitive",
            "mental model",
            "attention",
            "decision",
            "reasoning",
        ],
        "neuroscience": ["synaptic", "neural", "brain", "hippocampus", "fMRI"],
        "education": ["education", "pedagogy", "classroom", "tutoring", "assessment"],
        "motor": ["motor", "skill acquisition", "procedural", "embodied"],
        "emotion": ["emotion", "affective", "fear", "anxiety", "sentiment"],
        "creative": ["creativity", "creative", "artistic", "innovation"],
        "machine-learning": [
            "deep learning",
            "reinforcement",
            "supervised",
            "transformer",
            "neural network",
        ],
        "philosophy-of-mind": [
            "epistemology",
            "consciousness",
            "mental representation",
        ],
        "collective": ["swarm", "collective", "organizational", "multi-agent"],
        "health": ["health", "clinical", "patient", "medical training"],
        "social-learning": ["social learning", "observational", "imitation"],
        "language": ["language", "linguistic", "bilingual", "literacy"],
        "developmental": ["child development", "infant", "lifespan"],
        "behavioral": ["behavioral", "habit", "conditioning", "reinforcement"],
        "educational-psychology": ["motivation", "self-regulation", "mindset"],
        "neuromorphic": ["neuromorphic", "spiking", "brain-inspired"],
    }
    scores = {c: sum(1 for k in kw.get(c, []) if k in text) for c in VALID_CATEGORIES}
    scores[icat] = scores.get(icat, 0) + 5
    cat = max(scores, key=scores.get)

    sub_kw = {
        "theory": ["theory", "model", "framework", "conceptual"],
        "mechanism": ["mechanism", "neural", "process", "pathway"],
        "method": ["method", "experiment", "algorithm", "metric"],
        "application": [
            "application",
            "intervention",
            "training",
            "real-world",
            "clinical",
            "therapy",
            "program",
        ],
        "development": [
            "development",
            "child",
            "adolescent",
            "lifespan",
            "age",
            "trajectory",
            "growth",
        ],
        "individual-differences": [
            "individual differences",
            "personality",
            "trait",
            "aptitude",
            "intelligence",
            "variation",
        ],
        "technology": ["technology", "VR", "virtual", "app", "software", "system"],
        "review": ["review", "survey", "meta-analysis", "systematic"],
    }
    sub_scores = {s: sum(1 for k in kw if k in text) for s, kw in sub_kw.items()}
    sub_scores[isub] = sub_scores.get(isub, 0) + 5
    sub = max(sub_scores, key=sub_scores.get)
    return cat, sub


def main():
    with open(YAML_PATH) as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    titles_lower = [p.get("title", "").lower().strip() for p in papers]
    seen_titles = set(titles_lower)

    print(f"Loaded {len(papers)} papers", flush=True)

    total_new = 0
    for (cat, sub), queries in LAST_CELLS.items():
        # Check if cell already filled
        already = any(
            p.get("category") == cat and p.get("subcategory") == sub for p in papers
        )
        if already:
            print(f"{cat}/{sub} already filled, skipping", flush=True)
            continue

        for q in queries:
            print(f"\n[S2] {cat}/{sub}: {q[:50]}...", flush=True)
            entries = search_s2(q)
            print(f"  {len(entries)} entries", flush=True)

            for i, e in enumerate(entries):
                if i >= 200:  # cap per query to avoid timeout
                    break
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
                total_new += 1

                # Interim save every 50 papers
                if total_new % 50 == 0:
                    data["papers"] = papers
                    with open(YAML_PATH, "w", encoding="utf-8") as f:
                        yaml.dump(
                            data,
                            f,
                            default_flow_style=False,
                            allow_unicode=True,
                            sort_keys=False,
                        )
                    print(
                        f"  [checkpoint] saved {len(papers)} papers (+{total_new} new so far)",
                        flush=True,
                    )

            # Check if cell filled
            filled = any(
                p.get("category") == cat and p.get("subcategory") == sub for p in papers
            )
            if filled:
                print(f"  {cat}/{sub} filled!", flush=True)
                break

            time.sleep(API_DELAY)

        # Save after each cell
        data["papers"] = papers
        with open(YAML_PATH, "w", encoding="utf-8") as f:
            yaml.dump(
                data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
            )
        print(f"  saved ({len(papers)} papers)", flush=True)

    print(f"\nTotal new: {total_new}", flush=True)
    from collections import Counter

    subcnt = Counter((p["category"], p["subcategory"]) for p in papers)
    for c in sorted(VALID_CATEGORIES):
        empty = [a for a in ASPECTS if subcnt.get((c, a), 0) == 0]
        cnt = sum(1 for p in papers if p["category"] == c)
        print(
            f"  {c:30s} {cnt:5d} papers  {'FULL' if not empty else f'missing: {empty}'}"
        )


if __name__ == "__main__":
    main()
