---
layout: default
title: Results
---

# Results

Comprehensive results from the neurotransmitter-specific topology analysis.

---

## 1. GABA-GABA Connections Form Highly Clustered Modules

The most striking finding is the **extreme difference in clustering** between GABA-GABA and cross-transmitter connections.

### Key Statistics

| Metric                 | Value                                |
| ---------------------- | ------------------------------------ |
| GABA-GABA transitivity | **0.396** (95% CI: 0.380-0.412)      |
| ACh-GABA transitivity  | **0.0005** (95% CI: 0.00042-0.00058) |
| Fold difference        | **~714×** (95% CI: 607–883×)         |
| Bootstrap p-value      | **< 0.001** (1,000 iterations)       |

In 1,000 bootstrap samples, **100% showed GABA-GABA transitivity exceeding ACh-GABA transitivity**.

### Permutation Test Confirmation

A permutation test (1,000 iterations with shuffled NT labels) confirmed that this clustering difference is attributable to NT identity:

| Statistic                       | Value          |
| ------------------------------- | -------------- |
| Observed GABA-GABA transitivity | **0.396**      |
| Null mean                       | 0.041          |
| Null median                     | 0.024          |
| Null 95% CI                     | [0.005, 0.117] |
| Maximum null value              | 0.181          |
| Fold above null mean            | **9.7×**       |
| **p-value**                     | **< 0.001**    |

The observed value exceeds the maximum null value by **more than 2-fold**, providing strong evidence that GABA-specific clustering is not attributable to chance or network topology alone.

### Interpretation

**GABAergic neurons preferentially form local triangular motifs** with other GABAergic neurons. When a GABA neuron connects to another GABA neuron, their shared GABA neighbors are likely to also connect — creating dense inhibitory clusters.

In contrast, when GABA neurons connect to ACh neurons, those pairs **rarely share mutual connections**, forming sparse, tree-like structures.

---

## 2. Full Neurotransmitter-Specific Results

Transitivity varies systematically across NT pair types:

### Primary Subnetworks

| NT Pair       | N Pairs | N Neurons | Transitivity | Giant Component % |
| ------------- | ------- | --------- | ------------ | ----------------- |
| **GABA-GABA** | 10,214  | 6,832     | **0.396**    | 44.7%             |
| **ACh-ACh**   | 18,754  | 17,578    | 0.062        | 33.9%             |
| **Glut-Glut** | 5,144   | 5,178     | 0.061        | 27.0%             |
| **GABA-Glut** | 10,459  | 10,912    | 0.003        | 50.8%             |
| **ACh-Glut**  | 32,815  | 28,463    | 0.002        | 58.8%             |
| **ACh-GABA**  | 90,968  | 52,995    | **0.0005**   | 91.3%             |

### Key Patterns

1. **Same-NT pairs show consistently higher transitivity** than cross-NT pairs
2. **GABA-GABA has the highest transitivity** (0.396), followed by:
   - Serotonin-Serotonin: 0.299
   - Dopamine-Dopamine: 0.149
   - All three are inhibitory or neuromodulatory
3. **ACh-GABA has the lowest non-zero transitivity** (0.0005) despite having the **most edges** (90,968 pairs)
4. **Giant component fraction inversely correlates with transitivity**
   - High clustering → fragmented modules
   - Low clustering → spanning networks

### All 21 NT-Pair Combinations

Full statistics for all neurotransmitter pair combinations are available in [Supplementary Table S1](https://github.com/jknight137/flywire-gaba-topology/blob/master/results/supplementary_table_s1_all_21_pairs.csv).

---

## 3. GABAergic Neurons Dominate Network Hubs

Analysis of the **20 highest-degree hub neurons** (degree ≥ 708) reveals striking GABAergic enrichment.

### Hub Composition

| Category           | Count  | Percentage | Expected under null |
| ------------------ | ------ | ---------- | ------------------- |
| **GABAergic**      | **20** | **100%**   | 3.2 neurons         |
| Cholinergic        | 0      | 0%         | 9.1 neurons         |
| Glutamatergic      | 0      | 0%         | 4.7 neurons         |
| Other (DA/Ser/Oct) | 0      | 0%         | 3.0 neurons         |

### Statistical Significance

- **Enrichment:** 6.2-fold over baseline GABAergic fraction (16.2%)
- **Binomial test:** _p_ < 10⁻⁹
- **Robustness:** Enrichment persists across hub thresholds from k=10 to k=500

### Interpretation

This is not merely that GABAergic neurons are somewhat over-represented among hubs — **every single one of the top 20 hubs is GABAergic**. This suggests that:

1. **GABAergic neurons form the structural backbone** of the connectome
2. **Inhibitory control is centralized** through high-degree hubs
3. **The network architecture favors inhibitory coordination** at the global level

---

## 4. Scale-Free and Small-World Properties

The full reciprocal network exhibits characteristic complex network properties.

### Degree Distribution

- **Power-law exponent:** α = 2.37
- **Distribution type:** Heavy-tailed, consistent with scale-free topology
- **Interpretation:** Network contains a few highly connected hubs and many low-degree nodes

### Small-World Architecture

| Metric                 | Observed | Random Network | Ratio    |
| ---------------------- | -------- | -------------- | -------- |
| Clustering coefficient | 0.125    | 0.001          | **125×** |
| Average path length    | ~3.5     | ~3.2           | 1.1×     |

**Small-world criteria met:**

- ✓ High clustering relative to random network
- ✓ Short average path length similar to random network

### Biological Significance

Small-world topology enables:

- **Efficient information transfer** (short paths)
- **Modular processing** (high clustering)
- **Robustness to damage** (multiple redundant paths)

---

## 5. Sensitivity Analyses

### Hub Threshold Sensitivity

We tested GABA enrichment across hub thresholds from k=10 to k=500:

| Hub Threshold | GABA % | Baseline % | Enrichment | p-value  |
| ------------- | ------ | ---------- | ---------- | -------- |
| Top 10        | 100%   | 16.2%      | 6.2×       | < 10⁻⁵   |
| Top 20        | 100%   | 16.2%      | 6.2×       | < 10⁻⁹   |
| Top 50        | 96%    | 16.2%      | 5.9×       | < 10⁻²⁰  |
| Top 100       | 89%    | 16.2%      | 5.5×       | < 10⁻³⁵  |
| Top 500       | 68%    | 16.2%      | 4.2×       | < 10⁻¹⁰⁰ |

**Conclusion:** GABA enrichment is **extremely robust** and persists at all tested thresholds.

### Bootstrap Stability

All reported confidence intervals are based on 1,000 bootstrap iterations with resampling. Key findings:

- **GABA-GABA transitivity:** 95% CI = [0.380, 0.412] — narrow, stable estimate
- **Fold difference:** 95% CI = [607×, 883×] — consistently extreme across resamples
- **No overlap** between GABA-GABA and ACh-GABA bootstrap distributions

---

## 6. Component Structure

Clustering patterns are reflected in component fragmentation:

### Same-NT Networks (High Clustering)

- **GABA-GABA:** 44.7% in giant component → **55% fragmented**
- **ACh-ACh:** 33.9% in giant component → **66% fragmented**
- **Glut-Glut:** 27.0% in giant component → **73% fragmented**

Same-NT networks form **multiple disconnected modules**, consistent with local processing units.

### Cross-NT Networks (Low Clustering)

- **ACh-GABA:** 91.3% in giant component → **9% fragmented**
- **ACh-Glut:** 58.8% in giant component → **41% fragmented**
- **GABA-Glut:** 50.8% in giant component → **49% fragmented**

Cross-NT networks form **large spanning structures**, consistent with long-range coordination.

---

## Summary of Key Results

1. **714-fold clustering difference** between GABA-GABA (0.396) and ACh-GABA (0.0005)
2. **100% of top 20 hubs are GABAergic** (_p_ < 10⁻⁹)
3. **Scale-free degree distribution** (α = 2.37)
4. **Small-world architecture** (125× random clustering)
5. **Inverse correlation** between clustering and giant component fraction
6. **Robust across thresholds** and statistical tests

These findings collectively suggest that **GABAergic neurons occupy a privileged topological position**, serving as both densely clustered local modules and centralized global coordinators.

---

[← Back to Home](index.md) | [← Methods](methods.md) | [Code & Reproducibility →](code.md)
