#!/usr/bin/env python3
"""Generate D3.js visualization from papers.yaml."""

import json
import re
import os
import yaml
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORY_DISPLAY = {
    "cognitive-science": "Cognitive Science",
    "neuroscience": "Neuroscience",
    "education": "Education",
    "developmental": "Developmental",
    "behavioral": "Behavioral",
    "social-learning": "Social Learning",
    "language": "Language",
    "motor": "Motor",
    "emotion": "Emotion",
    "creative": "Creative",
    "machine-learning": "Machine Learning",
    "evolutionary": "Evolutionary",
    "philosophy-of-mind": "Philosophy of Mind",
    "educational-psychology": "Educational Psychology",
    "animal-learning": "Animal Learning",
    "neuromorphic": "Neuromorphic",
    "memory-science": "Memory Science",
    "perceptual": "Perceptual",
    "collective": "Collective",
    "health": "Health",
}

CATEGORY_ORDER = list(CATEGORY_DISPLAY.keys())

SUBCATEGORY_ORDER = [
    "theory",
    "mechanism",
    "method",
    "application",
    "development",
    "individual-differences",
    "technology",
    "review",
]

CAT_COLORS = [
    "#58a6ff",
    "#3fb950",
    "#d29922",
    "#f0883e",
    "#db6d8a",
    "#7ee787",
    "#a5d6ff",
    "#79c0ff",
    "#ffa657",
    "#ff7b72",
    "#d2a8ff",
    "#79c0ff",
    "#56d4dd",
    "#b392f0",
    "#ffc680",
    "#85e89d",
    "#f778ba",
    "#68a4ff",
    "#ffdf5d",
    "#a371f7",
]

with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
    _data = yaml.safe_load(f)
entries = _data.get("papers", [])
print(f"Parsed {len(entries)} papers")

cat_counter = Counter()
subcat_counter = Counter()
pub_dates = []
venue_counter = Counter()

for e in entries:
    cat = e.get("category", "unknown")
    sub = e.get("subcategory", "unknown")
    cat_counter[cat] += 1
    subcat_counter[sub] += 1
    d = e.get("date", "")
    if d and len(d) >= 7:
        pub_dates.append((d[:7], cat, sub))
    v = e.get("venue", "")
    if v:
        venue_counter[v] += 1
    else:
        venue_counter["Unknown/None"] += 1

total = len(entries)
cat_vals = [cat_counter.get(c, 0) for c in CATEGORY_ORDER]
subcat_vals = [subcat_counter.get(s, 0) for s in SUBCATEGORY_ORDER]

ym_set = sorted(set(ym for ym, _, _ in pub_dates))
if not ym_set:
    ym_set = ["2024-01"]

ym_cat_counter = defaultdict(lambda: Counter())
ym_total_counter = Counter()
for ym, cat, _ in pub_dates:
    ym_cat_counter[ym][cat] += 1
    ym_total_counter[ym] += 1

nodes = []
edges = []
edge_set = set()
venue_groups = defaultdict(list)

for i, e in enumerate(entries):
    d = e.get("date", "")
    year = d[:4] if d and len(d) >= 4 else "2026"
    nodes.append(
        {
            "id": i,
            "title": e.get("title", ""),
            "cat": e.get("category", "unknown"),
            "sub": e.get("subcategory", "unknown"),
            "year": year,
            "url": e.get("url", ""),
        }
    )
    v = e.get("venue", "")
    if v:
        venue_groups[v].append(i)

for v, ids in venue_groups.items():
    if len(ids) < 2:
        continue
    ids_sorted = sorted(ids)
    for idx in range(len(ids_sorted)):
        for jdx in range(idx + 1, min(idx + 6, len(ids_sorted))):
            key = (ids_sorted[idx], ids_sorted[jdx])
            if key not in edge_set:
                edge_set.add(key)
                edges.append({"source": ids_sorted[idx], "target": ids_sorted[jdx]})

node_degree = Counter()
for edge in edges:
    s = edge["source"]
    t = edge["target"]
    node_degree[s] += 1
    node_degree[t] += 1

max_degree = max(node_degree.values()) if node_degree else 1
for i, n in enumerate(nodes):
    n["degree"] = node_degree.get(i, 0)
    n["normDegree"] = round(node_degree.get(i, 0) / max_degree, 3)


def js_str(s):
    return json.dumps(s)


cat_color_map_js = "{"
for i, c in enumerate(CATEGORY_ORDER):
    cat_color_map_js += f'"{c}": "{CAT_COLORS[i % len(CAT_COLORS)]}",'
cat_color_map_js += "}"

STOPWORDS = {
    "the",
    "a",
    "an",
    "of",
    "for",
    "in",
    "to",
    "and",
    "on",
    "with",
    "via",
    "by",
    "from",
    "as",
    "at",
    "is",
    "that",
    "this",
    "its",
    "their",
    "our",
    "are",
    "based",
    "using",
    "toward",
    "towards",
    "across",
    "over",
    "through",
    "into",
    "between",
    "after",
    "under",
    "during",
    "without",
    "before",
    "all",
    "each",
    "both",
    "more",
    "than",
    "most",
    "some",
    "any",
    "new",
    "large",
    "long",
    "short",
    "high",
    "low",
    "multi",
    "self",
    "co",
    "study",
    "learning",
}
word_counter = Counter()
for e in entries:
    title = e.get("title", "")
    words = re.findall(r"[A-Za-z][A-Za-z-]+", title)
    for w in words:
        wl = w.lower()
        if len(wl) > 2 and wl not in STOPWORDS:
            word_counter[wl] += 1
top_words = word_counter.most_common(20)
word_labels = [w for w, _ in top_words]
word_values = [n for _, n in top_words]

top_venues = [(v, n) for v, n in venue_counter.most_common(10) if v != "Unknown/None"]
if venue_counter.get("Unknown/None", 0) > 0:
    top_venues.append(("Unknown/None", venue_counter["Unknown/None"]))

HTML = (
    """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Learning Research - Analysis</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0f1117; color: #e1e4e8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; }
h1 { font-size: 1.8rem; margin-bottom: 8px; color: #f0f6fc; }
h2 { font-size: 1.2rem; margin: 24px 0 12px; color: #79c0ff; }
p { color: #8b949e; margin-bottom: 16px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 24px; }
.stat-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; }
.stat-card .num { font-size: 1.8rem; font-weight: 700; color: #58a6ff; }
.stat-card .label { font-size: 0.85rem; color: #8b949e; margin-top: 4px; }
.chart-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.chart-box { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; overflow: hidden; }
.chart-box.full { grid-column: 1 / -1; }
canvas { max-height: 400px; }
table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
th { text-align: left; padding: 8px 10px; border-bottom: 2px solid #30363d; color: #79c0ff; }
td { padding: 7px 10px; border-bottom: 1px solid #21262d; }
a { color: #58a6ff; text-decoration: none; }
.legend { display: flex; gap: 12px; flex-wrap: wrap; margin: 8px 0; font-size: 0.8rem; }
.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
#forceGraph { width: 100%; height: 550px; background: #0d1117; border-radius: 6px; cursor: grab; }
#forceGraph:active { cursor: grabbing; }
.tooltip { position: absolute; background: #1c2128; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; font-size: 0.8rem; pointer-events: none; color: #e1e4e8; max-width: 300px; z-index: 100; }
@media (max-width: 768px) { .chart-row { grid-template-columns: 1fr; } }
</style>
</head>
<body>

<h1>Learning Research Analysis</h1>
<p>Analysis of """
    + str(total)
    + """ papers on learning across all disciplines</p>

<div class="stats-grid">
  <div class="stat-card"><div class="num">"""
    + str(total)
    + """</div><div class="label">Total Papers</div></div>
</div>

<h2>Paper Relationship Graph</h2>
<div class="chart-box full">
<div class="legend">
  <span style="color:#8b949e;">Node size = degree centrality | Click for paper</span>
</div>
<svg id="forceGraph"></svg>
<div id="tooltip" class="tooltip" style="display:none"></div>
</div>

<div class="chart-row">
  <div class="chart-box"><canvas id="catChart"></canvas></div>
  <div class="chart-box"><canvas id="subcatChart"></canvas></div>
</div>

<h2>Most Common Title Keywords</h2>
<div class="chart-box full">
<canvas id="wordChart"></canvas>
</div>

<h2>Top Venues</h2>
<div class="chart-box full">
<canvas id="venueChart"></canvas>
</div>

<script>
const catLabels = """
    + js_str(CATEGORY_ORDER)
    + """;
const catValues = """
    + js_str(cat_vals)
    + """;
const catColors = """
    + js_str([CAT_COLORS[i % len(CAT_COLORS)] for i in range(len(CATEGORY_ORDER))])
    + """;
const subcatLabels = """
    + js_str(SUBCATEGORY_ORDER)
    + """;
const subcatValues = """
    + js_str(subcat_vals)
    + """;

const graphNodes = """
    + js_str(nodes)
    + """;
const graphEdges = """
    + js_str(edges)
    + """;
const catColorMap = """
    + cat_color_map_js
    + """;

const wordLabels = """
    + js_str(word_labels)
    + """;
const wordValues = """
    + js_str(word_values)
    + """;

const venueLabels = """
    + js_str([v for v, _ in top_venues])
    + """;
const venueValues = """
    + js_str([n for _, n in top_venues])
    + """;

const width = document.getElementById('forceGraph').clientWidth;
const height = 550;
const svg = d3.select('#forceGraph').attr('viewBox', [0, 0, width, height]);
const g = svg.append('g');
svg.call(d3.zoom().scaleExtent([0.3, 4]).on('zoom', (event) => { g.attr('transform', event.transform); }));
const tooltip = d3.select('#tooltip');

const sim = d3.forceSimulation(graphNodes)
  .force('link', d3.forceLink(graphEdges).id(d => d.id).distance(60).strength(0.3))
  .force('charge', d3.forceManyBody().strength(-25))
  .force('center', d3.forceCenter(width/2, height/2))
  .force('collision', d3.forceCollide().radius(d => 3 + d.normDegree * 10));

const link = g.append('g').selectAll('line').data(graphEdges).join('line')
  .attr('stroke', '#30363d').attr('stroke-width', 0.5).attr('stroke-opacity', 0.3);

const node = g.append('g').selectAll('circle').data(graphNodes).join('circle')
  .attr('r', d => 3 + d.normDegree * 10)
  .attr('fill', d => catColorMap[d.cat] || '#8b949e')
  .attr('stroke', '#0d1117').attr('stroke-width', 1).attr('opacity', 0.8)
  .call(d3.drag()
    .on('start', (event, d) => { if (!event.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
    .on('end', (event, d) => { if (!event.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }))
  .on('mouseover', (event, d) => {
    tooltip.style('display', 'block')
      .html('<strong>' + d.title + '</strong><br>Category: ' + d.cat + ' | Sub: ' + d.sub + ' | Year: ' + d.year)
      .style('left', (event.pageX + 12) + 'px').style('top', (event.pageY - 10) + 'px');
  })
  .on('mouseout', () => tooltip.style('display', 'none'))
  .on('click', (event, d) => { if (d.url) window.open(d.url, '_blank'); });

sim.on('tick', () => {
  link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  node.attr('cx', d => d.x).attr('cy', d => d.y);
});

new Chart(document.getElementById('catChart'), {
  type: 'bar',
  data: { labels: catLabels, datasets: [{ label: 'Papers', data: catValues, backgroundColor: catColors, borderRadius: 4 }] },
  options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { color: '#8b949e' }, grid: { color: '#21262d' } }, y: { ticks: { color: '#8b949e', font: { size: 10 } }, grid: { color: '#21262d' } } } }
});

new Chart(document.getElementById('subcatChart'), {
  type: 'bar',
  data: { labels: subcatLabels, datasets: [{ label: 'Papers', data: subcatValues, backgroundColor: '#58a6ff', borderRadius: 4 }] },
  options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { color: '#8b949e' }, grid: { color: '#21262d' } }, y: { ticks: { color: '#8b949e' }, grid: { color: '#21262d' } } } }
});

new Chart(document.getElementById('wordChart'), {
  type: 'bar',
  data: { labels: wordLabels, datasets: [{ label: 'Occurrences', data: wordValues, backgroundColor: '#58a6ff', borderRadius: 3 }] },
  options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { color: '#8b949e' }, grid: { color: '#21262d' } }, y: { ticks: { color: '#8b949e', font: { size: 11 } }, grid: { color: '#21262d' } } } }
});

new Chart(document.getElementById('venueChart'), {
  type: 'bar',
  data: { labels: venueLabels, datasets: [{ label: 'Papers', data: venueValues, backgroundColor: '#3fb950', borderRadius: 3 }] },
  options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { color: '#8b949e' }, grid: { color: '#21262d' } }, y: { ticks: { color: '#8b949e', font: { size: 10 } }, grid: { color: '#21262d' } } } }
});
</script>
</body>
</html>"""
)

with open(
    os.path.join(BASE, "docs", "graph_analysis.html"), "w", encoding="utf-8"
) as f:
    f.write(HTML)
print(f"Wrote docs/graph_analysis.html ({len(HTML)} bytes)")
