#!/usr/bin/env python3
"""Continue saturation: run remaining queries for categories not yet covered.

Phase 1 completed queries 1-100 (cognitive-science through motor).
This script runs queries 101-241 (emotion through health) plus bonus
queries for underrepresented categories.
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
CHECKPOINT_INTERVAL = 20

REMAINING_QUERIES = [
    ("emotion", 'all:"sentiment" AND abs:"learning"'),
    ("emotion", 'all:"emotional intelligence" AND abs:"learning"'),
    ("emotion", 'all:"valence" AND abs:"learning" AND abs:"arousal"'),
    ("creative", 'all:"creativity" AND abs:"learning"'),
    ("creative", 'all:"creative cognition" AND abs:"learning"'),
    ("creative", 'all:"divergent thinking" AND abs:"learning"'),
    ("creative", 'all:"artistic" AND abs:"learning" AND abs:"cognition"'),
    ("creative", 'all:"creative process" AND abs:"learning"'),
    ("creative", 'all:"innovation" AND abs:"learning" AND abs:"creative"'),
    ("creative", 'all:"design thinking" AND abs:"learning"'),
    ("creative", 'all:"creative problem solving"'),
    ("creative", 'all:"imagination" AND abs:"learning"'),
    ("creative", 'all:"generative art" AND abs:"learning"'),
    ("creative", 'all:"creative AI" AND abs:"learning"'),
    ("machine-learning", 'all:"machine learning" AND abs:"survey"'),
    ("machine-learning", 'all:"deep learning" AND abs:"survey"'),
    ("machine-learning", 'all:"supervised learning" AND abs:"method"'),
    ("machine-learning", 'all:"reinforcement learning" AND abs:"survey"'),
    ("machine-learning", 'all:"self-supervised learning"'),
    ("machine-learning", 'all:"meta-learning" AND abs:"algorithm"'),
    ("machine-learning", 'all:"continual learning" AND abs:"method"'),
    ("machine-learning", 'all:"transfer learning" AND abs:"survey"'),
    ("machine-learning", 'all:"federated learning"'),
    ("machine-learning", 'all:"contrastive learning"'),
    ("machine-learning", 'all:"graph neural" AND abs:"learning"'),
    ("machine-learning", 'all:"representation learning"'),
    ("machine-learning", 'all:"transformer" AND abs:"learning"'),
    ("machine-learning", 'all:"in-context learning"'),
    ("machine-learning", 'all:"active learning" AND abs:"survey"'),
    ("evolutionary", 'all:"evolution" AND abs:"cognition" AND abs:"learning"'),
    ("evolutionary", 'all:"comparative cognition" AND abs:"learning"'),
    ("evolutionary", 'all:"animal intelligence" AND abs:"evolution"'),
    ("evolutionary", 'all:"cultural evolution" AND abs:"learning"'),
    ("evolutionary", 'all:"evolutionary" AND abs:"learning" AND abs:"algorithm"'),
    ("evolutionary", 'all:"evolutionary psychology" AND abs:"learning"'),
    ("evolutionary", 'all:"natural selection" AND abs:"learning"'),
    ("evolutionary", 'all:"phylogenetic" AND abs:"cognition"'),
    ("evolutionary", 'all:"hominin" AND abs:"cognition" AND abs:"learning"'),
    ("evolutionary", 'all:"tool use" AND abs:"evolution"'),
    ("evolutionary", 'all:"social evolution" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"philosophy" AND abs:"mind" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"epistemology" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"consciousness" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"mental representation" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"phenomenology" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"philosophy of cognition" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"rationalism" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"empiricism" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"intentionality" AND abs:"learning"'),
    ("philosophy-of-mind", 'all:"knowledge representation" AND abs:"philosophy"'),
    ("philosophy-of-mind", 'all:"normative" AND abs:"learning" AND abs:"cognition"'),
    ("educational-psychology", 'all:"educational psychology" AND abs:"learning"'),
    ("educational-psychology", 'all:"growth mindset" AND abs:"learning"'),
    ("educational-psychology", 'all:"self-regulation" AND abs:"learning"'),
    ("educational-psychology", 'all:"motivation" AND abs:"learning"'),
    ("educational-psychology", 'all:"scaffolding" AND abs:"learning"'),
    ("educational-psychology", 'all:"zone of proximal" AND abs:"learning"'),
    ("educational-psychology", 'all:"self-efficacy" AND abs:"learning"'),
    ("educational-psychology", 'all:"cognitive apprenticeship"'),
    ("educational-psychology", 'all:"constructivism" AND abs:"learning"'),
    ("educational-psychology", 'all:"achievement motivation" AND abs:"learning"'),
    ("educational-psychology", 'all:"engagement" AND abs:"learning" AND abs:"student"'),
    ("educational-psychology", 'all:"academic achievement" AND abs:"learning"'),
    ("animal-learning", 'all:"animal cognition" AND abs:"learning"'),
    ("animal-learning", 'all:"animal memory" AND abs:"learning"'),
    ("animal-learning", 'all:"animal navigation" AND abs:"learning"'),
    ("animal-learning", 'all:"tool use" AND abs:"animal" AND abs:"learning"'),
    ("animal-learning", 'all:"animal" AND abs:"conditioning" AND abs:"learning"'),
    ("animal-learning", 'all:"spatial learning" AND abs:"animal"'),
    ("animal-learning", 'all:"foraging" AND abs:"learning" AND abs:"animal"'),
    ("animal-learning", 'all:"bird song" AND abs:"learning"'),
    ("animal-learning", 'all:"habituation" AND abs:"animal"'),
    ("animal-learning", 'all:"animal communication" AND abs:"learning"'),
    ("animal-learning", 'all:"primate" AND abs:"cognition" AND abs:"learning"'),
    ("neuromorphic", 'all:"neuromorphic computing" AND abs:"learning"'),
    ("neuromorphic", 'all:"spiking neural" AND abs:"learning"'),
    ("neuromorphic", 'all:"brain-inspired" AND abs:"learning" AND abs:"computing"'),
    ("neuromorphic", 'all:"event-driven" AND abs:"neural" AND abs:"learning"'),
    ("neuromorphic", 'all:"memristor" AND abs:"learning"'),
    ("neuromorphic", 'all:"neuromorphic" AND abs:"plasticity"'),
    ("neuromorphic", 'all:"spike-timing dependent" AND abs:"plasticity"'),
    ("neuromorphic", 'all:"hardware" AND abs:"spiking" AND abs:"learning"'),
    ("neuromorphic", 'all:"brain-inspired" AND abs:"algorithm" AND abs:"learning"'),
    ("neuromorphic", 'all:"analog" AND abs:"neural" AND abs:"learning"'),
    ("neuromorphic", 'all:"Intel Loihi" AND abs:"learning"'),
    ("memory-science", 'all:"episodic memory" AND abs:"learning"'),
    ("memory-science", 'all:"semantic memory" AND abs:"learning"'),
    ("memory-science", 'all:"working memory" AND abs:"learning"'),
    ("memory-science", 'all:"forgetting" AND abs:"memory" AND abs:"learning"'),
    ("memory-science", 'all:"long-term memory" AND abs:"learning"'),
    ("memory-science", 'all:"memory consolidation" AND abs:"learning"'),
    ("memory-science", 'all:"memory retrieval" AND abs:"learning"'),
    ("memory-science", 'all:"memory formation" AND abs:"neural"'),
    ("memory-science", 'all:"recognition memory" AND abs:"learning"'),
    ("memory-science", 'all:"recall" AND abs:"memory" AND abs:"learning"'),
    ("memory-science", 'all:"reconsolidation" AND abs:"memory" AND abs:"learning"'),
    ("memory-science", 'all:"memory model" AND abs:"computational"'),
    ("perceptual", 'all:"perceptual learning" AND abs:"visual"'),
    ("perceptual", 'all:"sensory plasticity" AND abs:"learning"'),
    ("perceptual", 'all:"visual expertise" AND abs:"learning"'),
    ("perceptual", 'all:"auditory learning"'),
    ("perceptual", 'all:"perceptual" AND abs:"learning" AND abs:"plasticity"'),
    ("perceptual", 'all:"visual learning" AND abs:"recognition"'),
    ("perceptual", 'all:"face recognition" AND abs:"learning"'),
    ("perceptual", 'all:"object recognition" AND abs:"learning"'),
    ("perceptual", 'all:"speech perception" AND abs:"learning"'),
    ("perceptual", 'all:"cross-modal" AND abs:"learning"'),
    ("perceptual", 'all:"multisensory" AND abs:"learning"'),
    ("perceptual", 'all:"texture learning" AND abs:"perceptual"'),
    ("collective", 'all:"swarm intelligence" AND abs:"learning"'),
    ("collective", 'all:"collective behavior" AND abs:"learning"'),
    ("collective", 'all:"group decision" AND abs:"learning"'),
    ("collective", 'all:"organizational learning"'),
    ("collective", 'all:"multi-agent" AND abs:"learning" AND abs:"collective"'),
    ("collective", 'all:"ant colony" AND abs:"learning"'),
    ("collective", 'all:"particle swarm" AND abs:"learning"'),
    ("collective", 'all:"collective intelligence" AND abs:"learning"'),
    ("collective", 'all:"flocking" AND abs:"learning"'),
    ("collective", 'all:"distributed learning" AND abs:"system"'),
    ("collective", 'all:"consensus" AND abs:"learning" AND abs:"group"'),
    ("health", 'all:"health behavior" AND abs:"learning"'),
    ("health", 'all:"patient education" AND abs:"learning"'),
    ("health", 'all:"medical training" AND abs:"learning"'),
    ("health", 'all:"public health" AND abs:"learning"'),
    ("health", 'all:"clinical" AND abs:"learning" AND abs:"AI"'),
    ("health", 'all:"health literacy" AND abs:"learning"'),
    ("health", 'all:"digital health" AND abs:"learning"'),
    ("health", 'all:"rehabilitation" AND abs:"learning"'),
    ("health", 'all:"sleep" AND abs:"learning" AND abs:"memory"'),
    ("health", 'all:"nutrition" AND abs:"cognition" AND abs:"learning"'),
    ("health", 'all:"exercise" AND abs:"cognition" AND abs:"learning"'),
    ("health", 'all:"aging" AND abs:"cognition" AND abs:"learning"'),
]

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


def load_existing_papers(yaml_path):
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


def title_similarity(a, b):
    a_clean = re.sub(r"[^\w\s]", "", a.lower())
    b_clean = re.sub(r"[^\w\s]", "", b.lower())
    return SequenceMatcher(None, a_clean, b_clean).ratio()


def search_arxiv(query, months_back):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=months_back * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"
    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"
    try:
        resp = requests.get(
            ARXIV_SEARCH_API.format(
                requests.utils.quote(full_query), 0, MAX_RESULTS_PER_QUERY
            ),
            timeout=30,
        )
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
        print(f"  WARNING: arXiv search error: {e}", flush=True)
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
            "executive function",
            "cognitive flexibility",
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
            "brain plasticity",
            "spike-timing",
            "long-term potentiation",
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
            "mooc",
            "e-learning",
        ],
        "developmental": [
            "child development",
            "language acquisition",
            "cognitive development",
            "infant",
            "lifespan",
            "developmental psychology",
            "early childhood",
        ],
        "behavioral": [
            "behavioral economics",
            "habit formation",
            "operant conditioning",
            "classical conditioning",
            "behavior modification",
            "reward learning",
            "behavior change",
            "temporal difference",
        ],
        "social-learning": [
            "social learning",
            "observational learning",
            "cultural transmission",
            "peer learning",
            "collaborative learning",
            "cooperative learning",
            "social network",
            "social influence",
            "social norm",
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
            "reading",
            "language processing",
        ],
        "motor": [
            "motor learning",
            "skill acquisition",
            "procedural memory",
            "embodied cognition",
            "sports",
            "sensorimotor",
            "motor control",
            "motor adaptation",
            "motor sequence",
            "action learning",
        ],
        "emotion": [
            "emotional learning",
            "affective neuroscience",
            "emotion regulation",
            "stress",
            "affective",
            "fear learning",
            "anxiety",
            "well-being",
            "sentiment",
            "emotional intelligence",
        ],
        "creative": [
            "creativity",
            "creative cognition",
            "artistic",
            "divergent thinking",
            "creative process",
            "innovation",
            "design thinking",
            "creative problem solving",
            "imagination",
            "generative art",
            "creative ai",
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
            "evolutionary psychology",
            "natural selection",
            "phylogenetic",
            "social evolution",
        ],
        "philosophy-of-mind": [
            "epistemology",
            "consciousness",
            "mental representation",
            "phenomenology",
            "philosophy of cognition",
            "rationalism",
            "empiricism",
            "intentionality",
            "normative cognition",
            "philosophy mind",
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
            "neuromorphic plasticity",
            "analog neural",
            "loihi",
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
            "nutrition cognition",
            "exercise cognition",
            "aging cognition",
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
            "substrate",
        ],
        "method": [
            "method",
            "experiment",
            "measurement",
            "paradigm",
            "approach",
            "algorithm",
            "procedure",
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
            "growth",
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
            "AR",
            "virtual reality",
            "augmented reality",
            "AI tutor",
            "brain-computer",
            "platform",
            "software",
            "system",
        ],
        "review": [
            "survey",
            "review",
            "meta-analysis",
            "bibliometric",
            "systematic review",
            "literature review",
        ],
    }

    sub_scores = {}
    for sub, keywords in sub_keywords.items():
        sub_scores[sub] = sum(1 for k in keywords if k in text)

    subcategory = (
        max(sub_scores, key=sub_scores.get) if any(sub_scores.values()) else "theory"
    )
    return category, subcategory


def dedup_title(title, titles_lower, threshold=0.75):
    title_clean = title.lower().strip()
    for existing in titles_lower:
        if title_similarity(title_clean, existing) >= threshold:
            return True
    return False


def save_papers(yaml_path, data, papers):
    data["papers"] = papers
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


def main():
    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    data, papers, by_id, titles_lower = load_existing_papers(yaml_path)

    print(f"Loaded {len(papers)} existing papers", flush=True)
    print(f"Running {len(REMAINING_QUERIES)} remaining queries", flush=True)

    total_new = 0
    cat_new = Counter()
    seen_ids = set()
    seen_titles = set(titles_lower)

    for qi, (intended_cat, query) in enumerate(REMAINING_QUERIES):
        short_q = query[:60]
        print(
            f"\n[{qi + 1}/{len(REMAINING_QUERIES)}] {intended_cat}: {short_q}...",
            flush=True,
        )

        entries = search_arxiv(query, MONTHS_BACK)
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
            if dedup_title(title, titles_lower):
                continue

            abstract = entry.get("abstract", "")
            category, subcategory = classify_paper(title, abstract, intended_cat)

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

        print(f"  +{query_new} new papers (total so far: {len(papers)})", flush=True)

        time.sleep(API_DELAY)

        if (qi + 1) % CHECKPOINT_INTERVAL == 0:
            save_papers(yaml_path, data, papers)
            print(f"  [checkpoint] saved {len(papers)} papers", flush=True)

    save_papers(yaml_path, data, papers)
    print(f"\nSaved {len(papers)} total papers to {yaml_path}", flush=True)

    cat_counter = Counter()
    for p in papers:
        cat_counter[p.get("category", "unknown")] += 1

    print(f"\n{'=' * 60}", flush=True)
    print("FINAL DISTRIBUTION", flush=True)
    print(f"{'=' * 60}", flush=True)
    print(f"Total papers: {len(papers)}", flush=True)
    print(f"New papers added this phase: {total_new}", flush=True)
    print(f"\nBy category:", flush=True)
    for cat in sorted(VALID_CATEGORIES):
        count = cat_counter.get(cat, 0)
        new = cat_new.get(cat, 0)
        marker = " *** EMPTY ***" if count == 0 else ""
        print(f"  {cat:30s} {count:5d} total  (+{new} new){marker}", flush=True)

    missing = [c for c in VALID_CATEGORIES if cat_counter.get(c, 0) == 0]
    if missing:
        print(f"\nMISSING categories: {', '.join(missing)}", flush=True)
    else:
        print(f"\nAll 20 categories populated!", flush=True)


if __name__ == "__main__":
    main()
