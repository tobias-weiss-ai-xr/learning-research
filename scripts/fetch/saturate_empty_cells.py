#!/usr/bin/env python3
"""Targeted saturation: fill empty (category, subcategory) cells.

arXiv coverage is limited for non-CS disciplines, so this script uses
targeted multi-category queries with subcategory-biased classification.
"""

import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone, timedelta
from difflib import SequenceMatcher
from pathlib import Path

import requests
import yaml

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
ARXIV_SEARCH_API = (
    "http://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
)
API_DELAY = 3
MAX_RESULTS_PER_QUERY = 100
MONTHS_BACK = 48
CHECKPOINT_INTERVAL = 10
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

VALID_SUBCATEGORIES = {
    "theory",
    "mechanism",
    "method",
    "application",
    "development",
    "individual-differences",
    "technology",
    "review",
}

# Targeted queries: each entry is (category, subcategory-bias, arxiv-query)
# The subcategory-bias helps the classifier prefer that subcategory
TARGETED_QUERIES = [
    # ---- animal-learning: fill mechanism, method, application, development, individual-differences, technology, review ----
    (
        "animal-learning",
        "mechanism",
        'cat:q-bio.NC AND abs:"animal learning" AND abs:"neural"',
    ),
    (
        "animal-learning",
        "mechanism",
        'cat:q-bio.NC AND abs:"animal cognition" AND abs:"brain"',
    ),
    (
        "animal-learning",
        "method",
        'cat:q-bio.PE AND abs:"animal" AND abs:"learning" AND abs:"experiment"',
    ),
    (
        "animal-learning",
        "application",
        'cat:cs.RO AND abs:"robot" AND abs:"animal" AND abs:"inspired"',
    ),
    (
        "animal-learning",
        "development",
        'cat:q-bio.NC AND abs:"developmental" AND abs:"animal" AND abs:"learning"',
    ),
    (
        "animal-learning",
        "individual-differences",
        'all:"individual differences" AND abs:"animal" AND abs:"cognition"',
    ),
    (
        "animal-learning",
        "technology",
        'cat:cs.ET AND abs:"animal" AND abs:"tracking" AND abs:"learning"',
    ),
    # ---- collective: fill mechanism-vs-review ----
    (
        "collective",
        "mechanism",
        'cat:cs.MA AND abs:"multi-agent" AND abs:"coordination" AND abs:"learning"',
    ),
    (
        "collective",
        "mechanism",
        'cat:cs.SI AND abs:"swarm" AND abs:"algorithm" AND abs:"learning"',
    ),
    (
        "collective",
        "method",
        'cat:cs.SI AND abs:"swarm" AND abs:"optimization" AND abs:"method"',
    ),
    ("collective", "method", 'all:"collective" AND abs:"decision" AND abs:"algorithm"'),
    (
        "collective",
        "application",
        'cat:cs.RO AND abs:"swarm robotics" AND abs:"application"',
    ),
    (
        "collective",
        "application",
        'cat:cs.CY AND abs:"crowdsourcing" AND abs:"learning"',
    ),
    (
        "collective",
        "development",
        'all:"collective" AND abs:"emergence" AND abs:"learning"',
    ),
    (
        "collective",
        "individual-differences",
        'all:"heterogeneous" AND abs:"multi-agent" AND abs:"learning"',
    ),
    (
        "collective",
        "technology",
        'cat:cs.DC AND abs:"distributed" AND abs:"learning" AND abs:"system"',
    ),
    (
        "collective",
        "review",
        'all:"swarm intelligence" AND abs:"survey" AND abs:"learning"',
    ),
    # ---- educational-psychology: fill mechanism-vs-review ----
    (
        "educational-psychology",
        "mechanism",
        'cat:q-bio.NC AND abs:"motivation" AND abs:"neural" AND abs:"learning"',
    ),
    (
        "educational-psychology",
        "method",
        'cat:cs.CY AND abs:"self-regulated" AND abs:"learning" AND abs:"measure"',
    ),
    (
        "educational-psychology",
        "application",
        'cat:cs.CY AND abs:"classroom" AND abs:"motivation" AND abs:"intervention"',
    ),
    (
        "educational-psychology",
        "development",
        'all:"achievement" AND abs:"motivation" AND abs:"development"',
    ),
    (
        "educational-psychology",
        "individual-differences",
        'all:"self-efficacy" AND abs:"academic" AND abs:"achievement"',
    ),
    (
        "educational-psychology",
        "technology",
        'cat:cs.HC AND abs:"learning" AND abs:"engagement" AND abs:"system"',
    ),
    (
        "educational-psychology",
        "review",
        'all:"self-regulation" AND abs:"learning" AND abs:"review"',
    ),
    # ---- health: fill mechanism-vs-review ----
    (
        "health",
        "mechanism",
        'cat:q-bio.NC AND abs:"health" AND abs:"behavior" AND abs:"neural"',
    ),
    (
        "health",
        "mechanism",
        'cat:q-bio.NC AND abs:"aging" AND abs:"cognition" AND abs:"plasticity"',
    ),
    (
        "health",
        "method",
        'cat:cs.CY AND abs:"health" AND abs:"intervention" AND abs:"method"',
    ),
    (
        "health",
        "method",
        'cat:stat.ME AND abs:"clinical" AND abs:"learning" AND abs:"trial"',
    ),
    (
        "health",
        "application",
        'cat:cs.CY AND abs:"health" AND abs:"education" AND abs:"patient"',
    ),
    (
        "health",
        "application",
        'cat:cs.AI AND abs:"clinical" AND abs:"decision" AND abs:"learning"',
    ),
    (
        "health",
        "development",
        'all:"health" AND abs:"lifespan" AND abs:"learning" AND abs:"aging"',
    ),
    (
        "health",
        "individual-differences",
        'all:"health literacy" AND abs:"individual" AND abs:"difference"',
    ),
    (
        "health",
        "technology",
        'cat:cs.HC AND abs:"health" AND abs:"app" AND abs:"learning"',
    ),
    (
        "health",
        "technology",
        'cat:cs.CY AND abs:"digital health" AND abs:"learning" AND abs:"platform"',
    ),
    ("health", "review", 'all:"public health" AND abs:"learning" AND abs:"review"'),
    # ---- perceptual: fill mechanism-vs-review ----
    (
        "perceptual",
        "mechanism",
        'cat:q-bio.NC AND abs:"perceptual" AND abs:"plasticity" AND abs:"cortex"',
    ),
    (
        "perceptual",
        "mechanism",
        'cat:q-bio.NC AND abs:"sensory" AND abs:"adaptation" AND abs:"neural"',
    ),
    (
        "perceptual",
        "method",
        'cat:cs.CV AND abs:"visual" AND abs:"recognition" AND abs:"method"',
    ),
    (
        "perceptual",
        "application",
        'cat:cs.HC AND abs:"perceptual" AND abs:"training" AND abs:"interface"',
    ),
    (
        "perceptual",
        "development",
        'all:"perceptual" AND abs:"development" AND abs:"visual" AND abs:"child"',
    ),
    (
        "perceptual",
        "individual-differences",
        'all:"perceptual" AND abs:"ability" AND abs:"individual" AND abs:"difference"',
    ),
    (
        "perceptual",
        "technology",
        'cat:cs.HC AND abs:"visualization" AND abs:"learning" AND abs:"perception"',
    ),
    ("perceptual", "review", 'all:"perceptual learning" AND abs:"review"'),
    # ---- memory-science: fill mechanism, application, development, individual-differences, technology, review ----
    (
        "memory-science",
        "mechanism",
        'cat:q-bio.NC AND abs:"memory" AND abs:"consolidation" AND abs:"neural"',
    ),
    (
        "memory-science",
        "mechanism",
        'cat:q-bio.NC AND abs:"memory" AND abs:"synaptic" AND abs:"plasticity"',
    ),
    (
        "memory-science",
        "application",
        'cat:cs.HC AND abs:"memory" AND abs:"training" AND abs:"intervention"',
    ),
    (
        "memory-science",
        "development",
        'all:"memory" AND abs:"development" AND abs:"child" AND abs:"learning"',
    ),
    (
        "memory-science",
        "individual-differences",
        'all:"working memory" AND abs:"individual differences"',
    ),
    (
        "memory-science",
        "technology",
        'cat:cs.HC AND abs:"memory" AND abs:"assistive" AND abs:"technology"',
    ),
    ("memory-science", "review", 'all:"memory" AND abs:"systems" AND abs:"review"'),
    # ---- neuroscience: fill development, individual-differences, review ----
    (
        "neuroscience",
        "development",
        'cat:q-bio.NC AND abs:"developmental" AND abs:"neuroscience" AND abs:"learning"',
    ),
    (
        "neuroscience",
        "individual-differences",
        'cat:q-bio.NC AND abs:"individual" AND abs:"brain" AND abs:"learning"',
    ),
    (
        "neuroscience",
        "review",
        'cat:q-bio.NC AND abs:"neuroscience" AND abs:"learning" AND abs:"review"',
    ),
    # ---- Single-cell gaps ----
    (
        "developmental",
        "review",
        'all:"child development" AND abs:"review" AND abs:"learning"',
    ),
    (
        "emotion",
        "development",
        'all:"emotion" AND abs:"development" AND abs:"learning" AND abs:"child"',
    ),
    (
        "evolutionary",
        "individual-differences",
        'all:"evolutionary" AND abs:"individual differences" AND abs:"cognition"',
    ),
    ("motor", "review", 'all:"motor learning" AND abs:"review"'),
    (
        "neuromorphic",
        "development",
        'all:"neuromorphic" AND abs:"development" AND abs:"learning"',
    ),
    (
        "philosophy-of-mind",
        "development",
        'all:"philosophy" AND abs:"mind" AND abs:"development" AND abs:"learning"',
    ),
    (
        "social-learning",
        "development",
        'all:"social learning" AND abs:"development" AND abs:"child"',
    ),
]


def load_existing(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
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
    return data, papers, by_id, titles_lower


def title_similarity(a, b, threshold=0.75):
    a_clean = re.sub(r"[^\w\s]", "", a.lower())
    b_clean = re.sub(r"[^\w\s]", "", b.lower())
    return SequenceMatcher(None, a_clean, b_clean).ratio() >= threshold


def search_arxiv(query):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=MONTHS_BACK * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"
    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(
                ARXIV_SEARCH_API.format(
                    requests.utils.quote(full_query), 0, MAX_RESULTS_PER_QUERY
                ),
                timeout=60,
            )
            if resp.status_code == 429:
                wait = 10 * (2**attempt)
                print(
                    f"  RATE LIMITED (429), retrying in {wait}s (attempt {attempt + 1}/{MAX_RETRIES})",
                    flush=True,
                )
                time.sleep(wait)
                continue
            resp.raise_for_status()
            entries = []
            for match in re.finditer(r"<entry>(.*?)</entry>", resp.text, re.DOTALL):
                xml = match.group(1)
                entry = {}
                title_m = re.search(r"<title>(.*?)</title>", xml, re.DOTALL)
                if title_m:
                    entry["title"] = re.sub(r"\s+", " ", title_m.group(1).strip())
                id_m = re.search(r"<id>(.*?)</id>", xml)
                if id_m:
                    entry["url"] = id_m.group(1).strip().replace("http://", "https://")
                published_m = re.search(r"<published>(.*?)</published>", xml)
                if published_m:
                    entry["date"] = published_m.group(1).strip()[:7]
                summary_m = re.search(r"<summary>(.*?)</summary>", xml, re.DOTALL)
                if summary_m:
                    entry["abstract"] = re.sub(r"\s+", " ", summary_m.group(1).strip())
                if entry.get("title") and entry.get("url"):
                    entries.append(entry)
            return entries
        except requests.exceptions.Timeout:
            wait = 10 * (2**attempt)
            print(
                f"  TIMEOUT, retrying in {wait}s (attempt {attempt + 1}/{MAX_RETRIES})",
                flush=True,
            )
            time.sleep(wait)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 5 * (2**attempt)
                print(
                    f"  ERROR: {e}, retrying in {wait}s (attempt {attempt + 1}/{MAX_RETRIES})",
                    flush=True,
                )
                time.sleep(wait)
            else:
                print(
                    f"  WARNING: arXiv search failed after {MAX_RETRIES} attempts: {e}",
                    flush=True,
                )
                return []
    return []


def classify_with_bias(title, abstract, intended_cat, intended_sub):
    text = f"{title} {abstract}".lower()

    cat_keywords = {
        "cognitive-science": [
            "cognitive science",
            "mental model",
            "attention",
            "decision making",
            "working memory",
            "cognitive load",
            "executive function",
            "metacognition",
        ],
        "neuroscience": [
            "synaptic",
            "neural plasticity",
            "dopamine",
            "hippocampus",
            "brain plasticity",
            "cortical",
            "prefrontal",
            "basal ganglia",
        ],
        "education": [
            "pedagogy",
            "instructional",
            "classroom",
            "educational technology",
            "assessment",
            "intelligent tutoring",
            "mooc",
            "e-learning",
        ],
        "developmental": [
            "child development",
            "language acquisition",
            "cognitive development",
            "infant",
            "lifespan",
            "preschool",
            "adolescent",
        ],
        "behavioral": [
            "behavioral economics",
            "habit",
            "conditioning",
            "reinforcement",
            "behavior change",
            "operant",
            "classical conditioning",
        ],
        "social-learning": [
            "social learning",
            "observational learning",
            "cultural transmission",
            "peer learning",
            "collaborative learning",
            "imitation",
        ],
        "language": [
            "language learning",
            "linguistic",
            "bilingual",
            "literacy",
            "speech",
            "phonological",
            "syntax",
            "vocabulary",
        ],
        "motor": [
            "motor learning",
            "skill acquisition",
            "procedural memory",
            "embodied",
            "sensorimotor",
            "motor control",
        ],
        "emotion": [
            "emotional learning",
            "affective",
            "emotion regulation",
            "fear",
            "anxiety",
            "stress",
            "sentiment",
        ],
        "creative": [
            "creativity",
            "creative cognition",
            "artistic",
            "divergent thinking",
            "innovation",
            "design thinking",
        ],
        "machine-learning": [
            "deep learning",
            "supervised",
            "reinforcement learning",
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
            "spatial learning",
            "animal conditioning",
            "primate",
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
        ],
        "collective": [
            "swarm intelligence",
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

    scores = {}
    for cat, keywords in cat_keywords.items():
        scores[cat] = sum(1 for k in keywords if k in text)

    if intended_cat in scores:
        scores[intended_cat] += 3  # strong bias

    category = max(scores, key=scores.get) if any(scores.values()) else intended_cat

    sub_keywords = {
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
            "biological",
            "substrate",
            "pathway",
        ],
        "method": [
            "method",
            "experiment",
            "measurement",
            "paradigm",
            "algorithm",
            "procedure",
            "metric",
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
            "cognitive style",
            "intelligence",
            "trait",
        ],
        "technology": [
            "VR",
            "virtual reality",
            "augmented reality",
            "brain-computer",
            "platform",
            "tool",
            "software",
            "system",
            "app",
        ],
        "review": [
            "survey",
            "review",
            "meta-analysis",
            "bibliometric",
            "systematic review",
            "literature",
        ],
    }

    sub_scores = {}
    for sub, keywords in sub_keywords.items():
        sub_scores[sub] = sum(1 for k in keywords if k in text)

    if intended_sub in sub_scores:
        sub_scores[intended_sub] += 3

    subcategory = (
        max(sub_scores, key=sub_scores.get) if any(sub_scores.values()) else "theory"
    )
    return category, subcategory


def save_papers(yaml_path, data, papers):
    data["papers"] = papers
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


def main():
    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    data, papers, by_id, titles_lower = load_existing(yaml_path)

    # Pre-check: which cells are already filled?
    from collections import defaultdict

    existing_cells = defaultdict(set)
    for p in papers:
        existing_cells[p["category"]].add(p["subcategory"])

    # Filter: only run queries for cells that are still empty
    active_queries = []
    for cat, sub, query in TARGETED_QUERIES:
        if sub not in existing_cells.get(cat, set()):
            active_queries.append((cat, sub, query))

    print(f"Loaded {len(papers)} existing papers", flush=True)
    print(
        f"Total targeted queries: {len(active_queries)} (filtered from {len(TARGETED_QUERIES)})",
        flush=True,
    )
    print(f"Empty cells to fill: {len(active_queries)}", flush=True)
    print(f"Search window: {MONTHS_BACK} months", flush=True)

    total_new = 0
    cat_new = Counter()
    subcat_new = Counter()
    seen_ids = set()
    seen_titles = set(titles_lower)

    for qi, (intended_cat, intended_sub, query) in enumerate(active_queries):
        short_q = query[:65]
        print(
            f"\n[{qi + 1}/{len(active_queries)}] {intended_cat}/{intended_sub}: {short_q}...",
            flush=True,
        )

        entries = search_arxiv(query)
        print(f"  arXiv returned {len(entries)} entries", flush=True)

        query_new = 0
        for entry in entries:
            arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None

            if arxiv_id and (arxiv_id in by_id or arxiv_id in seen_ids):
                continue

            title = entry.get("title", "")
            title_lower = title.lower().strip()

            if title_lower in seen_titles:
                continue

            # Check for title similarity
            dedup = False
            for existing in seen_titles:
                if title_similarity(title_lower, existing):
                    dedup = True
                    break
            if dedup:
                continue

            abstract = entry.get("abstract", "")
            category, subcategory = classify_with_bias(
                title, abstract, intended_cat, intended_sub
            )

            new_paper = {
                "title": title,
                "date": entry.get("date", ""),
                "url": entry.get("url", ""),
                "category": category,
                "subcategory": subcategory,
                "authors": [],
                "venue": "",
                "code_url": "",
                "project_url": "",
                "abstract": abstract,
                "tags": [f"auto-{category}"],
            }

            if arxiv_id:
                seen_ids.add(arxiv_id)
                by_id[arxiv_id] = new_paper
            seen_titles.add(title_lower)
            titles_lower.append(title_lower)
            papers.append(new_paper)
            total_new += 1
            query_new += 1
            cat_new[category] += 1
            subcat_new[subcategory] += 1

        print(f"  +{query_new} new", flush=True)
        time.sleep(API_DELAY)

        if (qi + 1) % CHECKPOINT_INTERVAL == 0:
            save_papers(yaml_path, data, papers)
            print(f"  [checkpoint] saved {len(papers)} papers", flush=True)

    save_papers(yaml_path, data, papers)

    cat_counter = Counter()
    sub_counter = Counter()
    cell_counter = Counter()
    for p in papers:
        cat_counter[p["category"]] += 1
        sub_counter[p["subcategory"]] += 1
        cell_counter[(p["category"], p["subcategory"])] += 1

    print(f"\n{'=' * 60}", flush=True)
    print("RESULTS", flush=True)
    print(f"{'=' * 60}", flush=True)
    print(f"Total papers: {len(papers)}", flush=True)
    print(f"New papers added: {total_new}", flush=True)

    print(f"\nCell coverage:", flush=True)
    aspects = [
        "theory",
        "mechanism",
        "method",
        "application",
        "development",
        "individual-differences",
        "technology",
        "review",
    ]
    for cat in sorted(VALID_CATEGORIES):
        filled = [a for a in aspects if cell_counter.get((cat, a), 0) > 0]
        empty = [a for a in aspects if cell_counter.get((cat, a), 0) == 0]
        print(
            f"  {cat:30s} {len(filled):2d}/8 cells, {cat_counter[cat]:5d} papers",
            flush=True,
        )
        if empty:
            print(f"  {'':30s} STILL EMPTY: {', '.join(empty)}", flush=True)

    if all(cell_counter.get((c, a), 0) > 0 for c in VALID_CATEGORIES for a in aspects):
        print("\nALL 160 cells populated!", flush=True)
    else:
        total_cells = len(VALID_CATEGORIES) * len(aspects)
        filled_cells = sum(
            1
            for c in VALID_CATEGORIES
            for a in aspects
            if cell_counter.get((c, a), 0) > 0
        )
        print(f"\n{filled_cells}/{total_cells} cells populated", flush=True)


if __name__ == "__main__":
    main()
