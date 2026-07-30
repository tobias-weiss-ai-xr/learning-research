#!/usr/bin/env python3
"""Phase 3b: One category at a time, save to JSON after each, convert to YAML at end."""

import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
ARXIV_SEARCH_API = (
    "http://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
)
MAX_RESULTS_PER_QUERY = 100
MONTHS_BACK = 48

CATEGORY_BATCHES = {
    "perceptual": [
        'all:"perceptual learning" AND abs:"visual"',
        'all:"sensory plasticity" AND abs:"learning"',
        'all:"visual expertise" AND abs:"learning"',
        'all:"auditory learning"',
        'all:"perceptual" AND abs:"learning" AND abs:"plasticity"',
        'all:"visual learning" AND abs:"recognition"',
        'all:"face recognition" AND abs:"learning"',
        'all:"object recognition" AND abs:"learning"',
        'all:"speech perception" AND abs:"learning"',
        'all:"cross-modal" AND abs:"learning"',
        'all:"multisensory" AND abs:"learning"',
        'all:"texture discrimination" AND abs:"learning"',
        'all:"visual perceptual" AND abs:"learning"',
        'all:"audiovisual" AND abs:"learning"',
    ],
    "collective": [
        'all:"swarm intelligence" AND abs:"learning"',
        'all:"collective behavior" AND abs:"learning"',
        'all:"group decision" AND abs:"learning"',
        'all:"organizational learning"',
        'all:"ant colony" AND abs:"learning"',
        'all:"particle swarm" AND abs:"learning"',
        'all:"collective intelligence" AND abs:"learning"',
        'all:"flocking" AND abs:"learning"',
        'all:"distributed learning" AND abs:"system"',
        'all:"consensus" AND abs:"learning"',
        'all:"swarm robotics" AND abs:"learning"',
        'all:"social insect" AND abs:"learning"',
        'all:"information cascade" AND abs:"learning"',
    ],
    "health": [
        'all:"health behavior" AND abs:"learning"',
        'all:"patient education" AND abs:"learning"',
        'all:"medical training" AND abs:"learning"',
        'all:"public health" AND abs:"learning"',
        'all:"clinical" AND abs:"learning" AND abs:"AI"',
        'all:"health literacy" AND abs:"learning"',
        'all:"digital health" AND abs:"learning"',
        'all:"rehabilitation" AND abs:"learning"',
        'all:"sleep" AND abs:"learning" AND abs:"memory"',
        'all:"nutrition" AND abs:"cognition" AND abs:"learning"',
        'all:"exercise" AND abs:"cognition" AND abs:"learning"',
        'all:"aging" AND abs:"cognition" AND abs:"learning"',
        'all:"dementia" AND abs:"learning" AND abs:"cognition"',
        'all:"chronic disease" AND abs:"learning"',
    ],
    "animal-learning": [
        'all:"animal cognition" AND abs:"learning"',
        'all:"animal memory" AND abs:"learning"',
        'all:"animal navigation" AND abs:"learning"',
        'all:"tool use" AND abs:"animal" AND abs:"learning"',
        'all:"animal" AND abs:"conditioning" AND abs:"learning"',
        'all:"spatial learning" AND abs:"animal"',
        'all:"foraging" AND abs:"learning" AND abs:"animal"',
        'all:"bird song" AND abs:"learning"',
        'all:"habituation" AND abs:"animal"',
        'all:"animal communication" AND abs:"learning"',
        'all:"primate" AND abs:"cognition" AND abs:"learning"',
        'all:"rat" AND abs:"maze" AND abs:"learning"',
        'all:"bee" AND abs:"learning"',
        'all:"octopus" AND abs:"learning"',
    ],
    "educational-psychology": [
        'all:"educational psychology" AND abs:"learning"',
        'all:"growth mindset" AND abs:"learning"',
        'all:"self-regulation" AND abs:"learning"',
        'all:"motivation" AND abs:"learning"',
        'all:"scaffolding" AND abs:"learning"',
        'all:"zone of proximal" AND abs:"learning"',
        'all:"self-efficacy" AND abs:"learning"',
        'all:"cognitive apprenticeship"',
        'all:"constructivism" AND abs:"learning"',
        'all:"achievement motivation" AND abs:"learning"',
        'all:"engagement" AND abs:"learning" AND abs:"student"',
        'all:"academic achievement" AND abs:"learning"',
        'all:"mastery learning"',
        'all:"cognitive strategy" AND abs:"learning"',
    ],
}

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


def search_arxiv(query, retries=3):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=MONTHS_BACK * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"
    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"
    for attempt in range(retries):
        try:
            resp = requests.get(
                ARXIV_SEARCH_API.format(
                    requests.utils.quote(full_query), 0, MAX_RESULTS_PER_QUERY
                ),
                timeout=30,
            )
            if resp.status_code == 429:
                time.sleep(30 * (attempt + 1))
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
        except Exception as e:
            print(f"  Error: {e}", flush=True)
            time.sleep(15)
    return []


def classify_paper(title, abstract, intended_category):
    text = f"{title} {abstract}".lower()
    cat_keywords = {
        "cognitive-science": [
            "cognitive science",
            "mental model",
            "attention",
            "decision making",
            "working memory",
            "cognitive load",
            "metacognition",
        ],
        "neuroscience": [
            "neuroscience",
            "synaptic",
            "neural plasticity",
            "dopamine",
            "hippocampus",
            "cortical plasticity",
            "neurotransmitter",
            "spike-timing",
        ],
        "education": [
            "pedagogy",
            "instructional design",
            "classroom",
            "educational technology",
            "assessment",
            "intelligent tutoring",
            "learning analytics",
            "adaptive learning",
        ],
        "developmental": [
            "child development",
            "language acquisition",
            "cognitive development",
            "infant",
            "lifespan",
            "developmental psychology",
        ],
        "behavioral": [
            "behavioral economics",
            "habit formation",
            "operant conditioning",
            "classical conditioning",
            "behavior modification",
            "reward learning",
            "behavior change",
        ],
        "social-learning": [
            "social learning",
            "observational learning",
            "cultural transmission",
            "peer learning",
            "collaborative learning",
            "cooperative learning",
        ],
        "language": [
            "language learning",
            "linguistic",
            "bilingual",
            "literacy",
            "speech",
            "second language",
            "phonological",
            "morphological",
            "syntax",
            "vocabulary",
        ],
        "motor": [
            "motor learning",
            "skill acquisition",
            "procedural memory",
            "embodied cognition",
            "sports",
            "sensorimotor",
            "motor control",
        ],
        "emotion": [
            "emotional learning",
            "affective neuroscience",
            "emotion regulation",
            "stress",
            "affective",
            "anxiety",
            "well-being",
            "sentiment",
        ],
        "creative": [
            "creativity",
            "creative cognition",
            "artistic",
            "divergent thinking",
            "creative process",
            "innovation",
            "design thinking",
        ],
        "machine-learning": [
            "deep learning",
            "supervised learning",
            "reinforcement learning",
            "self-supervised",
            "meta-learning",
            "neural network",
            "gradient",
            "backpropagation",
            "continual learning",
            "transfer learning",
            "federated learning",
            "contrastive learning",
            "representation learning",
            "in-context learning",
            "transformer",
        ],
        "evolutionary": [
            "evolution cognition",
            "comparative cognition",
            "animal intelligence",
            "cultural evolution",
            "evolutionary learning",
        ],
        "philosophy-of-mind": [
            "epistemology",
            "consciousness",
            "mental representation",
            "phenomenology",
            "philosophy of cognition",
            "rationalism",
            "empiricism",
        ],
        "educational-psychology": [
            "motivation",
            "self-regulation",
            "growth mindset",
            "zone of proximal",
            "scaffolding",
            "self-efficacy",
            "cognitive apprenticeship",
            "constructivism",
            "achievement motivation",
            "student engagement",
            "academic achievement",
            "educational psychology",
            "mastery learning",
        ],
        "animal-learning": [
            "animal cognition",
            "animal memory",
            "animal navigation",
            "tool use",
            "animal conditioning",
            "spatial learning",
            "foraging",
            "bird song",
            "habituation",
            "animal communication",
            "primate cognition",
        ],
        "neuromorphic": [
            "neuromorphic",
            "spiking neural",
            "brain-inspired computing",
            "event-driven neural",
            "memristor",
            "spike-timing dependent",
        ],
        "memory-science": [
            "episodic memory",
            "semantic memory",
            "procedural memory",
            "forgetting",
            "memory systems",
            "memory consolidation",
            "memory retrieval",
            "memory formation",
            "recognition memory",
            "reconsolidation",
            "long-term memory",
        ],
        "perceptual": [
            "perceptual learning",
            "sensory plasticity",
            "visual learning",
            "auditory learning",
            "visual expertise",
            "face recognition",
            "object recognition",
            "speech perception",
            "cross-modal learning",
            "multisensory learning",
            "texture discrimination",
            "audiovisual",
        ],
        "collective": [
            "swarm intelligence",
            "collective behavior",
            "group decision",
            "organizational learning",
            "ant colony",
            "particle swarm",
            "collective intelligence",
            "flocking",
            "consensus",
            "distributed learning",
            "social insect",
            "information cascade",
        ],
        "health": [
            "health behavior",
            "patient education",
            "medical training",
            "public health",
            "clinical learning",
            "health literacy",
            "digital health",
            "rehabilitation",
            "sleep",
            "nutrition",
            "exercise",
            "aging cognition",
            "dementia",
            "chronic disease",
        ],
    }
    scores = {}
    for cat, keywords in cat_keywords.items():
        scores[cat] = sum(1 for k in keywords if k in text)
    if intended_category and intended_category in scores:
        scores[intended_category] += 2
    if not any(scores.values()):
        return (
            intended_category
            if intended_category in VALID_CATEGORIES
            else "machine-learning",
            "theory",
        )
    category = max(scores, key=scores.get)
    if category not in VALID_CATEGORIES:
        category = (
            intended_category
            if intended_category in VALID_CATEGORIES
            else "machine-learning"
        )
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
        ],
        "method": [
            "method",
            "experiment",
            "measurement",
            "paradigm",
            "approach",
            "algorithm",
        ],
        "application": [
            "application",
            "intervention",
            "applied",
            "real-world",
            "deploy",
            "clinical",
        ],
        "development": [
            "developmental",
            "age-related",
            "child",
            "infant",
            "lifespan",
            "trajectory",
        ],
        "individual-differences": [
            "individual differences",
            "aptitude",
            "personality",
            "cognitive style",
            "intelligence",
        ],
        "technology": [
            "VR",
            "AR",
            "virtual reality",
            "augmented reality",
            "AI tutor",
            "brain-computer",
            "platform",
            "software",
        ],
        "review": [
            "survey",
            "review",
            "meta-analysis",
            "bibliometric",
            "systematic review",
        ],
    }
    sub_scores = {}
    for sub, keywords in sub_keywords.items():
        sub_scores[sub] = sum(1 for k in keywords if k in text)
    subcategory = (
        max(sub_scores, key=sub_scores.get) if any(sub_scores.values()) else "theory"
    )
    return category, subcategory


def main():
    import yaml

    base = Path(__file__).resolve().parent.parent.parent
    yaml_path = base / "papers.yaml"
    json_path = base / "papers.json"

    print("Loading papers from JSON...", flush=True)
    with open(json_path) as f:
        papers = json.load(f)
    by_id = set()
    titles_set = set()
    for p in papers:
        url = p.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        if match:
            by_id.add(match.group(1))
        titles_set.add(p.get("title", "").lower().strip())
    print(f"Loaded {len(papers)} papers", flush=True)

    total_new = 0
    for cat_name, queries in CATEGORY_BATCHES.items():
        cat_new = 0
        for qi, query in enumerate(queries):
            print(f"\n[{cat_name} {qi + 1}/{len(queries)}] {query[:55]}...", flush=True)
            entries = search_arxiv(query)
            print(f"  {len(entries)} results", flush=True)

            for entry in entries:
                arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
                arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None
                if arxiv_id and arxiv_id in by_id:
                    continue
                title = entry.get("title", "")
                title_lower = title.lower().strip()
                if title_lower in titles_set:
                    continue

                abstract = entry.get("abstract", "")
                category, subcategory = classify_paper(title, abstract, cat_name)
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
                    by_id.add(arxiv_id)
                titles_set.add(title_lower)
                papers.append(new_paper)
                total_new += 1
                cat_new += 1

            time.sleep(5)

        print(f"  {cat_name}: +{cat_new} papers", flush=True)

        print("  Saving JSON checkpoint...", flush=True)
        with open(json_path, "w") as f:
            json.dump(papers, f, ensure_ascii=False)

    print(f"\nConverting to YAML...", flush=True)
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            {"papers": papers},
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    cat_counter = Counter()
    for p in papers:
        cat_counter[p.get("category", "unknown")] += 1

    print(f"\n{'=' * 60}", flush=True)
    print(f"Total: {len(papers)} | New: {total_new}", flush=True)
    for cat in sorted(VALID_CATEGORIES):
        count = cat_counter.get(cat, 0)
        marker = " *** EMPTY ***" if count == 0 else ""
        print(f"  {cat:30s} {count:5d}{marker}", flush=True)

    missing = [c for c in VALID_CATEGORIES if cat_counter.get(c, 0) == 0]
    if missing:
        print(f"\nMISSING: {', '.join(missing)}", flush=True)
    else:
        print("\nAll 20 categories populated!", flush=True)


if __name__ == "__main__":
    main()
