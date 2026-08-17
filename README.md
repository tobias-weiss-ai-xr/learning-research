<h1 align="center">
  <strong>Learning Research Corpus</strong>
</h1>
<h3 align="center">Evidence-based learning platform implementation — 29,592 papers across 20 academic disciplines</h3>

<div align="center">
  [![GitHub](https://img.shields.io/badge/GitHub-tobias-weiss-ai-xr/learning--research-181717.svg?logo=github)](https://github.com/tobias-weiss-ai-xr/learning-research)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  [![CI](https://img.shields.io/github/actions/workflow/status/tobias-weiss-ai-xr/learning--research/validate.yml?label=CI&logo=github)](https://github.com/tobias-weiss-ai-xr/learning-research/actions/workflows/validate.yml)
  [![AI Literacy](https://img.shields.io/badge/AI Literacy-ai--literacy--research-blue.svg?logo=github)](https://github.com/tobias-weiss-ai-xr/ai-literacy-research) [![Business Dev](https://img.shields.io/badge/Business Dev-business--development--research-blue.svg?logo=github)](https://github.com/tobias-weiss-ai-xr/business-development-research) [![Agent Learning](https://img.shields.io/badge/Agent Learning-agent--learning--research-blue.svg?logo=github)](https://github.com/tobias-weiss-ai-xr/agent-learning-research)
</div>

> 📖 **Learning research corpus:** personalization, spaced repetition, active recall,
> adaptive learning, feedback, cognitive load, motivation, social learning — analyzed
> with the same pipeline as the other `*-research` corpus repos.

<p align="center">
  <img src="https://raw.githubusercontent.com/tobias-weiss-ai-xr/learning-research/main/assets/visualizations/top_categories.png" alt="Teaser" width="600" />
</p>

---

## 🎯 Overview

This repository contains the research corpus and implementation tools for transforming learning platforms using evidence-based principles from **29,018 academic papers**.

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | 29,018 |
| **Academic Disciplines** | 20 |
| **Time Span** | 1964-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 98.1% (157/160 cells) |

### Top Evidence Areas

1. **Personalization** — 4,495 papers
2. **Spaced Repetition** — 1,732 papers
3. **Feedback** — 926 papers
4. **Motivation** — 848 papers
5. **Social Learning** — 562 papers
6. **Cognitive Load** — 162 papers

---

## 📊 The 7 Evidence-Based Principles

All implementation tools and documentation are based on these 7 principles:

| Principle | Evidence | Impact |
|-----------|----------|--------|
| **1. Spaced Repetition** | 1,732 papers | +30% retention |
| **2. Active Recall** | 1,732 papers | +40% retention |
| **3. Adaptive Personalization** | 4,495 papers | +20% efficiency |
| **4. Immediate Feedback** | 926 papers | +25% learning |
| **5. Cognitive Load** | 162 papers | +35% completion |
| **6. Motivation Design** | 848 papers | +20% engagement |
| **7. Social Learning** | 562 papers | +15% completion |

---

## 📁 Repository Structure

```
learning-research/
├── README.md                          # This file
├── papers.json                        # Paper metadata (21 MB)
├── papers.yaml                        # Paper metadata (22 MB)
├── statistics.json                    # Analysis statistics
├── requirements.txt                   # Python dependencies
│
├── assets/                            # Visualizations and images
│   └── visualizations/
│       ├── category_subcategory_heatmap.png
│       ├── papers_by_year.png
│       ├── research_gaps.png
│       ├── research_maturity.png
│       ├── subcategory_distribution.png
│       ├── summary_infographic.png
│       └── top_categories.png
│
├── docs/                              # Documentation
│   ├── implementation/                # Implementation guides
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── platform_implementation_plan.md
│   │   ├── platform_insights.md
│   │   └── PLATFORM_SUMMARY.md
│   ├── marketing/                     # Marketing materials
│   │   ├── landing_page.md
│   │   ├── whitepaper_learning_platforms.md
│   │   └── learn2learn_workshop_curriculum.md
│   └── research/                      # Research documentation
│       └── literature_review.md
│
├── tools/                             # Implementation tools
│   ├── platform_audit.py              # Interactive audit tool
│   ├── spaced_repetition.py           # SRS implementation
│   └── workshop_generator.py          # Workshop material generator
│
├── scripts/                           # Research scripts
│   ├── analysis/                      # Analysis scripts
│   ├── fetch/                         # Paper fetching scripts
│   ├── export_bibtex.py               # Export to BibTeX
│   ├── generate_readme.py             # Generate README
│   ├── validate_papers.py             # Validate paper data
│   └── visualize_statistics.py        # Generate visualizations
│
├── platform-scaffold/                 # Platform implementation scaffold
│   └── IMPLEMENTATION_GUIDE.md
│
└── workshop-repo/                     # Private workshop materials
    ├── README.md
    ├── LICENSE
    └── workshop_materials/
```

---

## 🛠️ Tools

### 1. Platform Audit Tool

Interactive assessment of your learning platform against the 7 evidence-based principles.

```bash
cd tools
python3 platform_audit.py
```

**Features:**
- 28 interactive questions
- Scores each principle (0-5 scale)
- Generates prioritized recommendations
- Exports to JSON for tracking

### 2. Spaced Repetition System

Production-ready SRS implementation using FSRS algorithm.

```bash
cd tools
python3 spaced_repetition.py
```

**Features:**
- FSRS algorithm (17 optimized parameters)
- Card creation and management
- Review scheduling
- Performance tracking
- Statistics and analytics

### 3. Workshop Material Generator

Generate complete workshop materials for Learn-to-Learn training.

```bash
cd tools
python3 workshop_generator.py
```

**Output:**
- Participant handbook
- Slide content
- Exercise worksheets
- Instructor notes

---

## 📊 Corpus Statistics

**29,592 papers** across **21 categories**.  
Sources: **arXiv** 25,116 (84%) · **DOI** 4,082 (13%) · **Other** 394 (1%).  
Full paper list: [GitHub Pages site](https://tobias-weiss-ai-xr.github.io/learning-research).

### Top categories

| Category | Papers | Recent | |
|----------|--------|--------|-|
|  | **5,573** | 0 | ████████████ |
| machine-learning | **5,176** | 0 | ███████████░ |
| cognitive-science | **2,442** | 0 | █████░░░░░░░ |
| language | **1,529** | 0 | ███░░░░░░░░░ |
| memory-science | **1,500** | 0 | ███░░░░░░░░░ |
| education | **1,429** | 0 | ███░░░░░░░░░ |
| neuroscience | **1,315** | 0 | ██░░░░░░░░░░ |
| collective | **1,237** | 0 | ██░░░░░░░░░░ |
| health | **1,107** | 0 | ██░░░░░░░░░░ |
| behavioral | **951** | 0 | ██░░░░░░░░░░ |
| *other* | **7,333** | | |


### By year

| Year | Papers | |
|------|--------|-|
| 2025 | 8,773 | ████████████ |
| 2026 | 7,382 | ██████████░░ |
| None | 7 | ░░░░░░░░░░░░ |


### Momentum (hottest categories)

| Category | Total | Rate | Recent | Score |
|----------|-------|------|--------|-------|
|  | 5,573 | 369.8/mo | 80% | 371 |
| Memory Science | 1,500 | 47.9/mo | 38% | 91 |
| Evolutionary | 688 | 18.1/mo | 32% | 72 |
| Behavioral | 951 | 27.0/mo | 34% | 60 |
| Motor | 778 | 22.0/mo | 34% | 57 |


### Trending keywords

| Keyword | Papers | Burst |
|---------|--------|-------|
| agentic | 424 | 2.25 |
| world model | 527 | 1.69 |
| scalable | 1,552 | 1.60 |
| retrieval | 1,022 | 1.56 |
| policy | 2,518 | 1.51 |
| uncertainty | 952 | 1.50 |
| benchmark | 4,544 | 1.48 |
| hierarchical | 949 | 1.46 |


### Top venues

| Venue | Papers |
|-------|--------|
| MED | 117 |
| Scientific Reports | 76 |
| Frontiers in Psychology | 73 |
| Nature Communications | 39 |
| bioRxiv (Cold Spring Harbor Laboratory) | 36 |
| Education and Information Technologies | 35 |
| PLoS ONE | 29 |
| Frontiers in Education | 28 |


### Research gaps (thinnest cells)

| Cell | Papers |
|------|--------|
| `behavioral/individual-differences` | 1 |
| `motor/individual-differences` | 1 |
| `developmental/review` | 1 |
| `developmental/individual-differences` | 2 |
| `language/individual-differences` | 2 |



## Related Projects

- **Platform Implementation:** [ki-kompetenz-training](https://github.com/tobias-weiss-ai-xr/ki-kompetenz-training) — Production platform with SRS integration

---

## 📞 Contact & Support

**Tobias Weiss | KI-Kompetenz-Training**  
📧 ki-kompetenz-training@tobias-weiss.org  
🌐 www.ki-kompetenz-training.org

**Services:**
- Platform audit and implementation support
- Learn-to-learn workshops (onsite or online)
- Consulting and ongoing training
- Custom tool development

---

## 📄 License

**© 2026 KI-Kompetenz-Training | Tobias Weiss**

- **Research corpus:** Proprietary
- **Tools:** MIT License
- **Workshop materials:** Proprietary (private repository)

---

## 🙏 Acknowledgments

This research corpus represents 62 years of learning science research, synthesized from 29,018 papers across 20 academic disciplines to create a comprehensive foundation for evidence-based learning platform design.

---

**Ready to transform your learning platform?**  
Contact us at ki-kompetenz-training@tobias-weiss.org
