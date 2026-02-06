---
layout: default
title: Home
---

# Neurotransmitter-Specific Clustering Reveals Distinct Topological Roles in the _Drosophila_ Brain Connectome

<div class="hero">
  <p class="lead">A computational neuroscience study revealing how GABAergic neurons dominate network hubs and form highly clustered local circuits in the <em>Drosophila</em> brain connectome.</p>
</div>

---

## Key Findings

<div class="findings-grid">
  <div class="finding">
    <h3>🔬 714-Fold Clustering Difference</h3>
    <p>GABA-GABA transitivity (0.396) exceeds ACh-GABA transitivity (0.0005) by <strong>~714-fold</strong> (95% CI: 607–883×, <em>p</em> < 0.001)</p>
  </div>
  
  <div class="finding">
    <h3>🎯 100% GABA Hub Dominance</h3>
    <p><strong>All 20 highest-degree hub neurons are GABAergic</strong> (<em>p</em> < 10⁻⁹), representing a 6.2-fold enrichment over baseline</p>
  </div>
  
  <div class="finding">
    <h3>🌐 Small-World Architecture</h3>
    <p>The network exhibits <strong>scale-free</strong> degree distribution (α = 2.37) and 125× higher clustering than random graphs</p>
  </div>
</div>

---

## Abstract

The FlyWire connectome provides an unprecedented view of synaptic connectivity in the adult _Drosophila_ brain, including neurotransmitter identity for most neurons. We analyzed the topological structure of neurotransmitter-specific subnetworks within **180,799 reciprocal synaptic pairs** among **77,607 neurons**.

Our analysis reveals three major findings:

1. **GABAergic neurons form highly clustered local modules** — GABA-GABA connections show extreme transitivity compared to cross-transmitter connections
2. **The network exhibits heavy-tailed degree distribution** consistent with scale-free properties (power-law exponent α = 2.37)
3. **Most strikingly, 100% of the 20 highest-degree hub neurons are GABAergic** — a remarkable enrichment suggesting inhibitory neurons form the control backbone of the connectome

These findings suggest that inhibitory circuits serve a dual topological role: forming dense local processing units while simultaneously providing brain-wide coordination through hub architecture.

---

## Data & Methods

### Dataset

- **Source:** [FlyWire v630 connectome](https://codex.flywire.ai/) (Dorkenwald et al., 2024)
- **Neurons:** 77,607 neurons with neurotransmitter predictions
- **Connections:** 180,799 reciprocal synaptic pairs
- **Neurotransmitter types:** ACh, GABA, Glutamate, Serotonin, Dopamine, Octopamine
- **License:** CC-BY 4.0 by the FlyWire consortium

### Analysis Approach

We constructed 21 neurotransmitter-specific subnetworks (6 same-type + 15 cross-type) and characterized:

- **Clustering:** Transitivity (ratio of closed triangles to connected triples)
- **Hub composition:** Neurotransmitter identity of highest-degree neurons
- **Component structure:** Giant component fraction
- **Statistical validation:** Bootstrap confidence intervals (1,000 iterations) and permutation tests

All code is available in our [GitHub repository](https://github.com/jknight137/flywire-gaba-topology).

---

## Results Summary

### Extreme Clustering Differences

| NT Pair   | N Pairs | Transitivity | Giant Component |
| --------- | ------- | ------------ | --------------- |
| GABA-GABA | 10,214  | **0.396**    | 44.7%           |
| ACh-ACh   | 18,754  | 0.062        | 33.9%           |
| Glut-Glut | 5,144   | 0.061        | 27.0%           |
| ACh-GABA  | 90,968  | **0.0005**   | 91.3%           |
| ACh-Glut  | 32,815  | 0.002        | 58.8%           |
| GABA-Glut | 10,459  | 0.003        | 50.8%           |

**Key observation:** Same-neurotransmitter pairs show consistently higher clustering than cross-transmitter pairs, with GABA-GABA exhibiting the most extreme clustering.

### Hub Neuron Composition

Analysis of the 20 highest-degree neurons (degree ≥ 708):

- **GABAergic:** 20/20 (100%)
- **Expected under null:** 3.2 neurons
- **Enrichment:** 6.2-fold
- **Statistical significance:** _p_ < 10⁻⁹ (binomial test)

This enrichment is robust across hub thresholds from k=10 to k=500.

---

## Biological Implications

Our findings suggest that **GABAergic neurons occupy a privileged position** in the _Drosophila_ brain network:

1. **Local processing:** High GABA-GABA clustering enables dense inhibitory modules for gain control and lateral inhibition
2. **Global coordination:** GABA hub dominance positions inhibitory neurons as central coordinators of brain-wide activity
3. **Dual architecture:** This combination of local clustering + hub dominance may reflect fundamental constraints on neural computation

The extreme segregation between inhibitory (clustered) and excitatory (sparse) topologies suggests distinct computational roles that transcend anatomy.

---

## Resources

<div class="resource-links">
  <a href="https://github.com/yourusername/flywire-gaba-topology" class="btn">📦 GitHub Repository</a>
  <a href="https://github.com/yourusername/flywire-gaba-topology/tree/master/data" class="btn">📊 Dataset</a>
  <a href="https://github.com/yourusername/flywire-gaba-topology/tree/master/analysis" class="btn">💻 Analysis Code</a>
  <a href="https://github.com/yourusername/flywire-gaba-topology/tree/master/results" class="btn">📈 Results</a>
</div>

---

## Citation

If you use this work, please cite:

```bibtex
@article{flywire_gaba_2026,
  title={Neurotransmitter-Specific Clustering Reveals Distinct Topological Roles in the Drosophila Brain Connectome},
  author={[Author]},
  journal={bioRxiv},
  year={2026},
  doi={[pending]}
}
```

**FlyWire dataset citation:**

```bibtex
@article{dorkenwald2024neuronal,
  title={Neuronal wiring diagram of an adult brain},
  author={Dorkenwald, Sven and others},
  journal={Nature},
  volume={634},
  pages={124--138},
  year={2024}
}
```

---

## Contact & Collaboration

Interested in collaborating or have questions? Please [open an issue](https://github.com/jknight137/flywire-gaba-topology/issues) on our GitHub repository.

---

<div class="footer-note">
  <p><em>This research uses data from the FlyWire consortium (CC-BY 4.0 license). Neurotransmitter predictions from Eckstein et al. (2024).</em></p>
</div>
