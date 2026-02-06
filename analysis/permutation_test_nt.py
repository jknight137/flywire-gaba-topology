"""
Permutation Test for NT-Specific Transitivity
Paper B: Neurotransmitter-Specific Clustering in FlyWire Connectome

Tests whether the GABA-GABA vs ACh-GABA transitivity difference (737x) is
attributable to NT identity by shuffling NT labels at the NEURON level while
preserving graph structure and NT frequency distribution.

Null hypothesis: NT identity does not affect transitivity structure.
Alternative: GABA-GABA transitivity is higher than expected under random NT assignment.

Optimized implementation:
- Pre-extracts unique neurons and their NTs into arrays
- Uses numpy vectorized operations for NT pair filtering
- Builds graphs with igraph for fast transitivity computation
- Target: <2 seconds per permutation

Run with: conda activate research-accelerator && python permutation_test_nt.py
"""

import os
import time
import numpy as np
import pandas as pd
import igraph as ig

# ============================================================
# Configuration
# ============================================================
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_SCRIPT_DIR, "..", "data")
RESULTS_DIR = os.path.join(_SCRIPT_DIR, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

N_PERM = 1000
RANDOM_SEED = 42

print("=" * 60)
print("Permutation Test for NT-Specific Transitivity")
print("=" * 60)

# ============================================================
# 1. Load Data
# ============================================================
print("\n1. Loading data...")
t0 = time.time()
pairs_df = pd.read_csv(os.path.join(DATA_DIR, "v630-all-reciprocal-pairs-s1.csv"))
print(f"   {len(pairs_df):,} reciprocal pairs loaded in {time.time()-t0:.1f}s")

# ============================================================
# 2. Pre-extract data into numpy arrays for speed
# ============================================================
print("\n2. Pre-extracting neuron data...")

# Get all unique neurons and assign integer indices
n1_arr = pairs_df["n1"].values
n2_arr = pairs_df["n2"].values
n1_nt_arr = pairs_df["n1_nt"].values
n2_nt_arr = pairs_df["n2_nt"].values

all_neurons = np.unique(np.concatenate([n1_arr, n2_arr]))
neuron_to_idx = {n: i for i, n in enumerate(all_neurons)}
n_neurons = len(all_neurons)
print(f"   {n_neurons:,} unique neurons")

# Build neuron -> NT mapping from the data
# Each neuron appears potentially multiple times; take the most common NT
neuron_nt_map = {}
for n, nt in zip(n1_arr, n1_nt_arr):
    neuron_nt_map[n] = nt
for n, nt in zip(n2_arr, n2_nt_arr):
    neuron_nt_map[n] = nt

# Create arrays: neuron indices for each pair, and per-neuron NT labels
n1_idx = np.array([neuron_to_idx[n] for n in n1_arr], dtype=np.int32)
n2_idx = np.array([neuron_to_idx[n] for n in n2_arr], dtype=np.int32)

# Per-neuron NT label array (indexed by neuron_idx)
neuron_nts = np.array([neuron_nt_map[n] for n in all_neurons])

# Count NT distribution
unique_nts, nt_counts = np.unique(neuron_nts, return_counts=True)
print(f"   NT distribution:")
for nt, count in sorted(zip(unique_nts, nt_counts), key=lambda x: -x[1]):
    print(f"     {nt}: {count:,} ({count/n_neurons*100:.1f}%)")

# Encode NTs as integers for fast comparison
nt_to_int = {nt: i for i, nt in enumerate(unique_nts)}
neuron_nt_ints = np.array([nt_to_int[nt] for nt in neuron_nts], dtype=np.int8)

GABA_INT = nt_to_int.get("gaba", -1)
ACH_INT = nt_to_int.get("ach", -1)
print(f"   GABA int code: {GABA_INT}, ACh int code: {ACH_INT}")

# ============================================================
# 3. Optimized transitivity computation
# ============================================================
def compute_transitivity_fast(n1_idx, n2_idx, nt_labels, nt1_int, nt2_int):
    """
    Compute transitivity for the subnetwork of pairs where
    one neuron has nt1_int and the other has nt2_int.

    Uses vectorized numpy operations for filtering and igraph for graph computation.

    Parameters:
        n1_idx: array of neuron-1 indices for each pair
        n2_idx: array of neuron-2 indices for each pair
        nt_labels: array mapping neuron_idx -> nt_int
        nt1_int: integer code for first NT type
        nt2_int: integer code for second NT type

    Returns:
        transitivity (float) or NaN if insufficient data
    """
    # Get NT labels for each pair's neurons
    n1_nts = nt_labels[n1_idx]
    n2_nts = nt_labels[n2_idx]

    # Vectorized mask: find pairs matching the NT combination
    if nt1_int == nt2_int:
        # Same-NT pair: both neurons must have this NT
        mask = (n1_nts == nt1_int) & (n2_nts == nt1_int)
    else:
        # Cross-NT pair: one has nt1 and other has nt2, or vice versa
        mask = ((n1_nts == nt1_int) & (n2_nts == nt2_int)) | \
               ((n1_nts == nt2_int) & (n2_nts == nt1_int))

    sub_n1 = n1_idx[mask]
    sub_n2 = n2_idx[mask]

    if len(sub_n1) < 3:
        return np.nan

    # Get unique neurons in this subnetwork and remap to contiguous indices
    unique_nodes = np.unique(np.concatenate([sub_n1, sub_n2]))
    if len(unique_nodes) < 3:
        return np.nan

    node_remap = np.full(n_neurons, -1, dtype=np.int32)
    node_remap[unique_nodes] = np.arange(len(unique_nodes), dtype=np.int32)

    remapped_n1 = node_remap[sub_n1]
    remapped_n2 = node_remap[sub_n2]

    # Build edge list (both directions for undirected)
    edges = list(zip(remapped_n1.tolist(), remapped_n2.tolist())) + \
            list(zip(remapped_n2.tolist(), remapped_n1.tolist()))

    G = ig.Graph(n=len(unique_nodes), edges=edges, directed=True)
    G.simplify()

    return G.transitivity_undirected()


# ============================================================
# 4. Compute observed (real) transitivity values
# ============================================================
print("\n3. Computing observed transitivity values...")

obs_gaba_gaba = compute_transitivity_fast(n1_idx, n2_idx, neuron_nt_ints, GABA_INT, GABA_INT)
obs_ach_gaba = compute_transitivity_fast(n1_idx, n2_idx, neuron_nt_ints, ACH_INT, GABA_INT)
obs_fold_diff = obs_gaba_gaba / obs_ach_gaba if obs_ach_gaba > 0 else np.inf

print(f"   GABA-GABA transitivity: {obs_gaba_gaba:.6f}")
print(f"   ACh-GABA transitivity:  {obs_ach_gaba:.6f}")
print(f"   Observed fold difference: {obs_fold_diff:.1f}x")

# ============================================================
# 5. Permutation test
# ============================================================
print(f"\n4. Running {N_PERM} permutations...")
print("   (Shuffling NT labels at NEURON level, preserving graph structure & NT frequencies)")

np.random.seed(RANDOM_SEED)

perm_results = []
t_start = time.time()

for i in range(N_PERM):
    if (i + 1) % 50 == 0 or i == 0:
        elapsed = time.time() - t_start
        rate = (i + 1) / elapsed if elapsed > 0 else 0
        eta = (N_PERM - i - 1) / rate if rate > 0 else 0
        print(f"   Iteration {i+1}/{N_PERM} ({elapsed:.0f}s elapsed, ~{eta:.0f}s remaining, {rate:.1f} iter/s)")

    # Shuffle NT labels across neurons (preserving frequency distribution)
    # numpy.random.permutation shuffles the array, keeping the same values
    shuffled_nt_ints = np.random.permutation(neuron_nt_ints)

    # Compute transitivity with shuffled labels
    perm_gaba_gaba = compute_transitivity_fast(n1_idx, n2_idx, shuffled_nt_ints, GABA_INT, GABA_INT)
    perm_ach_gaba = compute_transitivity_fast(n1_idx, n2_idx, shuffled_nt_ints, ACH_INT, GABA_INT)

    if perm_ach_gaba > 0 and not np.isnan(perm_ach_gaba) and not np.isnan(perm_gaba_gaba):
        fold_diff = perm_gaba_gaba / perm_ach_gaba
    else:
        fold_diff = np.nan

    perm_results.append({
        "iteration": i + 1,
        "gaba_gaba_transitivity": perm_gaba_gaba,
        "ach_gaba_transitivity": perm_ach_gaba,
        "fold_difference": fold_diff,
    })

total_time = time.time() - t_start
print(f"\n   Completed {N_PERM} permutations in {total_time:.1f}s ({total_time/N_PERM:.2f}s per permutation)")

# ============================================================
# 6. Analyze results
# ============================================================
print("\n5. Analyzing permutation results...")

results_df = pd.DataFrame(perm_results)
results_df.to_csv(os.path.join(RESULTS_DIR, "permutation_test_results.csv"), index=False)
print(f"   Saved: permutation_test_results.csv")

# Remove NaNs for analysis
valid = results_df.dropna(subset=["fold_difference"])
n_valid = len(valid)
print(f"   Valid permutations: {n_valid}/{N_PERM}")

null_fold_diffs = valid["fold_difference"].values
null_gaba_gaba = valid["gaba_gaba_transitivity"].values
null_ach_gaba = valid["ach_gaba_transitivity"].values

# Compute p-value: fraction of null fold-differences >= observed
p_value = np.mean(null_fold_diffs >= obs_fold_diff)

# Null distribution statistics
null_mean = np.mean(null_fold_diffs)
null_median = np.median(null_fold_diffs)
null_ci_low = np.percentile(null_fold_diffs, 2.5)
null_ci_high = np.percentile(null_fold_diffs, 97.5)
null_max = np.max(null_fold_diffs)

null_gaba_mean = np.mean(null_gaba_gaba)
null_ach_mean = np.mean(null_ach_gaba)

print(f"\n   === PERMUTATION TEST RESULTS ===")
print(f"   Observed fold difference: {obs_fold_diff:.1f}x")
print(f"   Null distribution:")
print(f"     Mean:   {null_mean:.2f}x")
print(f"     Median: {null_median:.2f}x")
print(f"     95% CI: [{null_ci_low:.2f}, {null_ci_high:.2f}]x")
print(f"     Max:    {null_max:.2f}x")
print(f"   Null GABA-GABA transitivity mean: {null_gaba_mean:.6f}")
print(f"   Null ACh-GABA transitivity mean:  {null_ach_mean:.6f}")
print(f"   p-value: {p_value:.4f} ({p_value})")
print(f"   {'SIGNIFICANT' if p_value < 0.001 else 'NOT SIGNIFICANT'}: Observed fold difference is {'far outside' if p_value < 0.001 else 'within'} the null distribution")

# ============================================================
# 7. Save summary
# ============================================================
summary = {
    "observed_gaba_gaba": obs_gaba_gaba,
    "observed_ach_gaba": obs_ach_gaba,
    "observed_fold_diff": obs_fold_diff,
    "null_mean_fold_diff": null_mean,
    "null_median_fold_diff": null_median,
    "null_ci_95_low": null_ci_low,
    "null_ci_95_high": null_ci_high,
    "null_max_fold_diff": null_max,
    "null_gaba_gaba_mean": null_gaba_mean,
    "null_ach_gaba_mean": null_ach_mean,
    "p_value": p_value,
    "n_permutations": N_PERM,
    "n_valid": n_valid,
    "time_seconds": total_time,
    "time_per_perm": total_time / N_PERM,
}

summary_df = pd.DataFrame([summary])
summary_df.to_csv(os.path.join(RESULTS_DIR, "permutation_test_summary.csv"), index=False)
print(f"\n   Saved: permutation_test_summary.csv")

# ============================================================
# 8. Generate visualization
# ============================================================
print("\n6. Generating null distribution figure...")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Null distribution of fold differences
ax = axes[0]
ax.hist(null_fold_diffs, bins=50, color='steelblue', alpha=0.7, edgecolor='black', label='Null distribution')
ax.axvline(obs_fold_diff, color='red', linestyle='--', linewidth=2, label=f'Observed: {obs_fold_diff:.0f}x')
ax.axvline(null_ci_low, color='gray', linestyle=':', linewidth=1.5)
ax.axvline(null_ci_high, color='gray', linestyle=':', linewidth=1.5, label=f'Null 95% CI: [{null_ci_low:.1f}, {null_ci_high:.1f}]x')
ax.set_xlabel('Fold Difference (GABA-GABA / ACh-GABA)')
ax.set_ylabel('Count')
ax.set_title(f'A. Permutation Null Distribution (n={N_PERM})\np < {max(p_value, 1/N_PERM):.3f}')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

# Add arrow pointing to observed value if it's off-scale
if obs_fold_diff > ax.get_xlim()[1] * 0.8:
    ax.annotate(f'Observed: {obs_fold_diff:.0f}x\n(far outside null)',
                xy=(min(obs_fold_diff, ax.get_xlim()[1]*0.95), ax.get_ylim()[1]*0.5),
                fontsize=9, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Panel B: Null GABA-GABA transitivity vs observed
ax = axes[1]
ax.hist(null_gaba_gaba, bins=50, color='steelblue', alpha=0.7, edgecolor='black', label='Null GABA-GABA')
ax.axvline(obs_gaba_gaba, color='red', linestyle='--', linewidth=2, label=f'Observed: {obs_gaba_gaba:.4f}')
ax.axvline(np.percentile(null_gaba_gaba, 2.5), color='gray', linestyle=':', linewidth=1.5)
ax.axvline(np.percentile(null_gaba_gaba, 97.5), color='gray', linestyle=':', linewidth=1.5)
ax.set_xlabel('GABA-GABA Transitivity')
ax.set_ylabel('Count')
ax.set_title('B. GABA-GABA Transitivity: Observed vs Null')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

plt.suptitle(f'Permutation Test: NT Labels Shuffled at Neuron Level\n'
             f'Observed {obs_fold_diff:.0f}x vs null median {null_median:.1f}x (p < {max(p_value, 1/N_PERM):.3f})',
             fontsize=12, fontweight='bold')
plt.tight_layout()

fig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(fig_dir, exist_ok=True)
plt.savefig(os.path.join(fig_dir, "permutation_test_null_distribution.png"), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(fig_dir, "permutation_test_null_distribution.pdf"), dpi=300, bbox_inches='tight')
plt.close()
print(f"   Saved: figures/permutation_test_null_distribution.png/pdf")

print("\n" + "=" * 60)
print("Permutation Test Complete!")
print("=" * 60)
