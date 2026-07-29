#!/usr/bin/env python3
"""Saturate papers.yaml by searching arXiv comprehensively for learning research papers.

Runs 150+ diverse queries across cs.AI, cs.LG, cs.CL, cs.RO, cs.CY, q-bio.NC
and other categories covering all 20 taxonomy categories.
Auto-classifies, deduplicates, and loops until saturation (<5 new).
Saves after each round to survive timeouts.
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
SATURATION_THRESHOLD = 5
MAX_RESULTS_PER_QUERY = 100
MONTHS_BACK = 48
MAX_ROUNDS = 3

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
    'cat:cs.AI AND abs:"learning" AND abs:"attention"',
    'cat:cs.CL AND abs:"learning" AND abs:"attention"',
    'cat:cs.AI AND abs:"cultural evolution" AND abs:"learning"',
    'cat:cs.SI AND abs:"cultural transmission" AND abs:"learning"',
    'cat:cs.AI AND abs:"embodied" AND abs:"learning"',
    'cat:cs.RO AND abs:"embodied" AND abs:"learning"',
    'cat:cs.AI AND abs:"procedural learning"',
    'cat:cs.LG AND abs:"procedural learning"',
    'cat:cs.CY AND abs:"public health" AND abs:"learning"',
    'cat:cs.CY AND abs:"behavior change" AND abs:"learning"',
    'cat:cs.AI AND abs:"causal learning"',
    'cat:cs.LG AND abs:"causal learning"',
    'cat:cs.AI AND abs:"analogical" AND abs:"learning"',
    'cat:cs.AI AND abs:"concept learning"',
    'cat:cs.LG AND abs:"concept learning"',
    'cat:cs.AI AND abs:"observation learning"',
    'cat:cs.AI AND abs:"observational learning"',
    'cat:q-bio.NC AND abs:"sensory" AND abs:"plasticity"',
    'cat:q-bio.NC AND abs:"visual learning"',
    'cat:cs.CV AND abs:"visual learning"',
    'cat:q-bio.NC AND abs:"auditory learning"',
    'cat:cs.AI AND abs:"expertise" AND abs:"learning"',
    'cat:cs.AI AND abs:"divergent thinking" AND abs:"learning"',
    'cat:cs.AI AND abs:"artistic" AND abs:"learning"',
    'cat:q-bio.NC AND abs:"trauma" AND abs:"learning"',
    'cat:cs.AI AND abs:"emotion regulation" AND abs:"learning"',
    'cat:cs.AI AND abs:"classical conditioning" AND abs:"model"',
    'cat:cs.AI AND abs:"operant conditioning" AND abs:"model"',
    'cat:cs.AI AND abs:"peer" AND abs:"learning"',
    'cat:cs.CY AND abs:"peer" AND abs:"learning"',
    'cat:cs.AI AND abs:"tool use" AND abs:"learning"',
    'cat:cs.RO AND abs:"tool use" AND abs:"learning"',
    'cat:cs.AI AND abs:"navigation" AND abs:"learning"',
    'cat:cs.RO AND abs:"navigation" AND abs:"learning"',
    'cat:cs.AI AND abs:"foraging" AND abs:"learning"',
    'cat:cs.AI AND abs:"group learning"',
    'cat:cs.MA AND abs:"group learning"',
    'cat:cs.AI AND abs:"mental model" AND abs:"learning"',
    'cat:cs.AI AND abs:"mental representation" AND abs:"learning"',
    'cat:cs.AI AND abs:"brain region" AND abs:"learning"',
    'cat:cs.AI AND abs:"fMRI" AND abs:"learning"',
    'cat:cs.AI AND abs:"pedagogy" AND abs:"AI"',
    'cat:cs.CY AND abs:"pedagogy" AND abs:"AI"',
    'cat:cs.AI AND abs:"assessment" AND abs:"learning" AND abs:"AI"',
    'cat:cs.CY AND abs:"assessment" AND abs:"learning" AND abs:"AI"',
    'cat:cs.AI AND abs:"lifespan" AND abs:"learning"',
    'cat:cs.AI AND abs:"cognitive style" AND abs:"learning"',
    'cat:cs.AI AND abs:"aptitude" AND abs:"learning"',
    'cat:cs.AI AND abs:"individual differences" AND abs:"learning"',
    'cat:cs.AI AND abs:"zone of proximal development"',
    'cat:cs.CY AND abs:"zone of proximal development"',
    'cat:cs.AI AND abs:"scaffolding" AND abs:"learning"',
    'cat:cs.CY AND abs:"scaffolding" AND abs:"learning"',
    'cat:cs.AI AND abs:"AI tutor" AND abs:"learning"',
    'cat:cs.CY AND abs:"AI tutor" AND abs:"learning"',
    'cat:cs.AI AND abs:"VR" AND abs:"education"',
    'cat:cs.HC AND abs:"VR" AND abs:"education"',
    'cat:cs.AI AND abs:"AR" AND abs:"education"',
    'cat:cs.HC AND abs:"AR" AND abs:"education"',
    'cat:cs.AI AND abs:"bibliometric" AND abs:"learning"',
    'cat:cs.AI AND abs:"meta-analysis" AND abs:"learning"',
    'cat:cs.AI AND abs:"systematic review" AND abs:"learning"',
]


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


def classify_paper(title, abstract):
    text = f"{title} {abstract}".lower()

    cat_keywords = {
        "cognitive-science": [
            "cognitive",
            "mental model",
            "attention",
            "perception",
            "decision-making",
            "working memory",
        ],
        "neuroscience": [
            "neural plasticity",
            "synaptic",
            "brain region",
            "fMRI",
            "neural network",
            "dopamine",
            "hippocampus",
        ],
        "education": [
            "pedagogy",
            "instructional design",
            "classroom",
            "educational technology",
            "assessment",
            "intelligent tutoring",
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
            "behavior modification",
            "operant",
            "classical",
        ],
        "social-learning": [
            "social learning",
            "observational learning",
            "cultural transmission",
            "peer learning",
        ],
        "language": [
            "language learning",
            "linguistic",
            "bilingual",
            "literacy",
            "speech",
        ],
        "motor": [
            "motor learning",
            "skill acquisition",
            "procedural memory",
            "embodied",
            "sports",
        ],
        "emotion": ["emotional learning", "affective", "emotion regulation", "trauma"],
        "creative": [
            "creativity",
            "creative cognition",
            "artistic",
            "divergent thinking",
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
        ],
        "evolutionary": [
            "evolution",
            "comparative cognition",
            "cultural evolution",
            "evolutionary learning",
        ],
        "philosophy-of-mind": [
            "epistemology",
            "consciousness",
            "mental representation",
            "theory of knowledge",
        ],
        "educational-psychology": [
            "motivation",
            "self-regulation",
            "growth mindset",
            "zone of proximal",
            "scaffolding",
        ],
        "animal-learning": [
            "animal",
            "foraging",
            "animal cognition",
            "animal memory",
            "animal intelligence",
        ],
        "neuromorphic": ["neuromorphic", "spiking network", "brain-inspired computing"],
        "memory-science": [
            "episodic memory",
            "semantic memory",
            "procedural memory",
            "forgetting",
            "memory systems",
        ],
        "perceptual": [
            "perceptual learning",
            "sensory plasticity",
            "visual learning",
            "auditory learning",
            "expertise",
        ],
        "collective": [
            "swarm",
            "collective behavior",
            "group learning",
            "organizational learning",
        ],
        "health": [
            "health behavior",
            "patient education",
            "medical training",
            "public health",
        ],
    }

    scores = {}
    for cat, keywords in cat_keywords.items():
        scores[cat] = sum(1 for k in keywords if k in text)

    if not any(scores.values()):
        return "machine-learning", "theory"

    category = max(scores, key=scores.get)

    sub_keywords = {
        "theory": ["theory", "model", "framework", "formalism", "survey", "taxonomy"],
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
        ],
        "development": [
            "developmental",
            "age",
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
            "tool",
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

    if not any(sub_scores.values()):
        subcategory = "theory"
    else:
        subcategory = max(sub_scores, key=sub_scores.get)

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
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )


def run_round(yaml_path, data, papers, by_id, titles_lower, queries, round_num):
    print(f"\n{'=' * 60}", flush=True)
    print(f"ROUND {round_num}", flush=True)
    print(f"{'=' * 60}", flush=True)

    round_new = []
    seen_ids = set()
    seen_titles = set(titles_lower)

    for qi, query in enumerate(queries):
        cat_match = re.search(r"cat:(\S+)", query)
        cat = cat_match.group(1) if cat_match else "?"
        print(
            f"\n  Query {qi + 1}/{len(queries)} [{cat}]...",
            flush=True,
        )

        entries = search_arxiv(query, MONTHS_BACK)
        print(f"    arXiv returned {len(entries)} entries", flush=True)

        for entry in entries:
            arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None

            if arxiv_id and arxiv_id in by_id:
                continue

            if arxiv_id and arxiv_id in seen_ids:
                continue

            title = entry.get("title", "")
            title_lower = title.lower().strip()

            if title_lower in seen_titles:
                continue

            if dedup_title(title, titles_lower):
                continue

            abstract = entry.get("abstract", "")
            category, subcategory = classify_paper(title, abstract)

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
            seen_titles.add(title_lower)
            titles_lower.append(title_lower)
            round_new.append(new_paper)
            by_id[arxiv_id] = new_paper

            print(
                f"    NEW [{category}/{subcategory}] {title[:70]}",
                flush=True,
            )

        time.sleep(API_DELAY)

        if (qi + 1) % 20 == 0:
            save_papers(yaml_path, data, papers + round_new)
            print(
                f"    [checkpoint] saved {len(papers) + len(round_new)} papers",
                flush=True,
            )

    print(f"\n  Round {round_num} found {len(round_new)} new papers", flush=True)
    return round_new


def main():
    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    data, papers, by_id, titles_lower = load_existing_papers(yaml_path)

    print(f"Loaded {len(papers)} existing papers", flush=True)
    print(f"Using {len(QUERIES)} queries", flush=True)
    print(f"Search window: {MONTHS_BACK} months", flush=True)

    total_new = 0
    round_num = 1

    while round_num <= MAX_ROUNDS:
        round_new = run_round(
            yaml_path, data, papers, by_id, titles_lower, QUERIES, round_num
        )

        papers.extend(round_new)
        total_new += len(round_new)

        save_papers(yaml_path, data, papers)
        print(f"  Saved {len(papers)} total papers to {yaml_path}", flush=True)

        if len(round_new) < SATURATION_THRESHOLD:
            print(
                f"\nSATURATED: Round {round_num} found only {len(round_new)} "
                f"new papers (< {SATURATION_THRESHOLD} threshold)",
                flush=True,
            )
            break

        print(
            f"\n  Total new so far: {total_new}, starting round {round_num + 1}...",
            flush=True,
        )
        round_num += 1

    if round_num > MAX_ROUNDS:
        print(
            f"\nReached max rounds ({MAX_ROUNDS}). Stopping.",
            flush=True,
        )

    if total_new == 0:
        print("\nNo new papers found. papers.yaml unchanged.", flush=True)

    cat_counter = Counter()
    sub_counter = Counter()
    for p in papers:
        cat_counter[p.get("category", "unknown")] += 1
        sub_counter[p.get("subcategory", "unknown")] += 1

    print(f"\n{'=' * 60}", flush=True)
    print("FINAL DISTRIBUTION", flush=True)
    print(f"{'=' * 60}", flush=True)
    print(f"Total papers: {len(papers)}", flush=True)
    print(f"New papers added: {total_new}", flush=True)
    print(f"Rounds: {round_num}", flush=True)


if __name__ == "__main__":
    main()
