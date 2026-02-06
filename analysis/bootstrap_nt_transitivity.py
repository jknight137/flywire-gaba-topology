"""
Bootstrap Confidence Intervals for NT Subnetwork Clustering
Week 2 - BETA Track - Statistical Robustness

This script provides bootstrap confidence intervals for the key finding that
GABA-GABA reciprocal pairs have ~800x higher clustering (transitivity) than
ACh-GABA pairs.

Goal: Confirm that the GABA-GABA vs ACh-GABA transitivity difference is 
statistically robust and not an artifact of sampling.

Method:
1. Bootstrap resample the reciprocal pairs (with replacement)
2. For each bootstrap sample, build NT-specific subnetworks
3. Compute transitivity for each subnetwork
4. Report 95% confidence intervals

Run with: conda activate research-accelerator && python bootstrap_nt_transitivity.py
"""
import os
import time
from collections import Counter

import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# ============================================================
# Configuration
# ============================================================
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_SCRIPT_DIR, "..", "data")
RESULTS_DIR = os.path.join(_SCRIPT_DIR, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

N_BOOTSTRAP = 1000  # Number of bootstrap iterations
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

print("=" * 60)
print("Bootstrap CI for NT Subnetwork Transitivity - BETA Track")
print("=" * 60)

# ============================================================
# 1. Load Data
# ============================================================
print("\n1. Loading data...")
t0 = time.time()
pairs_df = pd.read_csv(os.path.join(DATA_DIR, "v630-all-reciprocal-pairs-s1.csv"))
print(f"  {len(pairs_df):,} reciprocal pairs loaded in {time.time()-t0:.1f}s")

# Get top NT pair types
nt_pair_types = Counter()
for _, row in pairs_df.iterrows():
    pair = tuple(sorted([row["n1_nt"], row["n2_nt"]]))
    nt_pair_types[pair] += 1

top_pairs = nt_pair_types.most_common(6)
print(f"\n  Top NT pair types:")
for pair, count in top_pairs:
    print(f"    {pair[0]}-{pair[1]}: {count:,}")

# ============================================================
# 2. Helper Function: Compute Transitivity for a Subset of Pairs
# ============================================================
def compute_transitivity_for_nt_pair(pairs_subset, nt1, nt2):
    """
    Given a DataFrame of pairs and an NT combination, build the subnetwork
    and compute its transitivity.
    
    Returns: transitivity (float), or NaN if too few edges
    """
    # Filter for this NT pair
    mask = pairs_subset.apply(
        lambda row: set([row["n1_nt"], row["n2_nt"]]) == set([nt1, nt2]),
        axis=1
    )
    sub_pairs = pairs_subset[mask]
    
    if len(sub_pairs) < 3:  # Need at least 3 edges for a triangle
        return np.nan
    
    # Build graph
    neurons = sorted(set(sub_pairs["n1"]) | set(sub_pairs["n2"]))
    if len(neurons) < 3:
        return np.nan
        
    n2i = {n: i for i, n in enumerate(neurons)}
    edges = []
    for _, row in sub_pairs.iterrows():
        edges.append((n2i[row["n1"]], n2i[row["n2"]]))
        edges.append((n2i[row["n2"]], n2i[row["n1"]]))
    
    G = ig.Graph(n=len(neurons), edges=edges, directed=True)
    G.simplify()
    
    # Compute transitivity (undirected version = fraction of closed triangles)
    return G.transitivity_undirected()


# ============================================================
# 3. Compute Original (Full Dataset) Transitivity
# ============================================================
print("\n2. Computing original transitivity values...")

original_transitivity = {}
for (nt1, nt2), count in top_pairs:
    pair_label = f"{nt1}-{nt2}"
    trans = compute_transitivity_for_nt_pair(pairs_df, nt1, nt2)
    original_transitivity[pair_label] = trans
    print(f"  {pair_label}: {trans:.6f}")

# ============================================================
# 4. Bootstrap Resampling
# ============================================================
print(f"\n3. Running {N_BOOTSTRAP} bootstrap iterations...")
t0 = time.time()

# Store bootstrap results
bootstrap_results = {f"{nt1}-{nt2}": [] for (nt1, nt2), _ in top_pairs}

for i in range(N_BOOTSTRAP):
    if (i + 1) % 100 == 0:
        elapsed = time.time() - t0
        eta = elapsed / (i + 1) * (N_BOOTSTRAP - i - 1)
        print(f"  Iteration {i+1}/{N_BOOTSTRAP} ({elapsed:.0f}s elapsed, ~{eta:.0f}s remaining)")
    
    # Bootstrap resample pairs with replacement
    sample_idx = np.random.choice(len(pairs_df), size=len(pairs_df), replace=True)
    sample_df = pairs_df.iloc[sample_idx].reset_index(drop=True)
    
    # Compute transitivity for each NT pair type
    for (nt1, nt2), _ in top_pairs:
        pair_label = f"{nt1}-{nt2}"
        trans = compute_transitivity_for_nt_pair(sample_df, nt1, nt2)
        bootstrap_results[pair_label].append(trans)

elapsed = time.time() - t0
print(f"  Completed in {elapsed:.1f}s ({elapsed/N_BOOTSTRAP:.2f}s per iteration)")

# ============================================================
# 5. Compute Confidence Intervals
# ============================================================
print("\n4. Computing 95% confidence intervals...")

ci_results = []
for pair_label in bootstrap_results:
    values = np.array(bootstrap_results[pair_label])
    values = values[~np.isnan(values)]  # Remove NaNs
    
    if len(values) < 10:
        print(f"  {pair_label}: Insufficient data ({len(values)} valid samples)")
        continue
    
    original = original_transitivity[pair_label]
    mean = np.mean(values)
    std = np.std(values)
    ci_low = np.percentile(values, 2.5)
    ci_high = np.percentile(values, 97.5)
    
    ci_results.append({
        "nt_pair": pair_label,
        "original": original,
        "bootstrap_mean": mean,
        "bootstrap_std": std,
        "ci_95_low": ci_low,
        "ci_95_high": ci_high,
        "n_valid_samples": len(values),
    })
    
    print(f"  {pair_label:>12s}: {original:.6f} (95% CI: [{ci_low:.6f}, {ci_high:.6f}])")

# ============================================================
# 6. Test: Is GABA-GABA > ACh-GABA Significant?
# ============================================================
print("\n5. Statistical test: GABA-GABA vs ACh-GABA transitivity...")

gaba_gaba = np.array(bootstrap_results.get("gaba-gaba", []))
ach_gaba = np.array(bootstrap_results.get("ach-gaba", []))

# Remove NaNs
gaba_gaba = gaba_gaba[~np.isnan(gaba_gaba)]
ach_gaba = ach_gaba[~np.isnan(ach_gaba)]

if len(gaba_gaba) > 0 and len(ach_gaba) > 0:
    # Compute difference for each bootstrap sample
    # (Use pairwise differences if same length, otherwise use means)
    min_len = min(len(gaba_gaba), len(ach_gaba))
    diff = gaba_gaba[:min_len] - ach_gaba[:min_len]
    
    mean_diff = np.mean(diff)
    ci_diff_low = np.percentile(diff, 2.5)
    ci_diff_high = np.percentile(diff, 97.5)
    
    # What fraction of bootstrap samples show GABA-GABA > ACh-GABA?
    frac_higher = np.mean(diff > 0)
    
    print(f"  GABA-GABA transitivity: {np.mean(gaba_gaba):.6f} ± {np.std(gaba_gaba):.6f}")
    print(f"  ACh-GABA transitivity:  {np.mean(ach_gaba):.6f} ± {np.std(ach_gaba):.6f}")
    print(f"  Difference (GABA-GABA - ACh-GABA): {mean_diff:.6f}")
    print(f"  95% CI of difference: [{ci_diff_low:.6f}, {ci_diff_high:.6f}]")
    print(f"  Bootstrap samples where GABA-GABA > ACh-GABA: {frac_higher:.1%}")
    
    # Ratio (fold difference)
    ratio = gaba_gaba[:min_len] / (ach_gaba[:min_len] + 1e-10)  # Avoid div by zero
    ratio = ratio[np.isfinite(ratio)]
    if len(ratio) > 0:
        print(f"  Mean fold difference: {np.mean(ratio):.1f}x")
        print(f"  Median fold difference: {np.median(ratio):.1f}x")
        print(f"  95% CI of fold difference: [{np.percentile(ratio, 2.5):.1f}x, {np.percentile(ratio, 97.5):.1f}x]")

# ============================================================
# 7. Visualization
# ============================================================
print("\n6. Generating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# --- A: Bootstrap distributions ---
ax = axes[0, 0]
pair_labels = list(bootstrap_results.keys())
positions = range(len(pair_labels))
data_to_plot = []
colors = []
cmap = plt.cm.Set2

for i, label in enumerate(pair_labels):
    values = np.array(bootstrap_results[label])
    values = values[~np.isnan(values)]
    data_to_plot.append(values)
    colors.append(cmap(i / len(pair_labels)))

bp = ax.boxplot(data_to_plot, positions=positions, showfliers=False, patch_artist=True)
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Add original values as diamonds
for i, label in enumerate(pair_labels):
    orig = original_transitivity.get(label, np.nan)
    if not np.isnan(orig):
        ax.scatter([i], [orig], marker="D", s=100, c="red", zorder=10,
                  edgecolor="black", linewidth=1)

ax.set_xticks(positions)
ax.set_xticklabels([l.replace("-", "\n") for l in pair_labels], fontsize=10)
ax.set_ylabel("Transitivity (clustering coefficient)")
ax.set_title("Bootstrap Distribution of Transitivity by NT Pair\n(red diamonds = original values)")
ax.set_yscale("log")
ax.grid(True, alpha=0.3, axis="y")

# --- B: GABA-GABA vs ACh-GABA comparison ---
ax = axes[0, 1]
if len(gaba_gaba) > 0 and len(ach_gaba) > 0:
    ax.hist(gaba_gaba, bins=50, alpha=0.7, label=f"GABA-GABA (n={len(gaba_gaba)})", color="C0")
    ax.hist(ach_gaba, bins=50, alpha=0.7, label=f"ACh-GABA (n={len(ach_gaba)})", color="C1")
    ax.axvline(original_transitivity.get("gaba-gaba", 0), color="C0", linestyle="--", linewidth=2)
    ax.axvline(original_transitivity.get("ach-gaba", 0), color="C1", linestyle="--", linewidth=2)
    ax.set_xlabel("Transitivity")
    ax.set_ylabel("Count")
    ax.set_title(f"GABA-GABA vs ACh-GABA Bootstrap Distributions\n(dashed = original values)")
    ax.legend()
    ax.grid(True, alpha=0.3)

# --- C: Difference distribution ---
ax = axes[1, 0]
if len(diff) > 0:
    ax.hist(diff, bins=50, alpha=0.7, color="purple")
    ax.axvline(0, color="black", linestyle="--", linewidth=2)
    ax.axvline(ci_diff_low, color="red", linestyle=":", linewidth=2, label=f"95% CI: [{ci_diff_low:.4f}, {ci_diff_high:.4f}]")
    ax.axvline(ci_diff_high, color="red", linestyle=":", linewidth=2)
    ax.set_xlabel("Transitivity Difference (GABA-GABA - ACh-GABA)")
    ax.set_ylabel("Count")
    ax.set_title(f"Bootstrap Distribution of Transitivity Difference\n{frac_higher:.1%} of samples show GABA-GABA > ACh-GABA")
    ax.legend()
    ax.grid(True, alpha=0.3)

# --- D: Fold difference (ratio) distribution ---
ax = axes[1, 1]
if len(ratio) > 0:
    ax.hist(ratio, bins=50, alpha=0.7, color="green")
    ax.axvline(np.median(ratio), color="red", linestyle="--", linewidth=2, 
               label=f"Median: {np.median(ratio):.0f}x")
    ax.axvline(np.percentile(ratio, 2.5), color="orange", linestyle=":", linewidth=2)
    ax.axvline(np.percentile(ratio, 97.5), color="orange", linestyle=":", linewidth=2,
               label=f"95% CI: [{np.percentile(ratio, 2.5):.0f}x, {np.percentile(ratio, 97.5):.0f}x]")
    ax.set_xlabel("Fold Difference (GABA-GABA / ACh-GABA)")
    ax.set_ylabel("Count")
    ax.set_title(f"Bootstrap Distribution of Fold Difference")
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.suptitle(f"Bootstrap Analysis: NT-Specific Transitivity ({N_BOOTSTRAP} iterations)\n"
             f"Seed={RANDOM_SEED}", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "bootstrap_nt_transitivity.png"),
            dpi=150, bbox_inches="tight")
print(f"  Saved: bootstrap_nt_transitivity.png")

# ============================================================
# 8. Save Results
# ============================================================
print("\n7. Saving results...")

ci_df = pd.DataFrame(ci_results)
ci_df.to_csv(os.path.join(RESULTS_DIR, "bootstrap_nt_transitivity_ci.csv"), index=False)
print(f"  Saved: bootstrap_nt_transitivity_ci.csv")

# Save full bootstrap samples for reproducibility
bootstrap_df = pd.DataFrame(bootstrap_results)
bootstrap_df.to_csv(os.path.join(RESULTS_DIR, "bootstrap_nt_transitivity_samples.csv"), index=False)
print(f"  Saved: bootstrap_nt_transitivity_samples.csv")

# Summary statistics
summary = {
    "n_bootstrap": N_BOOTSTRAP,
    "random_seed": RANDOM_SEED,
    "gaba_gaba_mean": np.mean(gaba_gaba) if len(gaba_gaba) > 0 else np.nan,
    "gaba_gaba_ci_low": np.percentile(gaba_gaba, 2.5) if len(gaba_gaba) > 0 else np.nan,
    "gaba_gaba_ci_high": np.percentile(gaba_gaba, 97.5) if len(gaba_gaba) > 0 else np.nan,
    "ach_gaba_mean": np.mean(ach_gaba) if len(ach_gaba) > 0 else np.nan,
    "ach_gaba_ci_low": np.percentile(ach_gaba, 2.5) if len(ach_gaba) > 0 else np.nan,
    "ach_gaba_ci_high": np.percentile(ach_gaba, 97.5) if len(ach_gaba) > 0 else np.nan,
    "diff_mean": mean_diff if 'mean_diff' in dir() else np.nan,
    "diff_ci_low": ci_diff_low if 'ci_diff_low' in dir() else np.nan,
    "diff_ci_high": ci_diff_high if 'ci_diff_high' in dir() else np.nan,
    "fold_diff_median": np.median(ratio) if len(ratio) > 0 else np.nan,
    "fold_diff_ci_low": np.percentile(ratio, 2.5) if len(ratio) > 0 else np.nan,
    "fold_diff_ci_high": np.percentile(ratio, 97.5) if len(ratio) > 0 else np.nan,
    "frac_gaba_higher": frac_higher if 'frac_higher' in dir() else np.nan,
}
summary_df = pd.DataFrame([summary])
summary_df.to_csv(os.path.join(RESULTS_DIR, "bootstrap_nt_transitivity_summary.csv"), index=False)
print(f"  Saved: bootstrap_nt_transitivity_summary.csv")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Bootstrap Analysis Complete!")
print("=" * 60)
print(f"\nKey result: GABA-GABA has {np.median(ratio):.0f}x higher transitivity than ACh-GABA")
print(f"95% CI of fold difference: [{np.percentile(ratio, 2.5):.0f}x, {np.percentile(ratio, 97.5):.0f}x]")
print(f"This difference is observed in {frac_higher:.1%} of bootstrap samples.")
print(f"\nIf CI excludes 1x and frac > 95%, the finding is statistically robust.")
print(f"\nResults saved to: {RESULTS_DIR}")
