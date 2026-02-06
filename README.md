# Neurotransmitter-Specific Clustering Reveals Distinct Topological Roles in the *Drosophila* Brain Connectome

Analysis code and data for the paper investigating how neurotransmitter identity shapes network topology in the FlyWire v630 whole-brain connectome.

**🌐 [View Project Website](https://yourusername.github.io/flywire-gaba-topology/)** — Interactive documentation with detailed methods, results, and visualizations

## Key Findings

1. **GABA-GABA transitivity (0.396)** exceeds ACh-GABA transitivity (0.0005) by **~714-fold** (95% CI: 607–883×, permutation test *p* < 0.001)
2. **100% of the 20 highest-degree hub neurons are GABAergic** (*p* < 10⁻⁹, binomial test)
3. The network exhibits **scale-free** degree distribution (α = 2.37) and **small-world** properties (125× higher clustering than random graphs)

## Repository Structure

```
flywire-gaba-topology/
├── analysis/                          # All analysis scripts
│   ├── bootstrap_nt_transitivity.py   # Bootstrap CIs for NT-pair transitivity (Fig 1)
│   ├── nt_subnetwork_analysis.py      # NT-pair subnetwork statistics (Fig 2, 4)
│   ├── real_network_analysis.py       # Hub analysis, degree distribution (Fig 3)
│   ├── permutation_test_nt.py         # 1000-iteration permutation test (raw)
│   ├── permutation_test_analysis.py   # Permutation test post-hoc analysis
│   ├── generate_paper_figures.py      # Generate Figures 1-4 from results
│   ├── generate_supplementary_table.py# All 21 NT-pair statistics (Table S1)
│   └── hub_sensitivity.py            # GABA hub enrichment across thresholds
├── data/
│   ├── v630-all-reciprocal-pairs-s1.csv  # FlyWire v630 reciprocal pairs (180,799 pairs)
│   └── classifications/              # Neuron classification CSVs
│       ├── rich_club_neurons.csv
│       ├── broadcast_neurons.csv
│       ├── integrate_neurons.csv
│       ├── all_sensory.csv
│       └── intrinsic_balanced_neurons.csv
├── results/                           # Pre-computed results (CSV)
├── figures/                           # Generated figures (PNG + PDF)
├── paper/
│   └── manuscript.md                  # Paper draft
├── requirements.txt
├── LICENSE
└── README.md
```

## Reproducing the Analysis

### Prerequisites

```bash
pip install -r requirements.txt
```

Python ≥ 3.10 is required. The analysis uses NetworkX, python-igraph, NumPy, Pandas, matplotlib, scipy, and seaborn.

### Running the Analysis

Scripts should be run from the `analysis/` directory. Each script reads data from `../data/` and writes results to `../results/` and figures to `../figures/`.

**Recommended execution order:**

```bash
cd analysis

# Step 1: Core network statistics and hub analysis
python real_network_analysis.py
python nt_subnetwork_analysis.py

# Step 2: Bootstrap confidence intervals (~5 min)
python bootstrap_nt_transitivity.py

# Step 3: Permutation test (~30 min for 1000 iterations)
python permutation_test_nt.py
python permutation_test_analysis.py

# Step 4: Supplementary analyses
python hub_sensitivity.py
python generate_supplementary_table.py

# Step 5: Generate publication figures
python generate_paper_figures.py
```

Pre-computed results are included in `results/` so you can skip directly to Step 5 if you just want to regenerate figures.

## Data

The primary dataset (`data/v630-all-reciprocal-pairs-s1.csv`) is derived from the [FlyWire v630 connectome](https://codex.flywire.ai/) (Dorkenwald et al., 2024). It contains 180,799 reciprocal synaptic pairs among 77,607 neurons with neurotransmitter predictions from Eckstein et al. (2024). The data is released under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/) by the FlyWire consortium.

**Neurotransmitter types:** ACh, GABA, Glutamate, Serotonin, Dopamine, Octopamine

## GitHub Pages Website

Visit our [project website](https://yourusername.github.io/flywire-gaba-topology/) for:
- Interactive documentation and visualizations
- Detailed methodology and statistical analyses
- Comprehensive results with all figures
- Code documentation and reproducibility guide

The website is built with Jekyll and hosted on GitHub Pages in the `docs/` directory.

## Citation

If you use this code or analysis, please cite:

> [Author]. Neurotransmitter-Specific Clustering Reveals Distinct Topological Roles in the *Drosophila* Brain Connectome. *bioRxiv* (2026). doi: [pending]

And the FlyWire dataset:

> Dorkenwald, S. et al. Neuronal wiring diagram of an adult brain. *Nature* 634, 124–138 (2024).

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
