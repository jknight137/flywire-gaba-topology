---
layout: default
title: Code & Reproducibility
---

# Code & Reproducibility

All analysis code and data are publicly available for full reproducibility.

---

## Repository Structure

```
flywire-gaba-topology/
├── analysis/                          # All analysis scripts
│   ├── bootstrap_nt_transitivity.py   # Bootstrap CIs for NT-pair transitivity
│   ├── nt_subnetwork_analysis.py      # NT-pair subnetwork statistics
│   ├── real_network_analysis.py       # Hub analysis, degree distribution
│   ├── permutation_test_nt.py         # Permutation test (raw)
│   ├── permutation_test_analysis.py   # Permutation test post-hoc analysis
│   ├── generate_paper_figures.py      # Generate Figures 1-4
│   ├── generate_supplementary_table.py# All 21 NT-pair statistics
│   └── hub_sensitivity.py             # GABA hub enrichment analysis
├── data/
│   ├── v630-all-reciprocal-pairs-s1.csv  # FlyWire v630 reciprocal pairs
│   └── classifications/               # Neuron classification CSVs
├── results/                           # Pre-computed results (CSV)
├── figures/                           # Generated figures (PNG + PDF)
├── paper/
│   └── manuscript.md                  # Paper draft
├── docs/                              # GitHub Pages website
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Prerequisites

### Python Environment

**Python version:** ≥ 3.10

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Required packages:

- **networkx** (3.2+) — network analysis
- **python-igraph** — fast graph algorithms
- **numpy** (1.26+) — numerical computation
- **pandas** (2.1+) — data manipulation
- **matplotlib** — visualization
- **seaborn** — statistical plotting
- **scipy** — statistical tests

---

## Running the Analysis

Scripts should be run from the `analysis/` directory. Each script reads data from `../data/` and writes results to `../results/` and figures to `../figures/`.

### Step 1: Core Network Statistics

```bash
cd analysis

# Analyze the full network structure and identify hub neurons
python real_network_analysis.py

# Analyze all neurotransmitter-specific subnetworks
python nt_subnetwork_analysis.py
```

**Outputs:**

- `results/real_network_summary.csv` — Overall network metrics
- `results/hub_neurons.csv` — Top 100 hub neurons with NT labels
- `results/nt_subnetwork_stats.csv` — Statistics for all 21 NT-pair subnetworks

**Runtime:** ~2 minutes

---

### Step 2: Bootstrap Confidence Intervals

```bash
# Generate bootstrap CIs for transitivity (1,000 iterations)
python bootstrap_nt_transitivity.py
```

**Outputs:**

- `results/bootstrap_nt_transitivity_samples.csv` — All 1,000 bootstrap samples
- `results/bootstrap_nt_transitivity_summary.csv` — Summary statistics
- `results/bootstrap_nt_transitivity_ci.csv` — 95% confidence intervals

**Runtime:** ~5 minutes

---

### Step 3: Permutation Test

```bash
# Run permutation test (1,000 iterations with shuffled NT labels)
python permutation_test_nt.py

# Analyze permutation test results
python permutation_test_analysis.py
```

**Outputs:**

- `results/permutation_test_results.csv` — All 1,000 permutation samples
- `results/permutation_test_summary.csv` — Summary statistics and p-values

**Runtime:** ~30 minutes (1,000 iterations)

---

### Step 4: Supplementary Analyses

```bash
# Test GABA hub enrichment across thresholds (k=10 to k=500)
python hub_sensitivity.py

# Generate supplementary table with all 21 NT-pair combinations
python generate_supplementary_table.py
```

**Outputs:**

- `results/hub_sensitivity.csv` — GABA enrichment across hub thresholds
- `results/supplementary_table_s1_all_21_pairs.csv` — Complete NT-pair statistics

**Runtime:** ~1 minute

---

### Step 5: Generate Publication Figures

```bash
# Generate all figures for the paper
python generate_paper_figures.py
```

**Outputs (both PNG and PDF):**

- `figures/figure1_transitivity_comparison.{png,pdf}`
- `figures/figure2_subnetwork_heatmap.{png,pdf}`
- `figures/figure3_hub_composition.{png,pdf}`
- `figures/figure4_degree_distribution.{png,pdf}`

**Runtime:** ~30 seconds

---

## Quick Start: Just Regenerate Figures

Pre-computed results are included in `results/`, so you can skip directly to figure generation:

```bash
cd analysis
python generate_paper_figures.py
```

This will regenerate all publication figures from the pre-computed results.

---

## Analysis Scripts Details

### `real_network_analysis.py`

Analyzes the full reciprocal network:

- Degree distribution and power-law fitting
- Clustering coefficient and small-world metrics
- Hub identification (top 100 by degree)
- Rich club analysis (top 20 hubs)
- Neurotransmitter composition of hubs

**Key functions:**

- `compute_network_stats()` — Overall network metrics
- `identify_hubs()` — Extract top-degree neurons
- `test_gaba_enrichment()` — Binomial test for GABA over-representation

---

### `nt_subnetwork_analysis.py`

Constructs and analyzes all 21 neurotransmitter-specific subnetworks:

- Same-NT pairs (6 combinations: GABA-GABA, ACh-ACh, etc.)
- Cross-NT pairs (15 combinations: GABA-ACh, ACh-Glut, etc.)

**Metrics computed per subnetwork:**

- Number of edges (reciprocal pairs)
- Number of nodes (neurons)
- Transitivity (clustering coefficient)
- Number of triangles
- Giant component size and fraction
- Average degree

**Key functions:**

- `extract_nt_subnetwork()` — Build NT-specific graph
- `compute_subnetwork_stats()` — Calculate all metrics

---

### `bootstrap_nt_transitivity.py`

Generates bootstrap confidence intervals for transitivity estimates:

1. Resample reciprocal pairs with replacement
2. Reconstruct subnetwork from resampled pairs
3. Compute transitivity
4. Repeat 1,000 times
5. Report percentile-based 95% CIs

**Key parameters:**

- `n_iterations = 1000`
- `random_seed = 42`
- Focuses on GABA-GABA and ACh-GABA pairs

---

### `permutation_test_nt.py`

Tests the null hypothesis that NT identity doesn't affect clustering:

1. Shuffle NT labels across neurons
2. Preserve overall NT distribution and network structure
3. Recompute GABA-GABA transitivity
4. Repeat 1,000 times
5. Compare observed value to null distribution

**Key parameters:**

- `n_permutations = 1000`
- `random_seed = 42`

**Note:** This is computationally intensive (~30 min) because it reconstructs the full network 1,000 times.

---

### `hub_sensitivity.py`

Tests robustness of GABA hub enrichment across thresholds:

- Varies hub threshold from k=10 to k=500
- Computes GABA fraction at each threshold
- Performs binomial test for enrichment
- Plots enrichment vs. threshold

**Output:** `results/hub_sensitivity.csv`

---

### `generate_paper_figures.py`

Produces all publication-ready figures:

- **Figure 1:** Transitivity comparison (GABA-GABA vs. ACh-GABA)
- **Figure 2:** NT-pair subnetwork heatmap
- **Figure 3:** Hub composition pie chart
- **Figure 4:** Degree distribution with power-law fit

Uses seaborn for statistical plotting and matplotlib for customization.

---

## Data Files

### Primary Dataset

**File:** `data/v630-all-reciprocal-pairs-s1.csv`

**Columns:**

- `pre_root_id` — Presynaptic neuron ID
- `post_root_id` — Postsynaptic neuron ID
- `pre_nt` — Presynaptic neurotransmitter
- `post_nt` — Postsynaptic neurotransmitter
- `weight` — Number of synapses (always ≥2 for reciprocal pairs)

**Source:** FlyWire v630 connectome via codex.flywire.ai

**License:** CC-BY 4.0 by the FlyWire consortium

---

### Classification Files

Additional neuron classifications in `data/classifications/`:

- `rich_club_neurons.csv` — Top 20 highest-degree hubs
- `broadcast_neurons.csv` — High out-degree neurons
- `integrate_neurons.csv` — High in-degree neurons
- `all_sensory.csv` — Sensory neurons
- `intrinsic_balanced_neurons.csv` — Balanced in/out-degree

---

## Computational Requirements

### Hardware

- **RAM:** 16 GB recommended (8 GB minimum)
- **CPU:** Multi-core recommended for bootstrap/permutation tests
- **Storage:** ~500 MB for data + results

### Runtime Summary

| Script                            | Runtime     |
| --------------------------------- | ----------- |
| `real_network_analysis.py`        | ~2 min      |
| `nt_subnetwork_analysis.py`       | ~2 min      |
| `bootstrap_nt_transitivity.py`    | ~5 min      |
| `permutation_test_nt.py`          | ~30 min     |
| `permutation_test_analysis.py`    | <1 min      |
| `hub_sensitivity.py`              | ~1 min      |
| `generate_supplementary_table.py` | <1 min      |
| `generate_paper_figures.py`       | ~30 sec     |
| **Total (full pipeline)**         | **~40 min** |

---

## Reproducibility Notes

### Random Seeds

All stochastic analyses use **seed=42** for reproducibility:

- Bootstrap resampling
- Permutation tests
- Any random network generation

### Software Versions

Analysis was performed with:

- Python 3.10.12
- NetworkX 3.2.1
- NumPy 1.26.3
- Pandas 2.1.4
- Matplotlib 3.8.2
- Seaborn 0.13.1
- SciPy 1.11.4

Minor version differences should not affect results, but exact version matching ensures bit-for-bit reproducibility.

---

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install --upgrade -r requirements.txt
```

### Memory Issues

If bootstrap or permutation tests run out of memory:

1. Reduce `n_iterations` in the script
2. Use a machine with more RAM
3. Process subnetworks separately

### File Not Found Errors

Ensure you're running scripts from the `analysis/` directory:

```bash
cd analysis
python script_name.py
```

Scripts expect data files at `../data/` and write to `../results/` and `../figures/`.

---

## Citation

If you use this code, please cite:

```bibtex
@software{flywire_gaba_topology_code,
  title={Analysis Code for Neurotransmitter-Specific Clustering in Drosophila Connectome},
  author={[Author]},
  year={2026},
  url={https://github.com/yourusername/flywire-gaba-topology}
}
```

---

## License

This project is licensed under the **MIT License** — see [LICENSE](https://github.com/yourusername/flywire-gaba-topology/blob/master/LICENSE) for details.

The FlyWire data is licensed under **CC-BY 4.0** by the FlyWire consortium.

---

[← Back to Home](index.md) | [← Methods](methods.md) | [← Results](results.md)
