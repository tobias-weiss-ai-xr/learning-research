# Learning Research Documentation

This directory contains comprehensive analysis, statistics, and visualizations of the learning research corpus.

## Files

| File | Description |
|------|-------------|
| `papers.json` | JSON export of all 13,204 papers |
| `literature_review.md` | **Comprehensive literature review** with Bayesian analysis |
| `statistics.json` | Machine-readable statistics (JSON format) |
| `references.bib` | BibTeX export of all papers |
| `graph_analysis.html` | Interactive D3.js network visualization |
| `visualizations/` | Generated charts and graphs |

## Quick Stats

- **Total Papers:** 13,204
- **Categories:** 20 disciplines
- **Subcategories:** 8 aspects
- **Saturation:** 98.1% (157/160 cells)
- **Empty Cells:** 3
- **Growth:** +3,895% from 2021 to 2022

## Key Findings

### Top 3 Research Areas

1. **memory-science/theory** (884 papers, P=0.0662)
   - Memory systems as central bottleneck for AI agents
   - Episodic memory, working memory, learning to forget

2. **machine-learning/method** (778 papers, P=0.0583)
   - Reinforcement learning, self-supervised learning
   - Continual learning, transfer learning

3. **health/theory** (704 papers, P=0.0528)
   - Health behavior change, medical training
   - Patient education, public health learning

### Emerging Themes (2026)

1. **LLM Agent Memory** - 20 papers
2. **Multi-Agent Systems** - 20 papers
3. **Reinforcement Learning** - 16 papers
4. **Cognitive Models** - 12 papers
5. **Embodied AI/Robotics** - 12 papers

### Research Gaps (Priority Areas)

| Cell | Papers | Priority |
|------|--------|----------|
| memory-science/development | 0 | **CRITICAL** |
| perceptual/application | 0 | **CRITICAL** |
| perceptual/review | 0 | **CRITICAL** |
| education/development | 1 | High |
| developmental/review | 1 | High |

## Visualizations

Located in `visualizations/`:

- `papers_by_year.png` - Growth trend 2000-2026
- `top_categories.png` - Top 10 research categories
- `subcategory_distribution.png` - Aspect distribution pie chart
- `category_subcategory_heatmap.png` - Full 20×8 matrix
- `research_maturity.png` - Maturity classification
- `research_gaps.png` - Empty and low-fill cells
- `summary_infographic.png` - One-page summary

## Analysis Tools

| Script | Description |
|--------|-------------|
| `scripts/visualize_statistics.py` | Generate all visualizations |
| `scripts/export_bibtex.py` | Export to BibTeX format |
| `scripts/generate_readme.py` | Update main README.md |
| `scripts/validate_papers.py` | Validate papers.yaml |

## Bayesian Analysis

The literature review includes Bayesian posterior probability analysis:

**Formula:** P(cell|data) = (count + α) / (N + α×C)

Where:
- N = total papers (13,204)
- C = total cells (160)
- α = smoothing parameter (1)

This provides a statistically rigorous measure of research area importance, accounting for corpus size and cell count.

## Citation

If you use this corpus or analysis in your research:

```bibtex
@misc{learning-research-2026,
  author = {Tobias Weiss and Contributors},
  title = {Learning Research: A Cross-Disciplinary Survey},
  year = {2026},
  url = {https://github.com/tobias-weiss-ai-xr/learning-research},
  note = {13,204 papers across 20 disciplines}
}
```

## Updates

- **2026-07-30:** Literature review v1.0 published
  - 13,204 papers analyzed
  - 98.1% saturation achieved
  - 3 empty cells remaining
  - Bayesian analysis included

---

**Main Repository:** [github.com/tobias-weiss-ai-xr/learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)
