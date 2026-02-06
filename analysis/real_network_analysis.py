"""
FlyWire Real Connectivity Analysis
Week 2 - BETA Track

Builds a real network from FlyWire v630 reciprocal pairs data and
cross-references with neuron functional classifications.

The reciprocal pairs file contains 180,799 neuron pairs that have
bidirectional (mutual) connections. Each pair includes neurotransmitter types.

Analyses:
1. Build directed graph from reciprocal pairs (each pair → 2 directed edges)
2. Basic network statistics and degree distribution
3. Neurotransmitter composition analysis
4. Cross-reference with neuron classifications (rich club, broadcast, integrate, sensory)
5. Hub analysis - identify most connected neurons and their functional roles
6. Triadic closure in the reciprocal subnetwork
7. Community detection

Run with: conda activate research-accelerator && python real_network_analysis.py
"""
import os
import time
from collections import Counter

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ============================================================
# Configuration
# ============================================================
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_SCRIPT_DIR, "..", "data")
CSV_DIR = os.path.join(DATA_DIR, "classifications")
RESULTS_DIR = os.path.join(_SCRIPT_DIR, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 60)
print("FlyWire Real Connectivity Analysis - BETA Track Week 2")
print("=" * 60)

# ============================================================
# 1. Load Real Connectivity Data
# ============================================================
print("\n1. Loading real FlyWire reciprocal pairs...")
t0 = time.time()

pairs_df = pd.read_csv(os.path.join(DATA_DIR, "v630-all-reciprocal-pairs-s1.csv"))
print(f"  Loaded {len(pairs_df):,} reciprocal pairs in {time.time()-t0:.1f}s")
print(f"  Columns: {list(pairs_df.columns)}")

# Get unique neurons
all_neurons = set(pairs_df["n1"].values) | set(pairs_df["n2"].values)
print(f"  Unique neurons: {len(all_neurons):,}")

# Neurotransmitter distribution
nt_counts = Counter(list(pairs_df["n1_nt"]) + list(pairs_df["n2_nt"]))
print(f"\n  Neurotransmitter distribution (across all pair endpoints):")
for nt, count in sorted(nt_counts.items(), key=lambda x: -x[1]):
    print(f"    {nt:>5s}: {count:>8,} ({100*count/sum(nt_counts.values()):.1f}%)")

# ============================================================
# 2. Load Neuron Classifications
# ============================================================
print("\n2. Loading neuron classifications...")

classifications = {}
class_files = {
    "rich_club": "rich_club_neurons.csv",
    "broadcast": "broadcast_neurons.csv",
    "integrate": "integrate_neurons.csv",
    "sensory": "all_sensory.csv",
    "intrinsic_balanced": "intrinsic_balanced_neurons.csv",
}

for label, filename in class_files.items():
    filepath = os.path.join(CSV_DIR, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, header=None, names=["root_id"])
        classifications[label] = set(df["root_id"].values)
        print(f"  {label}: {len(classifications[label]):,} neurons")

# ============================================================
# 3. Build Directed Graph
# ============================================================
print("\n3. Building directed graph from reciprocal pairs...")
t0 = time.time()

# Create node ID mapping (neuron root IDs are large ints)
neuron_list = sorted(all_neurons)
neuron_to_idx = {n: i for i, n in enumerate(neuron_list)}
n_nodes = len(neuron_list)

# Each reciprocal pair → 2 directed edges (n1→n2 and n2→n1)
edges = []
edge_nt_pairs = []  # (n1_nt, n2_nt) for each edge
for _, row in pairs_df.iterrows():
    i = neuron_to_idx[row["n1"]]
    j = neuron_to_idx[row["n2"]]
    edges.append((i, j))
    edges.append((j, i))
    edge_nt_pairs.append((row["n1_nt"], row["n2_nt"]))
    edge_nt_pairs.append((row["n2_nt"], row["n1_nt"]))

G = ig.Graph(n=n_nodes, edges=edges, directed=True)
G.simplify()  # Remove any duplicate edges

print(f"  Built graph in {time.time()-t0:.1f}s")
print(f"  Nodes: {G.vcount():,}")
print(f"  Edges: {G.ecount():,}")
print(f"  Density: {G.density():.6f}")
print(f"  Reciprocity: {G.reciprocity():.4f}")

# Assign neuron classifications as vertex attributes
for label, neuron_set in classifications.items():
    membership = [1 if neuron_list[i] in neuron_set else 0 for i in range(n_nodes)]
    G.vs[label] = membership
    n_in = sum(membership)
    print(f"  Neurons in '{label}' class: {n_in:,} ({100*n_in/n_nodes:.1f}%)")

# ============================================================
# 4. Degree Distribution
# ============================================================
print("\n4. Computing degree distribution...")

in_deg = np.array(G.indegree())
out_deg = np.array(G.outdegree())
total_deg = in_deg + out_deg

print(f"  In-degree:  mean={in_deg.mean():.1f}, median={np.median(in_deg):.0f}, "
      f"max={in_deg.max()}, std={in_deg.std():.1f}")
print(f"  Out-degree: mean={out_deg.mean():.1f}, median={np.median(out_deg):.0f}, "
      f"max={out_deg.max()}, std={out_deg.std():.1f}")
print(f"  Total:      mean={total_deg.mean():.1f}, median={np.median(total_deg):.0f}, "
      f"max={total_deg.max()}")

# ============================================================
# 5. Hub Analysis — Top Neurons by Degree
# ============================================================
print("\n5. Hub analysis — top 20 neurons by total degree...")

top_idx = np.argsort(total_deg)[::-1][:20]
print(f"  {'Rank':>4s}  {'Neuron ID':>20s}  {'In':>5s}  {'Out':>5s}  {'Total':>5s}  Classifications")
print("  " + "-" * 80)

for rank, idx in enumerate(top_idx):
    nid = neuron_list[idx]
    labels = [lbl for lbl in classifications if nid in classifications[lbl]]
    label_str = ", ".join(labels) if labels else "—"
    print(f"  {rank+1:>4d}  {nid:>20d}  {in_deg[idx]:>5d}  {out_deg[idx]:>5d}  "
          f"{total_deg[idx]:>5d}  {label_str}")

# ============================================================
# 6. Classification Enrichment in Reciprocal Network
# ============================================================
print("\n6. Classification enrichment analysis...")

for label, neuron_set in classifications.items():
    # What fraction of reciprocally-connected neurons belong to this class?
    n_in_graph = sum(1 for n in neuron_list if n in neuron_set)
    frac_in_graph = n_in_graph / n_nodes if n_nodes > 0 else 0

    # What fraction of the full class is in our reciprocal network?
    n_total_class = len(neuron_set)
    n_overlap = sum(1 for n in neuron_set if n in all_neurons)
    frac_overlap = n_overlap / n_total_class if n_total_class > 0 else 0

    # Mean degree of neurons in this class vs overall
    class_mask = np.array([1 if neuron_list[i] in neuron_set else 0 for i in range(n_nodes)])
    if class_mask.sum() > 0:
        class_mean_deg = total_deg[class_mask == 1].mean()
        nonclass_mean_deg = total_deg[class_mask == 0].mean() if (class_mask == 0).sum() > 0 else 0
        enrichment = class_mean_deg / nonclass_mean_deg if nonclass_mean_deg > 0 else float('inf')
    else:
        class_mean_deg = 0
        enrichment = 0

    print(f"  {label:>20s}: {n_in_graph:>6,} in graph ({frac_in_graph:>5.1%}), "
          f"{frac_overlap:>5.1%} of class represented, "
          f"mean_deg={class_mean_deg:.1f} vs {nonclass_mean_deg:.1f} "
          f"(enrichment={enrichment:.2f}x)")

# ============================================================
# 7. Neurotransmitter Pair Analysis
# ============================================================
print("\n7. Neurotransmitter pair analysis in reciprocal connections...")

nt_pair_counts = Counter()
for _, row in pairs_df.iterrows():
    pair = tuple(sorted([row["n1_nt"], row["n2_nt"]]))
    nt_pair_counts[pair] += 1

print(f"  {'NT Pair':>15s}  {'Count':>8s}  {'Fraction':>8s}")
print("  " + "-" * 40)
total_pairs = sum(nt_pair_counts.values())
for pair, count in sorted(nt_pair_counts.items(), key=lambda x: -x[1]):
    label = f"{pair[0]}-{pair[1]}"
    print(f"  {label:>15s}  {count:>8,}  {100*count/total_pairs:>7.1f}%")

# ============================================================
# 8. Connected Components
# ============================================================
print("\n8. Connected components...")
components = G.connected_components(mode="weak")
comp_sizes = sorted([len(c) for c in components], reverse=True)
print(f"  Total components: {len(components):,}")
print(f"  Giant component: {comp_sizes[0]:,} nodes ({100*comp_sizes[0]/n_nodes:.1f}%)")
if len(comp_sizes) > 1:
    print(f"  2nd largest: {comp_sizes[1]:,} nodes")
    print(f"  Isolated nodes (degree 0): {sum(1 for s in comp_sizes if s == 1):,}")

# ============================================================
# 9. Local Clustering (Transitivity in Reciprocal Subnetwork)
# ============================================================
print("\n9. Computing clustering coefficient...")
t0 = time.time()

# Global transitivity (fraction of closed triangles)
transitivity = G.transitivity_undirected()
print(f"  Global transitivity: {transitivity:.4f}")

# Mean local clustering
# (For large graphs, compute on a sample)
if n_nodes > 50000:
    sample_idx = np.random.choice(n_nodes, 10000, replace=False)
    local_cc = G.transitivity_local_undirected(vertices=list(sample_idx))
    local_cc = [c for c in local_cc if c == c]  # Remove NaN
    print(f"  Mean local clustering (sample of 10K): {np.mean(local_cc):.4f}")
else:
    local_cc = G.transitivity_local_undirected()
    local_cc = [c for c in local_cc if c == c]  # Remove NaN
    print(f"  Mean local clustering: {np.mean(local_cc):.4f}")

print(f"  Computed in {time.time()-t0:.1f}s")

# ============================================================
# 10. Visualizations
# ============================================================
print("\n10. Generating visualizations...")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# --- A: Degree Distribution (log-log) ---
ax = axes[0, 0]
deg_counts = Counter(total_deg)
degs = sorted(deg_counts.keys())
counts = [deg_counts[d] for d in degs]
ax.scatter(degs, counts, s=10, alpha=0.6, color="steelblue")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Total Degree")
ax.set_ylabel("Count")
ax.set_title("Degree Distribution (log-log)")
ax.grid(True, alpha=0.3)

# --- B: In vs Out Degree ---
ax = axes[0, 1]
ax.scatter(in_deg, out_deg, s=2, alpha=0.2, color="steelblue")
ax.plot([0, max(in_deg.max(), out_deg.max())],
        [0, max(in_deg.max(), out_deg.max())],
        "r--", alpha=0.5, label="in = out")
ax.set_xlabel("In-Degree")
ax.set_ylabel("Out-Degree")
ax.set_title("In-Degree vs Out-Degree")
ax.legend()
ax.grid(True, alpha=0.3)

# --- C: Neurotransmitter Pair Distribution ---
ax = axes[0, 2]
top_nt_pairs = sorted(nt_pair_counts.items(), key=lambda x: -x[1])[:10]
nt_labels = [f"{p[0]}-{p[1]}" for p, _ in top_nt_pairs]
nt_vals = [c for _, c in top_nt_pairs]
colors_nt = plt.cm.Set3(np.linspace(0, 1, len(nt_labels)))
bars = ax.barh(range(len(nt_labels)), nt_vals, color=colors_nt)
ax.set_yticks(range(len(nt_labels)))
ax.set_yticklabels(nt_labels)
ax.set_xlabel("Count")
ax.set_title("Reciprocal Pair NT Composition")
ax.invert_yaxis()
ax.grid(True, alpha=0.3, axis="x")

# --- D: Degree by Classification ---
ax = axes[1, 0]
class_data = []
class_labels_plot = []
for label in ["rich_club", "broadcast", "integrate", "sensory", "intrinsic_balanced"]:
    if label in classifications:
        mask = np.array([1 if neuron_list[i] in classifications[label] else 0
                        for i in range(n_nodes)])
        if mask.sum() > 0:
            class_data.append(total_deg[mask == 1])
            class_labels_plot.append(label.replace("_", "\n"))

# Add "other" category
all_classified = set()
for s in classifications.values():
    all_classified |= s
other_mask = np.array([1 if neuron_list[i] not in all_classified else 0
                       for i in range(n_nodes)])
if other_mask.sum() > 0:
    class_data.append(total_deg[other_mask == 1])
    class_labels_plot.append("other")

bp = ax.boxplot(class_data, labels=class_labels_plot, showfliers=False,
                patch_artist=True)
colors_box = plt.cm.Set2(np.linspace(0, 1, len(class_data)))
for patch, color in zip(bp["boxes"], colors_box):
    patch.set_facecolor(color)
ax.set_ylabel("Total Degree")
ax.set_title("Degree by Neuron Classification")
ax.grid(True, alpha=0.3, axis="y")

# --- E: Classification overlap with reciprocal network ---
ax = axes[1, 1]
class_names = list(classifications.keys())
frac_in_recip = []
for label in class_names:
    neuron_set = classifications[label]
    n_overlap = sum(1 for n in neuron_set if n in all_neurons)
    frac_in_recip.append(n_overlap / len(neuron_set))

colors_bar = plt.cm.Set2(np.linspace(0, 1, len(class_names)))
bars = ax.bar(range(len(class_names)), frac_in_recip, color=colors_bar)
ax.set_xticks(range(len(class_names)))
ax.set_xticklabels([c.replace("_", "\n") for c in class_names], fontsize=9)
ax.set_ylabel("Fraction in Reciprocal Network")
ax.set_title("Classification Representation")
ax.set_ylim(0, 1)
for bar, val in zip(bars, frac_in_recip):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f"{val:.1%}", ha="center", fontsize=9)
ax.grid(True, alpha=0.3, axis="y")

# --- F: Component Size Distribution ---
ax = axes[1, 2]
if len(comp_sizes) > 1:
    # Skip giant component, show distribution of smaller ones
    small_comps = [s for s in comp_sizes[1:] if s > 1]
    if small_comps:
        comp_counts = Counter(small_comps)
        sizes = sorted(comp_counts.keys())
        freq = [comp_counts[s] for s in sizes]
        ax.bar(sizes, freq, color="steelblue", alpha=0.8)
        ax.set_xlabel("Component Size")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Small Component Sizes\n(giant={comp_sizes[0]:,} nodes)")
    else:
        ax.text(0.5, 0.5, f"Single component\n{comp_sizes[0]:,} nodes",
                transform=ax.transAxes, ha="center", va="center", fontsize=14)
        ax.set_title("Component Analysis")
else:
    ax.text(0.5, 0.5, f"Single component\n{comp_sizes[0]:,} nodes",
            transform=ax.transAxes, ha="center", va="center", fontsize=14)
    ax.set_title("Component Analysis")
ax.grid(True, alpha=0.3)

plt.suptitle(f"FlyWire Real Reciprocal Connectivity (v630)\n"
             f"{n_nodes:,} neurons, {G.ecount():,} directed edges, "
             f"{len(pairs_df):,} reciprocal pairs",
             fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "real_network_analysis.png"),
            dpi=150, bbox_inches="tight")
print(f"  Saved: real_network_analysis.png")

# --- Separate figure: NT co-occurrence heatmap ---
fig2, ax2 = plt.subplots(figsize=(8, 6))
nt_types = sorted(set(pairs_df["n1_nt"]) | set(pairs_df["n2_nt"]))
nt_matrix = np.zeros((len(nt_types), len(nt_types)))
for _, row in pairs_df.iterrows():
    i = nt_types.index(row["n1_nt"])
    j = nt_types.index(row["n2_nt"])
    nt_matrix[i, j] += 1

# Make symmetric for display (since pair order is arbitrary)
nt_sym = nt_matrix + nt_matrix.T
np.fill_diagonal(nt_sym, np.diag(nt_matrix))

im = ax2.imshow(nt_sym, cmap="YlOrRd")
ax2.set_xticks(range(len(nt_types)))
ax2.set_yticks(range(len(nt_types)))
ax2.set_xticklabels(nt_types, rotation=45, ha="right")
ax2.set_yticklabels(nt_types)
ax2.set_title("Neurotransmitter Co-occurrence in Reciprocal Pairs")
plt.colorbar(im, label="Count")

# Add text annotations
for i in range(len(nt_types)):
    for j in range(len(nt_types)):
        val = int(nt_sym[i, j])
        if val > 0:
            color = "white" if val > nt_sym.max() * 0.6 else "black"
            ax2.text(j, i, f"{val:,}", ha="center", va="center",
                    fontsize=8, color=color)

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "nt_cooccurrence_heatmap.png"),
            dpi=150, bbox_inches="tight")
print(f"  Saved: nt_cooccurrence_heatmap.png")

# ============================================================
# 11. Save Summary Statistics
# ============================================================
print("\n11. Saving results...")

summary = {
    "n_neurons": n_nodes,
    "n_reciprocal_pairs": len(pairs_df),
    "n_directed_edges": G.ecount(),
    "density": G.density(),
    "reciprocity": G.reciprocity(),
    "mean_in_degree": in_deg.mean(),
    "mean_out_degree": out_deg.mean(),
    "max_total_degree": int(total_deg.max()),
    "n_components": len(components),
    "giant_component_size": comp_sizes[0],
    "global_transitivity": transitivity,
    "mean_local_clustering": np.mean(local_cc),
}

summary_df = pd.DataFrame([summary])
summary_df.to_csv(os.path.join(RESULTS_DIR, "real_network_summary.csv"), index=False)
print(f"  Saved: real_network_summary.csv")

# Save hub neurons
hub_data = []
for idx in top_idx:
    nid = neuron_list[idx]
    labels = [lbl for lbl in classifications if nid in classifications[lbl]]
    hub_data.append({
        "neuron_id": nid,
        "in_degree": int(in_deg[idx]),
        "out_degree": int(out_deg[idx]),
        "total_degree": int(total_deg[idx]),
        "classifications": "|".join(labels) if labels else "none",
    })

hub_df = pd.DataFrame(hub_data)
hub_df.to_csv(os.path.join(RESULTS_DIR, "hub_neurons.csv"), index=False)
print(f"  Saved: hub_neurons.csv")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Real Network Analysis Complete!")
print("=" * 60)
print(f"\nKey findings:")
print(f"  - {n_nodes:,} neurons participate in reciprocal connections")
print(f"  - {len(pairs_df):,} reciprocal pairs -> {G.ecount():,} directed edges")
print(f"  - Giant component: {comp_sizes[0]:,} nodes ({100*comp_sizes[0]/n_nodes:.1f}%)")
print(f"  - Global transitivity: {transitivity:.4f}")
print(f"  - Most common NT in reciprocal pairs: "
      f"{nt_counts.most_common(1)[0][0]} ({nt_counts.most_common(1)[0][1]:,})")
print(f"\nResults saved to: {RESULTS_DIR}")
