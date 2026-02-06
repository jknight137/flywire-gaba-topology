"""
Neurotransmitter-Specific Subnetwork Analysis
Week 2 - BETA Track (Stretch Goal)

Breaks the FlyWire reciprocal connectivity network into subnetworks by
neurotransmitter (NT) type and analyzes each separately. This goes beyond
the FlyWire paper's overall network statistics to reveal NT-specific
circuit architecture.

Key questions:
1. Do ACh-GABA pairs form different local structures than ACh-ACh pairs?
2. Which NT types form tightly clustered communities vs sparse connections?
3. Are certain NT combinations preferentially found in hubs vs periphery?
4. Is there a "backbone" NT type that connects communities?

Run with: conda activate research-accelerator && python nt_subnetwork_analysis.py
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
print("NT-Specific Subnetwork Analysis - BETA Track Week 2")
print("=" * 60)

# ============================================================
# 1. Load Data
# ============================================================
print("\n1. Loading data...")
pairs_df = pd.read_csv(os.path.join(DATA_DIR, "v630-all-reciprocal-pairs-s1.csv"))
print(f"  {len(pairs_df):,} reciprocal pairs")

# Load classifications
classifications = {}
class_files = {
    "rich_club": "rich_club_neurons.csv",
    "broadcast": "broadcast_neurons.csv",
    "integrate": "integrate_neurons.csv",
}
for label, filename in class_files.items():
    filepath = os.path.join(CSV_DIR, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, header=None, names=["root_id"])
        classifications[label] = set(df["root_id"].values)

# ============================================================
# 2. Build NT-Specific Subnetworks
# ============================================================
print("\n2. Building NT-specific subnetworks...")

# Assign each neuron its NT type (from the pairs data)
neuron_nt = {}
for _, row in pairs_df.iterrows():
    neuron_nt[row["n1"]] = row["n1_nt"]
    neuron_nt[row["n2"]] = row["n2_nt"]

# Count neurons per NT
nt_neuron_counts = Counter(neuron_nt.values())
print(f"  Neurons per NT type:")
for nt, count in sorted(nt_neuron_counts.items(), key=lambda x: -x[1]):
    print(f"    {nt:>5s}: {count:>6,}")

# Build subnetworks for the top NT pair types
nt_pair_types = Counter()
for _, row in pairs_df.iterrows():
    pair = tuple(sorted([row["n1_nt"], row["n2_nt"]]))
    nt_pair_types[pair] += 1

top_pairs = nt_pair_types.most_common(6)  # Top 6 NT pair types
print(f"\n  Top NT pair types:")
for pair, count in top_pairs:
    print(f"    {pair[0]}-{pair[1]}: {count:,}")

# ============================================================
# 3. Analyze Each NT Subnetwork
# ============================================================
print("\n3. Analyzing NT subnetworks...")

subnetwork_stats = []

for (nt1, nt2), pair_count in top_pairs:
    print(f"\n  --- {nt1}-{nt2} subnetwork ({pair_count:,} pairs) ---")

    # Filter pairs for this NT combination
    mask = pairs_df.apply(
        lambda row: set([row["n1_nt"], row["n2_nt"]]) == set([nt1, nt2]),
        axis=1
    )
    sub_pairs = pairs_df[mask]

    # Build graph
    neurons = sorted(set(sub_pairs["n1"]) | set(sub_pairs["n2"]))
    n2i = {n: i for i, n in enumerate(neurons)}
    edges = []
    for _, row in sub_pairs.iterrows():
        edges.append((n2i[row["n1"]], n2i[row["n2"]]))
        edges.append((n2i[row["n2"]], n2i[row["n1"]]))

    G = ig.Graph(n=len(neurons), edges=edges, directed=True)
    G.simplify()

    # Compute statistics
    n_nodes = G.vcount()
    n_edges = G.ecount()
    components = G.connected_components(mode="weak")
    comp_sizes = sorted([len(c) for c in components], reverse=True)
    giant_frac = comp_sizes[0] / n_nodes if n_nodes > 0 else 0

    # Degree stats
    total_deg = np.array(G.indegree()) + np.array(G.outdegree())

    # Transitivity
    transitivity = G.transitivity_undirected()

    # What fraction are rich club neurons?
    rc_neurons = classifications.get("rich_club", set())
    n_rc = sum(1 for n in neurons if n in rc_neurons)
    rc_frac = n_rc / n_nodes if n_nodes > 0 else 0

    stats = {
        "nt_pair": f"{nt1}-{nt2}",
        "n_pairs": pair_count,
        "n_neurons": n_nodes,
        "n_edges": n_edges,
        "density": G.density(),
        "n_components": len(components),
        "giant_component_frac": giant_frac,
        "mean_degree": total_deg.mean(),
        "max_degree": int(total_deg.max()),
        "transitivity": transitivity,
        "rich_club_frac": rc_frac,
    }
    subnetwork_stats.append(stats)

    print(f"    Neurons: {n_nodes:,}, Edges: {n_edges:,}")
    print(f"    Components: {len(components)}, Giant: {giant_frac:.1%}")
    print(f"    Mean degree: {total_deg.mean():.1f}, Max: {total_deg.max()}")
    print(f"    Transitivity: {transitivity:.4f}")
    print(f"    Rich club fraction: {rc_frac:.1%}")

# ============================================================
# 4. Hub NT Composition Analysis
# ============================================================
print("\n4. Hub NT composition analysis...")

# Build full graph to identify hubs
all_neurons = sorted(set(pairs_df["n1"]) | set(pairs_df["n2"]))
full_n2i = {n: i for i, n in enumerate(all_neurons)}
full_edges = []
for _, row in pairs_df.iterrows():
    full_edges.append((full_n2i[row["n1"]], full_n2i[row["n2"]]))
    full_edges.append((full_n2i[row["n2"]], full_n2i[row["n1"]]))
G_full = ig.Graph(n=len(all_neurons), edges=full_edges, directed=True)
G_full.simplify()

total_deg = np.array(G_full.indegree()) + np.array(G_full.outdegree())

# Top 100 hubs
top100_idx = np.argsort(total_deg)[::-1][:100]

# What NT types do the top hubs connect with?
hub_nt_profile = Counter()
for idx in top100_idx:
    nid = all_neurons[idx]
    nt = neuron_nt.get(nid, "unknown")
    hub_nt_profile[nt] += 1

print(f"  NT composition of top 100 hubs:")
for nt, count in sorted(hub_nt_profile.items(), key=lambda x: -x[1]):
    print(f"    {nt:>5s}: {count}")

# What NT connections do hubs make?
hub_set = set(all_neurons[i] for i in top100_idx)
hub_connection_nt = Counter()
for _, row in pairs_df.iterrows():
    if row["n1"] in hub_set or row["n2"] in hub_set:
        pair = tuple(sorted([row["n1_nt"], row["n2_nt"]]))
        hub_connection_nt[pair] += 1

print(f"\n  NT pair types involving top 100 hubs:")
for pair, count in sorted(hub_connection_nt.items(), key=lambda x: -x[1])[:8]:
    print(f"    {pair[0]}-{pair[1]}: {count:,}")

# ============================================================
# 5. Degree-Degree Correlation by NT Type
# ============================================================
print("\n5. Degree-degree correlation by NT type...")

# For each NT pair type, what's the correlation between
# the degrees of the two neurons in each pair?
nt_degree_corr = {}
for (nt1, nt2), _ in top_pairs:
    mask = pairs_df.apply(
        lambda row: set([row["n1_nt"], row["n2_nt"]]) == set([nt1, nt2]),
        axis=1
    )
    sub_pairs = pairs_df[mask]

    d1 = [total_deg[full_n2i[n]] for n in sub_pairs["n1"]]
    d2 = [total_deg[full_n2i[n]] for n in sub_pairs["n2"]]

    if len(d1) > 2:
        corr = np.corrcoef(d1, d2)[0, 1]
        nt_degree_corr[f"{nt1}-{nt2}"] = corr
        print(f"  {nt1}-{nt2}: r = {corr:.3f} (n={len(d1):,})")

# ============================================================
# 6. Visualizations
# ============================================================
print("\n6. Generating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# --- A: Subnetwork comparison (bar chart) ---
ax = axes[0, 0]
stats_df = pd.DataFrame(subnetwork_stats)
x = np.arange(len(stats_df))
ax.bar(x, stats_df["transitivity"], color=plt.cm.Set2(np.linspace(0, 1, len(stats_df))))
ax.set_xticks(x)
ax.set_xticklabels(stats_df["nt_pair"], rotation=45, ha="right")
ax.set_ylabel("Global Transitivity")
ax.set_title("Clustering by NT Pair Type")
ax.grid(True, alpha=0.3, axis="y")
for i, v in enumerate(stats_df["transitivity"]):
    ax.text(i, v + 0.001, f"{v:.4f}", ha="center", fontsize=9)

# --- B: Giant component fraction ---
ax = axes[0, 1]
ax.bar(x, stats_df["giant_component_frac"],
       color=plt.cm.Set2(np.linspace(0, 1, len(stats_df))))
ax.set_xticks(x)
ax.set_xticklabels(stats_df["nt_pair"], rotation=45, ha="right")
ax.set_ylabel("Giant Component Fraction")
ax.set_title("Network Connectivity by NT Pair Type")
ax.set_ylim(0, 1.05)
ax.grid(True, alpha=0.3, axis="y")
for i, v in enumerate(stats_df["giant_component_frac"]):
    ax.text(i, v + 0.02, f"{v:.1%}", ha="center", fontsize=9)

# --- C: Hub NT composition pie ---
ax = axes[1, 0]
labels = list(hub_nt_profile.keys())
sizes = list(hub_nt_profile.values())
colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct="%1.0f%%",
                                   colors=colors, textprops={"fontsize": 10})
ax.set_title("NT Types of Top 100 Hub Neurons")

# --- D: Degree-degree correlation ---
ax = axes[1, 1]
nt_labels = list(nt_degree_corr.keys())
corr_vals = list(nt_degree_corr.values())
colors_corr = ["steelblue" if v > 0 else "coral" for v in corr_vals]
ax.barh(range(len(nt_labels)), corr_vals, color=colors_corr, alpha=0.8)
ax.set_yticks(range(len(nt_labels)))
ax.set_yticklabels(nt_labels)
ax.set_xlabel("Degree-Degree Correlation (r)")
ax.set_title("Assortative Mixing by NT Pair Type")
ax.axvline(x=0, color="black", linewidth=0.5)
ax.grid(True, alpha=0.3, axis="x")

plt.suptitle("Neurotransmitter-Specific Subnetwork Architecture\n"
             "FlyWire v630 Reciprocal Connectivity",
             fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "nt_subnetwork_analysis.png"),
            dpi=150, bbox_inches="tight")
print(f"  Saved: nt_subnetwork_analysis.png")

# ============================================================
# 7. Rich Club Fraction by NT Type
# ============================================================
print("\n7. Rich club fraction by NT type...")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(x, stats_df["rich_club_frac"],
        color=plt.cm.Set2(np.linspace(0, 1, len(stats_df))))
ax2.set_xticks(x)
ax2.set_xticklabels(stats_df["nt_pair"], rotation=45, ha="right")
ax2.set_ylabel("Fraction of Neurons in Rich Club")
ax2.set_title("Rich Club Representation by NT Pair Type")
ax2.grid(True, alpha=0.3, axis="y")
for i, v in enumerate(stats_df["rich_club_frac"]):
    ax2.text(i, v + 0.01, f"{v:.1%}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "nt_rich_club_fraction.png"),
            dpi=150, bbox_inches="tight")
print(f"  Saved: nt_rich_club_fraction.png")

# ============================================================
# 8. Save Results
# ============================================================
print("\n8. Saving results...")
stats_df.to_csv(os.path.join(RESULTS_DIR, "nt_subnetwork_stats.csv"), index=False)
print(f"  Saved: nt_subnetwork_stats.csv")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("NT Subnetwork Analysis Complete!")
print("=" * 60)

print(f"\nKey findings:")
# Find most/least clustered
most_clustered = stats_df.loc[stats_df["transitivity"].idxmax()]
least_clustered = stats_df.loc[stats_df["transitivity"].idxmin()]
print(f"  Most clustered NT pair: {most_clustered['nt_pair']} "
      f"(transitivity={most_clustered['transitivity']:.4f})")
print(f"  Least clustered NT pair: {least_clustered['nt_pair']} "
      f"(transitivity={least_clustered['transitivity']:.4f})")

# Most connected
most_connected = stats_df.loc[stats_df["giant_component_frac"].idxmax()]
print(f"  Most connected: {most_connected['nt_pair']} "
      f"(giant={most_connected['giant_component_frac']:.1%})")

print(f"\nResults saved to: {RESULTS_DIR}")
