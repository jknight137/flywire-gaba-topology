---
layout: default
title: About
---

# About This Project

## Overview

This website presents research on neurotransmitter-specific topology in the *Drosophila* brain connectome using data from the FlyWire v630 whole-brain reconstruction.

## Research Context

### The FlyWire Connectome

The [FlyWire project](https://codex.flywire.ai/) represents one of the most ambitious neuroscience efforts to date: reconstructing every neuron and synapse in an adult *Drosophila melanogaster* brain. With over 130,000 neurons and millions of synapses, this dataset enables unprecedented analysis of neural circuit organization.

### Why Neurotransmitter-Specific Analysis?

Different neurotransmitters serve distinct computational roles:

- **GABA** provides inhibitory control and lateral inhibition
- **Acetylcholine** mediates fast excitatory transmission
- **Glutamate** drives feedforward excitation
- **Monoamines** (dopamine, serotonin, octopamine) modulate circuit activity

By analyzing how these different transmitter systems organize at the network level, we can understand fundamental principles of brain architecture.

## Key Discoveries

### 1. Extreme Clustering Segregation

GABAergic neurons form highly clustered local modules, while cross-transmitter connections form sparse spanning networks. This 714-fold difference suggests fundamentally distinct circuit motifs.

### 2. Hub Architecture

100% of the highest-degree hub neurons are GABAergic, indicating that inhibitory control is centralized through a small number of highly connected coordinators.

### 3. Dual Topological Role

The combination of local clustering + hub dominance suggests GABAergic neurons serve both:
- **Local processing:** Dense modules for gain control
- **Global coordination:** Central hubs for brain-wide synchronization

## Biological Implications

### Inhibitory Control as Network Backbone

The central position of GABAergic neurons in the network topology suggests that:

1. **Inhibition is prioritized architecturally** — Not just functionally important but structurally central
2. **Global state control** — High-degree GABA hubs can influence large portions of the network
3. **Computational efficiency** — Sparse excitation + dense inhibition may optimize energy use

### Evolutionary Constraints

The extreme segregation between inhibitory (clustered) and excitatory (sparse) topologies may reflect:

- **Stability requirements** — Prevent runaway excitation
- **Information processing** — Balance local integration with global broadcasting
- **Developmental constraints** — Different growth programs for inhibitory vs. excitatory neurons

## Data Sources

### Primary Data

- **FlyWire v630 connectome** (Dorkenwald et al., 2024)
- **77,607 neurons** with reciprocal connections
- **180,799 reciprocal pairs** (bidirectional synapses)
- **Neurotransmitter predictions** from Eckstein et al. (2024)

### Licensing

All FlyWire data is released under **CC-BY 4.0** by the FlyWire consortium. This allows free use with proper attribution.

Our analysis code is released under **MIT License** for maximum reusability.

## Technical Approach

### Network Science Methods

We used established network analysis techniques:

- **Transitivity (clustering coefficient)** — Measures local connectivity
- **Giant component analysis** — Tests network fragmentation
- **Degree distribution** — Characterizes hub structure
- **Bootstrap resampling** — Robust confidence intervals
- **Permutation tests** — Control for topology effects

### Software Stack

- **Python 3.10+** — Analysis environment
- **NetworkX** — Graph algorithms
- **NumPy/Pandas** — Data manipulation
- **Matplotlib/Seaborn** — Visualization
- **SciPy** — Statistical tests

All code is open source and available on GitHub.

## Impact & Applications

### Neuroscience

- **Circuit mapping principles** — How to organize large-scale networks
- **Inhibitory circuit design** — Dual role in computation
- **Comparative connectomics** — Test principles across species

### Network Science

- **Heterogeneous network analysis** — Multiple edge types
- **Clustering in biological networks** — Non-random motifs
- **Hub enrichment** — Functional specialization

### Computational Neuroscience

- **Biologically-inspired architectures** — AI/ML design principles
- **Neural network initialization** — Inhibitory connectivity patterns
- **Recurrent network design** — Balance excitation/inhibition

## Team & Collaboration

This is an open science project. We welcome:

- **Collaborations** — Extended analyses, cross-species comparisons
- **Questions** — Open issues on GitHub
- **Code contributions** — Pull requests for improvements
- **Data reuse** — All data and code freely available

## Publications

### Primary Paper

> [Author]. Neurotransmitter-Specific Clustering Reveals Distinct Topological Roles in the *Drosophila* Brain Connectome. *bioRxiv* (2026). doi: [pending]

### Related Work

- Dorkenwald, S. et al. (2024). Neuronal wiring diagram of an adult brain. *Nature* 634, 124–138.
- Eckstein, N. et al. (2024). Neurotransmitter classification from electron microscopy. *Cell* 187, 2574–2594.

## Acknowledgments

This work builds on the efforts of:

- **FlyWire Consortium** — Connectome reconstruction
- **Seung Lab** — Infrastructure and tools
- **Allen Institute** — Data curation
- **HHMI** — Funding and support

We thank the entire connectomics community for making this data available under open licenses.

## Contact

- **GitHub:** [github.com/yourusername/flywire-gaba-topology](https://github.com/yourusername/flywire-gaba-topology)
- **Issues:** [Report bugs or ask questions](https://github.com/yourusername/flywire-gaba-topology/issues)
- **Email:** [your.email@institution.edu](mailto:your.email@institution.edu)

## Website Information

This website is:

- **Built with:** Jekyll static site generator
- **Hosted on:** GitHub Pages
- **Theme:** Cayman with custom styling
- **Source:** Available in `docs/` folder of repository

To run locally: `bundle exec jekyll serve` from the `docs/` directory.

---

[← Back to Home](index.md)
