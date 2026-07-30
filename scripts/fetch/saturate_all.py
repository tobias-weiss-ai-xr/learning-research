#!/usr/bin/env python3
"""Saturate papers.yaml with 5000+ papers across all 20 taxonomy categories.

Runs 250+ targeted arXiv queries (10-15 per category) covering a 48-month window.
Auto-classifies by keyword heuristics, deduplicates by title, saves incrementally.
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

CATEGORY_QUERIES = {
    "cognitive-science": [
        'all:"cognitive science" AND abs:"learning"',
        'all:"working memory" AND abs:"cognitive"',
        'all:"attention" AND abs:"cognitive" AND abs:"learning"',
        'all:"decision making" AND abs:"learning"',
        'all:"mental model" AND abs:"learning"',
        'all:"cognitive load" AND abs:"learning"',
        'all:"cognitive control" AND abs:"learning"',
        'all:"executive function" AND abs:"learning"',
        'all:"cognitive flexibility" AND abs:"learning"',
        'all:"reasoning" AND abs:"learning" AND abs:"cognitive"',
        'all:"problem solving" AND abs:"cognitive" AND abs:"learning"',
        'all:"metacognition" AND abs:"learning"',
    ],
    "neuroscience": [
        'all:"neuroscience" AND abs:"learning"',
        'all:"synaptic plasticity" AND abs:"learning"',
        'all:"neural plasticity" AND abs:"learning"',
        'all:"dopamine" AND abs:"learning"',
        'all:"hippocampus" AND abs:"memory" AND abs:"learning"',
        'all:"cortical plasticity" AND abs:"learning"',
        'all:"neurotransmitter" AND abs:"learning"',
        'all:"brain" AND abs:"plasticity" AND abs:"learning"',
        'all:"spike-timing" AND abs:"learning"',
        'all:"long-term potentiation" AND abs:"learning"',
        'all:"prefrontal cortex" AND abs:"learning"',
        'all:"basal ganglia" AND abs:"learning"',
        'all:"neural circuit" AND abs:"learning"',
    ],
    "education": [
        'all:"education" AND abs:"learning"',
        'all:"pedagogy" AND abs:"learning"',
        'all:"instructional design" AND abs:"learning"',
        'all:"educational technology" AND abs:"learning"',
        'all:"student learning" AND abs:"model"',
        'all:"classroom" AND abs:"learning" AND abs:"AI"',
        'all:"intelligent tutoring" AND abs:"learning"',
        'all:"learning analytics" AND abs:"education"',
        'all:"adaptive learning" AND abs:"education"',
        'all:"formative assessment" AND abs:"learning"',
        'all:"blended learning" AND abs:"education"',
        'all:"MOOC" AND abs:"learning"',
        'all:"e-learning" AND abs:"education"',
    ],
    "developmental": [
        'all:"child development" AND abs:"cognition"',
        'all:"language acquisition" AND abs:"child"',
        'all:"cognitive development" AND abs:"learning"',
        'all:"infant learning" AND abs:"cognition"',
        'all:"developmental" AND abs:"learning" AND abs:"cognition"',
        'all:"early childhood" AND abs:"learning"',
        'all:"adolescent" AND abs:"learning" AND abs:"cognition"',
        'all:"lifespan" AND abs:"learning"',
        'all:"developmental psychology" AND abs:"learning"',
        'all:"prelinguistic" AND abs:"learning"',
        'all:"theory of mind" AND abs:"development"',
        'all:"numeracy" AND abs:"development" AND abs:"learning"',
    ],
    "behavioral": [
        'all:"behavioral economics" AND abs:"learning"',
        'all:"habit formation" AND abs:"learning"',
        'all:"operant conditioning" AND abs:"learning"',
        'all:"classical conditioning" AND abs:"learning"',
        'all:"reinforcement" AND abs:"behavior" AND abs:"learning"',
        'all:"behavioral" AND abs:"learning" AND abs:"model"',
        'all:"reward learning" AND abs:"behavioral"',
        'all:"punishment" AND abs:"learning" AND abs:"behavior"',
        'all:"behavior change" AND abs:"learning"',
        'all:"choice behavior" AND abs:"learning"',
        'all:"stimulus response" AND abs:"learning"',
        'all:"temporal difference" AND abs:"behavior"',
    ],
    "social-learning": [
        'all:"social learning" AND abs:"cognition"',
        'all:"observational learning"',
        'all:"cultural transmission" AND abs:"learning"',
        'all:"peer learning" AND abs:"education"',
        'all:"social cognition" AND abs:"learning"',
        'all:"imitation" AND abs:"learning" AND abs:"social"',
        'all:"collaborative learning"',
        'all:"cooperative learning"',
        'all:"social network" AND abs:"learning"',
        'all:"social influence" AND abs:"learning"',
        'all:"crowd learning"',
        'all:"social norm" AND abs:"learning"',
    ],
    "language": [
        'all:"language learning" AND abs:"model"',
        'all:"second language" AND abs:"acquisition"',
        'all:"bilingualism" AND abs:"learning"',
        'all:"literacy" AND abs:"learning"',
        'all:"speech" AND abs:"learning"',
        'all:"natural language" AND abs:"learning"',
        'all:"phonological" AND abs:"learning"',
        'all:"morphological" AND abs:"learning"',
        'all:"syntax" AND abs:"learning"',
        'all:"vocabulary" AND abs:"acquisition"',
        'all:"reading" AND abs:"learning" AND abs:"comprehension"',
        'all:"language processing" AND abs:"learning"',
        'all:"pragmatics" AND abs:"learning"',
    ],
    "motor": [
        'all:"motor learning" AND abs:"skill"',
        'all:"skill acquisition" AND abs:"motor"',
        'all:"procedural memory" AND abs:"motor"',
        'all:"embodied cognition" AND abs:"learning"',
        'all:"sports" AND abs:"learning"',
        'all:"sensorimotor" AND abs:"learning"',
        'all:"motor control" AND abs:"learning"',
        'all:"motor adaptation" AND abs:"learning"',
        'all:"motor sequence" AND abs:"learning"',
        'all:"action learning"',
        'all:"robot" AND abs:"motor learning"',
        'all:"force field" AND abs:"motor learning"',
    ],
    "emotion": [
        'all:"emotional learning" AND abs:"cognition"',
        'all:"affective neuroscience" AND abs:"learning"',
        'all:"emotion regulation" AND abs:"learning"',
        'all:"stress" AND abs:"learning" AND abs:"cognition"',
        'all:"affective" AND abs:"learning"',
        'all:"emotion" AND abs:"memory" AND abs:"learning"',
        'all:"fear learning" AND abs:"conditioning"',
        'all:"anxiety" AND abs:"learning"',
        'all:"well-being" AND abs:"learning"',
        'all:"sentiment" AND abs:"learning"',
        'all:"emotional intelligence" AND abs:"learning"',
        'all:"valence" AND abs:"learning" AND abs:"arousal"',
    ],
    "creative": [
        'all:"creativity" AND abs:"learning"',
        'all:"creative cognition" AND abs:"learning"',
        'all:"divergent thinking" AND abs:"learning"',
        'all:"artistic" AND abs:"learning" AND abs:"cognition"',
        'all:"creative process" AND abs:"learning"',
        'all:"innovation" AND abs:"learning" AND abs:"creative"',
        'all:"design thinking" AND abs:"learning"',
        'all:"creative problem solving"',
        'all:"imagination" AND abs:"learning"',
        'all:"generative art" AND abs:"learning"',
        'all:"creative AI" AND abs:"learning"',
    ],
    "machine-learning": [
        'all:"machine learning" AND abs:"survey"',
        'all:"deep learning" AND abs:"survey"',
        'all:"supervised learning" AND abs:"method"',
        'all:"reinforcement learning" AND abs:"survey"',
        'all:"self-supervised learning"',
        'all:"meta-learning" AND abs:"algorithm"',
        'all:"continual learning" AND abs:"method"',
        'all:"transfer learning" AND abs:"survey"',
        'all:"federated learning"',
        'all:"contrastive learning"',
        'all:"graph neural" AND abs:"learning"',
        'all:"representation learning"',
        'all:"transformer" AND abs:"learning"',
        'all:"in-context learning"',
        'all:"active learning" AND abs:"survey"',
    ],
    "evolutionary": [
        'all:"evolution" AND abs:"cognition" AND abs:"learning"',
        'all:"comparative cognition" AND abs:"learning"',
        'all:"animal intelligence" AND abs:"evolution"',
        'all:"cultural evolution" AND abs:"learning"',
        'all:"evolutionary" AND abs:"learning" AND abs:"algorithm"',
        'all:"evolutionary psychology" AND abs:"learning"',
        'all:"natural selection" AND abs:"learning"',
        'all:"phylogenetic" AND abs:"cognition"',
        'all:"hominin" AND abs:"cognition" AND abs:"learning"',
        'all:"tool use" AND abs:"evolution"',
        'all:"social evolution" AND abs:"learning"',
    ],
    "philosophy-of-mind": [
        'all:"philosophy" AND abs:"mind" AND abs:"learning"',
        'all:"epistemology" AND abs:"learning"',
        'all:"consciousness" AND abs:"learning"',
        'all:"mental representation" AND abs:"learning"',
        'all:"phenomenology" AND abs:"learning"',
        'all:"philosophy of cognition" AND abs:"learning"',
        'all:"rationalism" AND abs:"learning"',
        'all:"empiricism" AND abs:"learning"',
        'all:"intentionality" AND abs:"learning"',
        'all:"knowledge representation" AND abs:"philosophy"',
        'all:"normative" AND abs:"learning" AND abs:"cognition"',
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
    ],
    "neuromorphic": [
        'all:"neuromorphic computing" AND abs:"learning"',
        'all:"spiking neural" AND abs:"learning"',
        'all:"brain-inspired" AND abs:"learning" AND abs:"computing"',
        'all:"event-driven" AND abs:"neural" AND abs:"learning"',
        'all:"memristor" AND abs:"learning"',
        'all:"neuromorphic" AND abs:"plasticity"',
        'all:"spike-timing dependent" AND abs:"plasticity"',
        'all:"hardware" AND abs:"spiking" AND abs:"learning"',
        'all:"brain-inspired" AND abs:"algorithm" AND abs:"learning"',
        'all:"analog" AND abs:"neural" AND abs:"learning"',
        'all:"Intel Loihi" AND abs:"learning"',
    ],
    "memory-science": [
        'all:"episodic memory" AND abs:"learning"',
        'all:"semantic memory" AND abs:"learning"',
        'all:"working memory" AND abs:"learning"',
        'all:"forgetting" AND abs:"memory" AND abs:"learning"',
        'all:"long-term memory" AND abs:"learning"',
        'all:"memory consolidation" AND abs:"learning"',
        'all:"memory retrieval" AND abs:"learning"',
        'all:"memory formation" AND abs:"neural"',
        'all:"recognition memory" AND abs:"learning"',
        'all:"recall" AND abs:"memory" AND abs:"learning"',
        'all:"reconsolidation" AND abs:"memory" AND abs:"learning"',
        'all:"memory model" AND abs:"computational"',
    ],
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
        'all:"texture learning" AND abs:"perceptual"',
    ],
    "collective": [
        'all:"swarm intelligence" AND abs:"learning"',
        'all:"collective behavior" AND abs:"learning"',
        'all:"group decision" AND abs:"learning"',
        'all:"organizational learning"',
        'all:"multi-agent" AND abs:"learning" AND abs:"collective"',
        'all:" swarm" AND abs:"optimization" AND abs:"learning"',
        'all:"ant colony" AND abs:"learning"',
        'all:"particle swarm" AND abs:"learning"',
        'all:"collective intelligence" AND abs:"learning"',
        'all:"flocking" AND abs:"learning"',
        'all:"distributed learning" AND abs:"system"',
        'all:"consensus" AND abs:"learning" AND abs:"group"',
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


def build_queries():
    queries = []
    for cat, cat_qs in CATEGORY_QUERIES.items():
        for q in cat_qs:
            queries.append((cat, q))
    return queries


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


def search_arxiv(query, months_back, intended_category):
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
                entry["_intended_category"] = intended_category
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
            "problem solving",
            "reasoning",
            "cognitive control",
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
            "prefrontal cortex",
            "basal ganglia",
            "neural circuit",
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
            "formative assessment",
            "blended learning",
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
            "adolescent",
            "prelinguistic",
            "theory of mind",
            "numeracy",
        ],
        "behavioral": [
            "behavioral economics",
            "habit formation",
            "operant conditioning",
            "classical conditioning",
            "behavior modification",
            "reward learning",
            "punishment",
            "behavior change",
            "choice behavior",
            "stimulus response",
            "temporal difference",
        ],
        "social-learning": [
            "social learning",
            "observational learning",
            "cultural transmission",
            "peer learning",
            "social cognition",
            "collaborative learning",
            "cooperative learning",
            "social network",
            "social influence",
            "crowd learning",
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
            "vocabulary acquisition",
            "reading comprehension",
            "language processing",
            "pragmatics",
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
            "force field",
        ],
        "emotion": [
            "emotional learning",
            "affective neuroscience",
            "emotion regulation",
            "stress learning",
            "affective",
            "fear learning",
            "anxiety",
            "well-being",
            "sentiment",
            "emotional intelligence",
            "valence",
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
            "hominin",
            "social evolution",
        ],
        "philosophy-of-mind": [
            "epistemology",
            "consciousness",
            "mental representation",
            "theory of knowledge",
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
            "tool use animal",
            "animal conditioning",
            "spatial learning animal",
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
            "multi-agent collective",
            "ant colony",
            "particle swarm",
            "collective intelligence",
            "flocking",
            "distributed learning",
            "consensus learning",
        ],
        "health": [
            "health behavior",
            "patient education",
            "medical training",
            "public health",
            "clinical learning",
            "health literacy",
            "digital health",
            "rehabilitation learning",
            "sleep learning",
            "nutrition cognition",
            "exercise cognition",
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

    queries = build_queries()
    print(f"Loaded {len(papers)} existing papers", flush=True)
    print(
        f"Total queries: {len(queries)} across {len(CATEGORY_QUERIES)} categories",
        flush=True,
    )
    print(f"Search window: {MONTHS_BACK} months", flush=True)

    total_new = 0
    cat_new = Counter()
    seen_ids = set()
    seen_titles = set(titles_lower)

    for qi, (intended_cat, query) in enumerate(queries):
        short_q = query[:60]
        print(f"\n[{qi + 1}/{len(queries)}] {intended_cat}: {short_q}...", flush=True)

        entries = search_arxiv(query, MONTHS_BACK, intended_cat)
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
    sub_counter = Counter()
    for p in papers:
        cat_counter[p.get("category", "unknown")] += 1
        sub_counter[p.get("subcategory", "unknown")] += 1

    print(f"\n{'=' * 60}", flush=True)
    print("FINAL DISTRIBUTION", flush=True)
    print(f"{'=' * 60}", flush=True)
    print(f"Total papers: {len(papers)}", flush=True)
    print(f"New papers added: {total_new}", flush=True)
    print(f"\nBy category:", flush=True)
    for cat in sorted(VALID_CATEGORIES):
        count = cat_counter.get(cat, 0)
        new = cat_new.get(cat, 0)
        marker = " ***" if count == 0 else ""
        print(f"  {cat:30s} {count:5d} total  (+{new} new){marker}", flush=True)
    print(f"\nBy subcategory:", flush=True)
    for sub in sorted(VALID_SUBCATEGORIES):
        print(f"  {sub:25s} {sub_counter.get(sub, 0):5d}", flush=True)

    missing = [c for c in VALID_CATEGORIES if cat_counter.get(c, 0) == 0]
    if missing:
        print(f"\nMISSING categories: {', '.join(missing)}", flush=True)
    else:
        print(f"\nAll 20 categories populated!", flush=True)


if __name__ == "__main__":
    main()
