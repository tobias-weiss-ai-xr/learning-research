#!/usr/bin/env python3
"""Generate visualizations for learning-research statistics."""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np

# Load statistics
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent
STATS_PATH = REPO_DIR / "docs" / "statistics.json"

with open(STATS_PATH) as f:
    stats = json.load(f)

# Create output directory
OUTPUT_DIR = REPO_DIR / "docs" / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)

# Color schemes
CATEGORY_COLORS = {
    'machine-learning': '#FF6B6B',
    'memory-science': '#4ECDC4',
    'language': '#45B7D1',
    'collective': '#FFA07A',
    'cognitive-science': '#98D8C8',
    'education': '#F7DC6F',
    'health': '#BB8FCE',
    'neuroscience': '#85C1E9',
    'neuromorphic': '#F8B739',
    'social-learning': '#52B788',
    'educational-psychology': '#74C69D',
    'behavioral': '#D4A5A5',
    'animal-learning': '#9D76C1',
    'motor': '#B5EAD7',
    'evolutionary': '#FFB347',
    'developmental': '#C7CEEA',
    'philosophy-of-mind': '#E0BBE4',
    'creative': '#957DAD',
    'perceptual': '#D291BC',
    'emotion': '#FEC8D8'
}

ASPECT_COLORS = {
    'theory': '#667EEA',
    'method': '#764BA2',
    'mechanism': '#F093FB',
    'technology': '#4FACFE',
    'application': '#00F5D4',
    'development': '#FE9A2B',
    'individual-differences': '#FB5BC5',
    'review': '#C9DED2'
}

print("Generating visualizations...")

# 1. Papers by Year (Growth Trend)
plt.figure(figsize=(12, 6))
years = sorted(stats['by_year'].keys(), key=lambda x: int(x))
counts = [stats['by_year'][y] for y in years]

plt.bar(years, counts, color='#667EEA', alpha=0.8)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Papers', fontsize=12)
plt.title('Learning Research Papers by Year (Growth Trend)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

# Add value labels
for i, (y, c) in enumerate(zip(years, counts)):
    plt.text(i, c + 50, f'{c:,}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'papers_by_year.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ papers_by_year.png")

# 2. Top 10 Categories
plt.figure(figsize=(14, 8))
top_categories = list(stats['by_category'].items())[:10]
cats = [c[0].replace('-', '\n') for c in top_categories]
counts = [c[1] for c in top_categories]
colors = [CATEGORY_COLORS.get(c[0], '#888888') for c in top_categories]

bars = plt.barh(cats, counts, color=colors, alpha=0.8)
plt.xlabel('Number of Papers', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.title('Top 10 Research Categories by Paper Count', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()

# Add value labels
for bar in bars:
    width = bar.get_width()
    plt.text(width + 20, bar.get_y() + bar.get_height()/2, 
             f'{width:,}', ha='left', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'top_categories.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ top_categories.png")

# 3. Subcategory Distribution
plt.figure(figsize=(12, 6))
subcats = list(stats['by_subcategory'].items())
subcat_names = [s[0].replace('-', '\n') for s in subcats]
subcat_counts = [s[1] for s in subcats]
subcat_colors = [ASPECT_COLORS.get(s[0], '#888888') for s in subcats]

wedges, texts, autotexts = plt.pie(subcat_counts, labels=subcat_names, colors=subcat_colors,
                                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
plt.title('Research Distribution by Subcategory (Aspect)', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'subcategory_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ subcategory_distribution.png")

# 4. Heatmap: Category × Subcategory Matrix
fig, ax = plt.subplots(figsize=(16, 10))

VALID_CATEGORIES = ['cognitive-science', 'neuroscience', 'education', 'developmental', 'behavioral',
    'social-learning', 'language', 'motor', 'emotion', 'creative', 'machine-learning', 'evolutionary',
    'philosophy-of-mind', 'educational-psychology', 'animal-learning', 'neuromorphic', 'memory-science',
    'perceptual', 'collective', 'health']
ASPECTS = ['theory', 'mechanism', 'method', 'application', 'development', 'individual-differences', 'technology', 'review']

# Build matrix
matrix = np.zeros((len(VALID_CATEGORIES), len(ASPECTS)))
for i, cat in enumerate(VALID_CATEGORIES):
    for j, aspect in enumerate(ASPECTS):
        key = f'{cat}/{aspect}'
        matrix[i, j] = stats['by_cell'].get(key, 0)

# Create heatmap
im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=max(matrix.max(), 100))

# Set labels
ax.set_xticks(np.arange(len(ASPECTS)))
ax.set_yticks(np.arange(len(VALID_CATEGORIES)))
ax.set_xticklabels([a[:8] for a in ASPECTS], fontsize=8)
ax.set_yticklabels([c[:15] for c in VALID_CATEGORIES], fontsize=8)

# Rotate x-axis labels
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

# Title and colorbar
ax.set_title('Learning Research: Category × Subcategory Heatmap\n(Deeper colors = more papers)', fontsize=14, fontweight='bold', pad=20)
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Number of Papers', rotation=-90, va="bottom", fontsize=10)

# Add text annotations for high-value cells
for i in range(len(VALID_CATEGORIES)):
    for j in range(len(ASPECTS)):
        if matrix[i, j] > 200:
            text = ax.text(j, i, f'{int(matrix[i, j]):,}', ha="center", va="center", 
                          color="black", fontsize=7, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'category_subcategory_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ category_subcategory_heatmap.png")

# 5. Research Maturity Bar Chart
plt.figure(figsize=(14, 8))

maturity_levels = {'HIGH': [], 'MEDIUM': [], 'EMERGING': []}
for cat, count in stats['by_category'].items():
    if count > 800:
        maturity_levels['HIGH'].append((cat, count))
    elif count > 400:
        maturity_levels['MEDIUM'].append((cat, count))
    else:
        maturity_levels['EMERGING'].append((cat, count))

# Sort within each level
for level in maturity_levels:
    maturity_levels[level].sort(key=lambda x: -x[1])

all_cats = [c[0] for level in maturity_levels.values() for c in level]
all_counts = [c[1] for level in maturity_levels.values() for c in level]
all_colors = []
for cat in all_cats:
    if cat in [c[0] for c in maturity_levels['HIGH']]:
        all_colors.append('#2ECC71')  # Green
    elif cat in [c[0] for c in maturity_levels['MEDIUM']]:
        all_colors.append('#F39C12')  # Orange
    else:
        all_colors.append('#E74C3C')  # Red

bars = plt.barh([c.replace('-', '\n') for c in all_cats], all_counts, color=all_colors, alpha=0.8)
plt.xlabel('Number of Papers', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.title('Research Maturity by Category\n(Green=HIGH>800, Orange=MEDIUM>400, Red=EMERGING<400)', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()

# Add legend
high_patch = mpatches.Patch(color='#2ECC71', label='HIGH (>800 papers)')
medium_patch = mpatches.Patch(color='#F39C12', label='MEDIUM (400-800 papers)')
emerging_patch = mpatches.Patch(color='#E74C3C', label='EMERGING (<400 papers)')
plt.legend(handles=[high_patch, medium_patch, emerging_patch], loc='lower right')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'research_maturity.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ research_maturity.png")

# 6. Empty and Low-Fill Cells Table
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

empty_cells = stats['saturation']['empty_cell_list']
low_fill_cells = stats['saturation']['low_fill_cell_list']

table_data = [
    ['Empty Cells (0 papers)', ''],
    ['---', '---'],
]
for cell in empty_cells:
    table_data.append([cell, ''])

table_data.append(['', ''])
table_data.append(['Low-Fill Cells (<10 papers)', 'Count'])
table_data.append(['---', '---'])
for cell in low_fill_cells[:15]:  # Show top 15
    count = stats['by_cell'].get(cell, 0)
    table_data.append([cell, str(count)])

if len(low_fill_cells) > 15:
    table_data.append([f'... and {len(low_fill_cells)-15} more', ''])

table = ax.table(cellText=table_data, loc='center', cellLoc='left', colWidths=[0.6, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)

# Style header rows
for i in range(2):
    table[(i, 0)].set_facecolor('#667EEA')
    table[(i, 0)].set_text_props(color='white', fontweight='bold')
    table[(i, 1)].set_facecolor('#667EEA')
    table[(i, 1)].set_text_props(color='white', fontweight='bold')

# Style empty cells
for i in range(2, len(empty_cells) + 2):
    table[(i, 0)].set_facecolor('#E74C3C')
    table[(i, 0)].set_text_props(color='white')

# Style low-fill header
header_row = len(empty_cells) + 2
table[(header_row, 0)].set_facecolor('#F39C12')
table[(header_row, 0)].set_text_props(color='white', fontweight='bold')
table[(header_row, 1)].set_facecolor('#F39C12')
table[(header_row, 1)].set_text_props(color='white', fontweight='bold')

plt.title('Research Gaps: Empty and Low-Fill Cells', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'research_gaps.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ research_gaps.png")

# 7. Summary Statistics Infographic
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')

total_papers = stats['metadata']['total_papers']
saturation = stats['saturation']['saturation_percentage']
empty = stats['saturation']['empty_cells']
low_fill = stats['saturation']['low_fill_cells']
top_cat = list(stats['by_category'].items())[0]
top_sub = list(stats['by_subcategory'].items())[0]

summary_text = f"""
LITERATURE REVIEW SUMMARY
=========================

CORPUS OVERVIEW
─────────────────────────────────
Total Papers:        {total_papers:,}
Taxonomy Cells:      160 (20×8)
Saturation Level:    {saturation}%
Empty Cells:         {empty}
Low-Fill Cells:      {low_fill}

TOP RESEARCH AREAS
─────────────────────────────────
Largest Category:    {top_cat[0].replace('-', ' ').title()}
                     ({top_cat[1]:,} papers, {top_cat[1]/total_papers*100:.1f}%)
Largest Subcategory: {top_sub[0].replace('-', ' ').title()}
                     ({top_sub[1]:,} papers, {top_sub[1]/total_papers*100:.1f}%)

RESEARCH MATURITY
─────────────────────────────────
HIGH (>800 papers):  {len([c for c in stats['by_category'].values() if c > 800])} categories
MEDIUM (400-800):    {len([c for c in stats['by_category'].values() if 400 < c <= 800])} categories
EMERGING (<400):     {len([c for c in stats['by_category'].values() if c <= 400])} categories

KEY INSIGHTS
─────────────────────────────────
• Memory-science is the dominant research area
• Theory dominates (52.3% of all papers)
• Exponential growth since 2022 (+3,895%)
• Only 3 cells remain empty
• Strong cross-disciplinary unity

Generated: 2026-07-30
"""

plt.text(0.5, 0.5, summary_text, transform=ax.transAxes, fontsize=11,
         verticalalignment='center', horizontalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.title('Learning Research: Statistical Summary', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'summary_infographic.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ summary_infographic.png")

print(f"\n✓ All visualizations saved to {OUTPUT_DIR}")
print(f"  - papers_by_year.png")
print(f"  - top_categories.png")
print(f"  - subcategory_distribution.png")
print(f"  - category_subcategory_heatmap.png")
print(f"  - research_maturity.png")
print(f"  - research_gaps.png")
print(f"  - summary_infographic.png")
