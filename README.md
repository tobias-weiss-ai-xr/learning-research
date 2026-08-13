# Learning Research Corpus

**Evidence-based learning platform implementation** — Analysis of 17,165 research papers across 20 academic disciplines.

**Author:** Tobias Weiss  
**Contact:** ki-kompetenz-training@tobias-weiss.org  
**Website:** www.ki-kompetenz-training.org

---

## 🎯 Overview

This repository contains the research corpus and implementation tools for transforming learning platforms using evidence-based principles from **27,517 academic papers**.

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | 27,517 |
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

## 📚 Documentation

### Implementation Guides

| Document | Purpose | Size |
|----------|---------|------|
| `docs/implementation/IMPLEMENTATION_SUMMARY.md` | Quick reference | 7.8 KB |
| `docs/implementation/platform_implementation_plan.md` | Step-by-step guide | 19 KB |
| `docs/implementation/platform_insights.md` | Design principles | 22 KB |
| `docs/implementation/PLATFORM_SUMMARY.md` | Checklist | 6.2 KB |

### Marketing Materials

| Document | Purpose | Size |
|----------|---------|------|
| `docs/marketing/landing_page.md` | Website content | 12 KB |
| `docs/marketing/whitepaper_learning_platforms.md` | Sales whitepaper | 22 KB |
| `docs/marketing/learn2learn_workshop_curriculum.md` | Workshop curriculum | 19 KB |

### Research Documentation

| Document | Purpose | Size |
|----------|---------|------|
| `docs/research/literature_review.md` | Full research synthesis | 21 KB |

---

## 🚀 Quick Start

### 1. Run Platform Audit

```bash
cd tools
python3 platform_audit.py
```

This will assess your current platform and generate recommendations.

### 2. Generate Workshop Materials

```bash
cd tools
python3 workshop_generator.py
```

Materials will be generated in `workshop-repo/workshop_materials/`.

### 3. Test SRS Implementation

```bash
cd tools
python3 spaced_repetition.py
```

This will demonstrate the SRS algorithm and save state to `srs_state.json`.

---

## 📊 Expected Outcomes

### 6 Months After Implementation

| Metric | Target |
|--------|--------|
| 30-day retention | 60% |
| Course completion | 35% |
| Learner satisfaction | 4.0/5 |
| Time to competency | -20% |

### 12 Months After Implementation

| Metric | Target |
|--------|--------|
| 30-day retention | 70%+ |
| Course completion | 40%+ |
| Learner satisfaction | 4.5/5 |
| Time to competency | -35% |

### ROI (Year 1)

| Component | Value |
|-----------|-------|
| Investment | €15,000 - €50,000 |
| Improved retention savings | €150,000+ |
| Improved completion gains | €200,000+ |
| Faster competency | €100,000+ |
| **Total ROI** | **300-500%** |

---

## 🎓 Workshop Offerings

### Onsite Workshop (2 Days)

**Price:** €6,500 (up to 20 participants)

**Content:**
- Day 1: Memory science, active learning, cognitive load
- Day 2: SRS systems, adaptive strategies, motivation, implementation

### Online Course (4 Weeks)

**Price:** €897 per participant

**Content:**
- Weekly live sessions (2 hours)
- Self-paced modules
- Discussion forum
- SRS account setup

---

## 🔗 Related Repositories

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

This research corpus represents 62 years of learning science research, synthesized from 27,517 papers across 20 academic disciplines to create a comprehensive foundation for evidence-based learning platform design.

---

**Ready to transform your learning platform?**  
Contact us at ki-kompetenz-training@tobias-weiss.org
