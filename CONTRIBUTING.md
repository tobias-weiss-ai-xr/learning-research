# Contributing to Learning Research

Thank you for your interest in contributing! This guide explains how to add papers to the survey.

## Overview

This repository maintains a curated, cross-disciplinary list of research papers on **learning** — spanning 20 academic disciplines from cognitive science to machine learning.

The source of truth is `papers.yaml`. The `README.md` is **auto-generated** from `papers.yaml` — never edit it directly.

## Quick Start: Adding a Paper

1. **Check for duplicates** — search `papers.yaml` by title and URL. If the paper already exists, skip.
2. **Edit `papers.yaml`** — add your entry following the schema below.
3. **Validate** — run `python3 scripts/validate_papers.py`
4. **Regenerate README** — run `python3 scripts/generate_readme.py`
5. **Commit and open a PR** — see the PR checklist below.

## papers.yaml Schema

```yaml
papers:
  - title: "Paper Title"            # Required
    date: "2026-01"                  # Required, YYYY-MM format
    url: "https://arxiv.org/abs/XXXX"  # Required
    category: "cognitive-science"     # Required: see taxonomy below
    subcategory: "theory"            # Required: see taxonomy below
    # Optional fields:
    authors: ["Author1", "Author2"]
    venue: "Nature 2025"
    code_url: "https://github.com/..."
    project_url: "https://..."
    abstract: "..."
    tags: ["tag1", "tag2"]
```

## URL Normalization Rules

- **arXiv papers**: always use `https://arxiv.org/abs/XXXX` format
  - Do NOT use `https://doi.org/10.48550/arXiv.XXXX`
  - Do NOT use `https://www.arxiv.org/abs/XXXX`
  - Do NOT use `https://arxiv.org/pdf/XXXX`
- **Non-arXiv papers**: keep URLs as-is (e.g., `doi.org`, `nature.com`, `pnas.org`)

## Taxonomy Guide

### Category (Discipline — 20 categories)

| Category | Description | Examples |
|----------|-------------|----------|
| **cognitive-science** | Human cognition, memory, attention, perception, decision-making | Working memory models, attention studies, mental models |
| **neuroscience** | Neural plasticity, synaptic learning, brain regions, fMRI | LTP, dopamine and learning, hippocampus |
| **education** | Pedagogy, instructional design, classroom learning | Intelligent tutoring, flipped classroom, assessment |
| **developmental** | Child development, language acquisition | Infant learning, Piaget, Vygotsky |
| **behavioral** | Behavioral economics, habit formation, conditioning | Operant conditioning, nudge theory |
| **social-learning** | Social learning theory, cultural transmission | Bandura, peer effects, imitation |
| **language** | Language learning, linguistics, bilingualism | L2 acquisition, literacy, speech perception |
| **motor** | Motor learning, skill acquisition, embodied cognition | Procedural memory, sports science, robotics |
| **emotion** | Emotional learning, affective neuroscience | Emotion regulation, trauma and learning |
| **creative** | Creativity research, divergent thinking | Creative cognition, artistic learning |
| **machine-learning** | Deep learning, RL, self-supervised, meta-learning | Transformers, curriculum learning |
| **evolutionary** | Evolution of learning, comparative cognition | Cultural evolution, animal intelligence |
| **philosophy-of-mind** | Epistemology, consciousness, mental representation | Theories of knowledge, embodied mind |
| **educational-psychology** | Motivation, self-regulation, growth mindset | Zone of proximal development, scaffolding |
| **animal-learning** | Comparative cognition, animal memory, tool use | Foraging, navigation, animal intelligence |
| **neuromorphic** | Brain-inspired computing, spiking networks | Neuromorphic engineering, SNNs |
| **memory-science** | Human memory systems, forgetting | Episodic, semantic, procedural, working memory |
| **perceptual** | Perceptual learning, sensory plasticity | Visual expertise, auditory learning |
| **collective** | Swarm intelligence, organizational learning | Group learning, multi-agent systems |
| **health** | Health behavior change, patient education | Medical training, public health learning |

### Subcategory (Aspect — 8 subcategories)

| Subcategory | Description | Examples |
|-------------|-------------|----------|
| **theory** | Theoretical frameworks, models, formalisms | Bayesian learning theory, cognitive architectures |
| **mechanism** | Underlying mechanisms, processes, neural correlates | Dopaminergic signaling, synaptic plasticity |
| **method** | Research methods, experimental paradigms, measurement | EEG paradigms, behavioral assays |
| **application** | Applied settings, interventions, real-world use | Classroom interventions, clinical applications |
| **development** | Developmental trajectories, age effects, lifespan | Infant memory, age-related cognitive decline |
| **individual-differences** | Aptitude, intelligence, personality, cognitive style | Learning styles, IQ and learning |
| **technology** | Tools, platforms, AI tutors, VR/AR, BCI | Learning analytics, adaptive systems |
| **review** | Meta-analyses, systematic reviews, surveys | Bibliometric analyses, literature reviews |

A paper may belong to one category/subcategory combination. If a paper spans multiple, choose the **primary** contribution.

## Deduplication Checklist

Before adding a paper, check that it is not already in the list:

1. Search `papers.yaml` by **title** (case-insensitive)
2. Search `papers.yaml` by **URL**
3. If the same paper appears under a different category, that is acceptable

## Local Development Setup

```bash
pip install -r requirements.txt
```

### Useful Commands

| Command | Description |
|---------|-------------|
| `python3 scripts/validate_papers.py` | Validate `papers.yaml` for errors |
| `python3 scripts/validate_papers.py --fix` | Validate and auto-fix URL normalization |
| `python3 scripts/generate_readme.py` | Regenerate `README.md` from `papers.yaml` |
| `python3 scripts/generate_readme.py --check` | Check if README is up-to-date (CI use) |
| `python3 scripts/export_bibtex.py` | Export all papers to BibTeX format |
| `python3 scripts/fetch/fetch_new_papers.py` | Discover new learning research papers from arXiv |
| `python3 scripts/fetch/fetch_new_papers.py --dry-run` | Preview new papers without creating anything |
| `python3 scripts/fetch/fetch_metadata_bulk.py` | Bulk metadata fetch from arXiv |
| `python3 scripts/fetch/saturate_papers.py` | Comprehensive saturation with 150+ queries |
| `python3 scripts/analysis/generate_analysis.py` | Generate D3.js visualization |

## PR Process

1. Fork this repository
2. Create a branch: `git checkout -b add-paper-name`
3. Edit `papers.yaml` to add your paper entry
4. Run the validator: `python3 scripts/validate_papers.py`
5. Run the README generator: `python3 scripts/generate_readme.py`
6. Commit your changes
7. Open a pull request

## PR Checklist

- [ ] Added entry to `papers.yaml` (not `README.md`)
- [ ] Used normalized URL format (`https://arxiv.org/abs/XXXX`)
- [ ] Checked for duplicates (searched by title and URL)
- [ ] Ran `python3 scripts/validate_papers.py` — no errors
- [ ] Ran `python3 scripts/generate_readme.py` — README updated
- [ ] Used correct date format (YYYY-MM)
- [ ] Used valid category and subcategory from the taxonomy
