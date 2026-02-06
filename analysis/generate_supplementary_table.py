"""
Generate Supplementary Table S1: Complete 21 NT-pair transitivity analysis.
For Paper B: Neurotransmitter-Specific Clustering in the Drosophila Brain Connectome.
"""

import os
import pandas as pd
import numpy as np
import igraph as ig
from collections import Counter
from itertools import combinations_with_replacement

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_SCRIPT_DIR, "..", "data")
RESULTS_DIR = os.path.join(_SCRIPT_DIR, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 70)
print("  Supplementary Table S1: All 21 NT-Pair Subnetwork Statistics")
print("=" * 70)

# Load data
print("\nLoading reciprocal pairs...")
pairs_df = pd.read_csv(os.path.join(DATA_DIR, "v630-all-reciprocal-pairs-s1.csv"))
print(f"  {len(pairs_df):,} reciprocal pairs loaded")

# Assign NT pair type to each row
pairs_df["nt_pair"] = pairs_df.apply(
    lambda row: tuple(sorted([row["n1_nt"], row["n2_nt"]])), axis=1
)

# Get all 21 unique pair types
nt_types = sorted(pairs_df["n1_nt"].unique())
all_pair_types = []
for i, nt1 in enumerate(nt_types):
    for nt2 in nt_types[i:]:
        all_pair_types.append((nt1, nt2))

print(f"  {len(all_pair_types)} unique NT pair types")

# Analyze each
results = []

for nt1, nt2 in all_pair_types:
    pair_key = (nt1, nt2)
    mask = pairs_df["nt_pair"] == pair_key
    sub_pairs = pairs_df[mask]
    pair_count = len(sub_pairs)

    if pair_count == 0:
        continue

    pair_label = f"{nt1.upper()}-{nt2.upper()}"
    same_type = "Same" if nt1 == nt2 else "Cross"
    print(f"\n  {pair_label}: {pair_count:,} pairs...", end=" ", flush=True)

    # Build graph
    neurons = sorted(set(sub_pairs["n1"]) | set(sub_pairs["n2"]))
    n2i = {n: i for i, n in enumerate(neurons)}
    edges = []
    for _, row in sub_pairs.iterrows():
        edges.append((n2i[row["n1"]], n2i[row["n2"]]))
        edges.append((n2i[row["n2"]], n2i[row["n1"]]))

    G = ig.Graph(n=len(neurons), edges=edges, directed=True)
    G.simplify()

    # Statistics
    n_nodes = G.vcount()
    n_edges = G.ecount()
    components = G.connected_components(mode="weak")
    comp_sizes = sorted([len(c) for c in components], reverse=True)
    giant_frac = comp_sizes[0] / n_nodes if n_nodes > 0 else 0

    # Degree
    total_deg = np.array(G.indegree()) + np.array(G.outdegree())
    mean_deg = np.mean(total_deg)
    max_deg = np.max(total_deg)

    # Transitivity
    transitivity = G.transitivity_undirected()
    if transitivity != transitivity:  # NaN check
        transitivity = 0.0

    print(f"trans={transitivity:.6f}", flush=True)

    results.append({
        "NT Pair": pair_label,
        "Type": same_type,
        "N Pairs": pair_count,
        "N Neurons": n_nodes,
        "N Edges": n_edges,
        "Density": G.density(),
        "Transitivity": transitivity,
        "N Components": len(components),
        "Giant Component %": giant_frac * 100,
        "Mean Degree": mean_deg,
        "Max Degree": max_deg,
    })

# Sort: same-type first (by transitivity desc), then cross-type (by transitivity desc)
results_df = pd.DataFrame(results)
same_mask = results_df["Type"] == "Same"
same_df = results_df[same_mask].sort_values("Transitivity", ascending=False)
cross_df = results_df[~same_mask].sort_values("Transitivity", ascending=False)
results_df = pd.concat([same_df, cross_df], ignore_index=True)

# Save CSV
csv_path = os.path.join(RESULTS_DIR, "supplementary_table_s1_all_21_pairs.csv")
results_df.to_csv(csv_path, index=False)
print(f"\n\nSaved to: {csv_path}")

# Print as markdown table for the paper
print("\n" + "=" * 70)
print("  SUPPLEMENTARY TABLE S1 (Markdown format)")
print("=" * 70)
print()
print("| NT Pair | Type | N Pairs | N Neurons | Transitivity | Giant Comp. % | Mean Degree |")
print("|---------|------|---------|-----------|-------------|--------------|-------------|")
for _, row in results_df.iterrows():
    print(f"| {row['NT Pair']} | {row['Type']} | {row['N Pairs']:,} | "
          f"{row['N Neurons']:,} | {row['Transitivity']:.6f} | "
          f"{row['Giant Component %']:.1f}% | {row['Mean Degree']:.1f} |")

print(f"\n  Total pairs analyzed: {results_df['N Pairs'].sum():,}")
print(f"  Same-type pairs: {same_df['N Pairs'].sum():,}")
print(f"  Cross-type pairs: {cross_df['N Pairs'].sum():,}")
