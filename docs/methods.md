---
layout: default
title: Methods
---

# Methods

Detailed methodology for the neurotransmitter-specific topology analysis.

---

## Data Source

### FlyWire v630 Connectome

We used the FlyWire v630 connectome (Dorkenwald et al., 2024), accessed via [codex.flywire.ai](https://codex.flywire.ai/). This represents the most complete adult _Drosophila_ brain connectome to date.

**Dataset characteristics:**

- **77,607 neurons** in reciprocal network
- **180,799 reciprocal pairs** (bidirectional connections)
- **6 major neurotransmitter types** with predictions
- **License:** CC-BY 4.0 by the FlyWire consortium

### Neurotransmitter Predictions

Neurons were classified by primary neurotransmitter using predictions from Eckstein et al. (2024), which achieve approximately **90% accuracy** on held-out validation data.

We used the maximum-confidence prediction for each neuron without applying an additional confidence threshold, as the FlyWire dataset provides pre-filtered high-confidence predictions.

**Note:** ~10% misclassification would tend to blur boundaries between NT-specific subnetworks, making our reported transitivity differences **conservative estimates** of the true NT-specific clustering.

**Neurotransmitter types analyzed:**

- **GABA** (γ-aminobutyric acid) — primary inhibitory
- **ACh** (Acetylcholine) — primary fast excitatory
- **Glut** (Glutamate) — excitatory
- **DA** (Dopamine) — neuromodulatory
- **Ser/5-HT** (Serotonin) — neuromodulatory
- **Oct** (Octopamine) — neuromodulatory

---

## Network Construction

### Subnetwork Extraction

For each transmitter pair (e.g., GABA-GABA, GABA-ACh), we extracted the subgraph containing:

- **Nodes:** Neurons of the relevant transmitter type(s)
- **Edges:** Reciprocal pairs between nodes of the specified types

This produced **21 unique subnetworks**:

- 6 same-type subnetworks (GABA-GABA, ACh-ACh, etc.)
- 15 cross-type subnetworks (GABA-ACh, ACh-Glut, etc.)

We focused our primary analysis on the 6 largest subnetworks representing major connectivity patterns.

---

## Topological Metrics

### Clustering Coefficient (Transitivity)

We quantified local connectivity using **transitivity**, the ratio of closed triangles to connected triples:

$$
C = \frac{3 \times \text{triangles}}{\text{connected triples}}
$$

**Why transitivity?**

- More robust to degree heterogeneity than local clustering coefficient
- Less sensitive to sampling effects
- Better captures global clustering patterns in large networks

**Interpretation:**

- High transitivity → clustered, modular structure
- Low transitivity → sparse, tree-like or star-like structure

### Giant Component Analysis

For each subnetwork, we identified connected components and computed the fraction of nodes in the largest (giant) component.

**Interpretation:**

- High fraction → connected, spanning network
- Low fraction → fragmented, modular structure

### Degree Distribution

We analyzed the degree distribution of the full reciprocal network to characterize hub structure.

**Metrics computed:**

- Power-law exponent (α) via maximum likelihood
- Goodness-of-fit to power-law vs. exponential models
- Hub composition by neurotransmitter type

---

## Statistical Methods

### Bootstrap Confidence Intervals

Reciprocal pairs are **not independent samples** — they share correlation structure through common neurons and anatomical constraints.

**Bootstrap procedure:**

1. Resample reciprocal pairs with replacement (n = original count)
2. Reconstruct subnetwork from resampled pairs
3. Compute transitivity on resampled network
4. Repeat 1,000 times
5. Report 2.5th and 97.5th percentiles as 95% CI

This approach is **conservative**, as it preserves the correlation structure of the original data.

**Note:** Bootstrap means are typically lower than full-data values because resampling fragments the graph, reducing triangle counts. We report full-data values as point estimates and bootstrap CIs for uncertainty.

### Permutation Test for NT Identity

To test whether transitivity differences are attributable to NT identity rather than network topology alone, we performed a permutation test.

**Permutation procedure:**

1. Randomly shuffle NT labels across neurons
2. Preserve overall NT frequency distribution and graph structure (edges, degrees)
3. Recompute GABA-GABA transitivity
4. Repeat 1,000 iterations
5. Compare observed value to null distribution

**p-value:** Fraction of permutations where null transitivity ≥ observed transitivity

This tests the null hypothesis that NT identity has no effect on clustering patterns.

### Hub Enrichment Analysis

We identified hub neurons by degree (number of reciprocal connections) and tested for enrichment of specific neurotransmitter types.

**Binomial test:**

Under a null model where each hub's neurotransmitter identity is drawn independently from the population distribution, we computed:

$$
p = P(X \geq k) \text{ where } X \sim \text{Binomial}(n, p_0)
$$

- n = number of hubs tested
- k = number of GABAergic hubs observed
- p₀ = baseline GABAergic fraction in full network (0.162)

**Sensitivity analysis:** We varied the hub threshold from k=10 to k=500 to ensure robustness.

---

## Computational Implementation

### Software & Dependencies

All analyses were performed in **Python 3.10+** using:

- **NetworkX 3.2** — network analysis
- **python-igraph** — fast graph algorithms
- **NumPy 1.26** — numerical computation
- **Pandas 2.1** — data manipulation
- **matplotlib** — visualization
- **seaborn** — statistical plotting
- **scipy** — statistical tests

### Reproducibility

All analysis scripts are available in the [GitHub repository](https://github.com/jknight137/flywire-gaba-topology/tree/master/analysis).

**Execution order:**

```bash
cd analysis

# Core network statistics
python real_network_analysis.py
python nt_subnetwork_analysis.py

# Bootstrap CIs (~5 min)
python bootstrap_nt_transitivity.py

# Permutation test (~30 min)
python permutation_test_nt.py
python permutation_test_analysis.py

# Supplementary analyses
python hub_sensitivity.py
python generate_supplementary_table.py

# Generate figures
python generate_paper_figures.py
```

Pre-computed results are included in `results/` so you can skip directly to figure generation.

**Random seed:** All stochastic analyses use seed=42 for reproducibility.

---

## Data Availability

All data and code are publicly available:

- **Primary dataset:** [v630-all-reciprocal-pairs-s1.csv](https://github.com/jknight137/flywire-gaba-topology/tree/master/data)
- **Analysis code:** [analysis/](https://github.com/jknight137/flywire-gaba-topology/tree/master/analysis)
- **Pre-computed results:** [results/](https://github.com/jknight137/flywire-gaba-topology/tree/master/results)

---

## References

1. **Dorkenwald, S. et al.** (2024). Neuronal wiring diagram of an adult brain. _Nature_ 634, 124–138.
2. **Eckstein, N. et al.** (2024). Neurotransmitter classification from electron microscopy images at synaptic sites in _Drosophila_ melanogaster. _Cell_ 187, 2574–2594.
3. **FlyWire Consortium** — [https://codex.flywire.ai/](https://codex.flywire.ai/)

---

[← Back to Home](index.md) | [View Results →](results.md) | [Code & Reproducibility →](code.md)
