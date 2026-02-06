import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import binomtest
from collections import Counter

RESULTS_DIR = Path(__file__).resolve().parent.parent / 'results'
FIGURES_DIR = Path(__file__).resolve().parent.parent / 'figures'
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
FIGURES_DIR.mkdir(exist_ok=True)

def main():
    print('Hub Sensitivity Analysis')

    pairs = pd.read_csv(DATA_DIR / 'v630-all-reciprocal-pairs-s1.csv')
    print('Loaded', len(pairs), 'reciprocal pairs')

    # Build neuron -> NT mapping
    nt_map = {}
    for _, row in pairs.iterrows():
        nt_map[row['n1']] = row['n1_nt']
        nt_map[row['n2']] = row['n2_nt']
    print('Mapped', len(nt_map), 'neurons to NT labels')

    overall_gaba_frac = sum(1 for nt in nt_map.values() if nt == 'gaba') / len(nt_map)
    print('Overall GABA fraction:', round(overall_gaba_frac, 3))

    # Compute degree for each neuron from pairs
    degree_counter = Counter()
    for _, row in pairs.iterrows():
        degree_counter[row['n1']] += 1
        degree_counter[row['n2']] += 1

    # Sort by degree descending
    sorted_neurons = sorted(degree_counter.items(), key=lambda x: -x[1])
    print('Total neurons with degree info:', len(sorted_neurons))
    print('Top neuron degree:', sorted_neurons[0][1])

    k_values = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
    results = []

    for k in k_values:
        top_k_neurons = [n for n, d in sorted_neurons[:k]]
        n_gaba = sum(1 for n in top_k_neurons if nt_map.get(n) == 'gaba')
        gaba_pct = 100.0 * n_gaba / k
        enrichment = gaba_pct / (overall_gaba_frac * 100)
        bt = binomtest(n_gaba, k, overall_gaba_frac, alternative='greater')
        p_val = bt.pvalue
        results.append({
            'k': k, 'n_gaba': n_gaba, 'gaba_pct': gaba_pct,
            'expected_gaba_pct': overall_gaba_frac * 100,
            'enrichment_fold': enrichment, 'p_value': p_val,
        })
        print('  k=' + str(k) + ': ' + str(n_gaba) + '/' + str(k) + ' GABA (' + str(round(gaba_pct,1)) + '%), enrichment=' + str(round(enrichment,2)) + 'x, p=' + '{:.2e}'.format(p_val))

    results_df = pd.DataFrame(results)
    results_df.to_csv(RESULTS_DIR / 'hub_sensitivity.csv', index=False)
    print('Saved results')

    # Figure
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(8, 5))
    ks = results_df['k'].values
    gaba_pcts = results_df['gaba_pct'].values
    expected = results_df['expected_gaba_pct'].values[0]

    ax.plot(ks, gaba_pcts, 'o-', color='#E74C3C', linewidth=2, markersize=8, label='Observed GABA %')
    ax.axhline(expected, color='#95A5A6', linestyle='--', linewidth=1.5,
               label='Expected (' + str(round(expected, 1)) + '%)')
    ax.fill_between(ks, expected, gaba_pcts, alpha=0.15, color='#E74C3C')

    for _, row in results_df.iterrows():
        if row['p_value'] < 0.001:
            ax.text(row['k'], row['gaba_pct'] + 2, '***', ha='center', fontsize=9)
        elif row['p_value'] < 0.01:
            ax.text(row['k'], row['gaba_pct'] + 2, '**', ha='center', fontsize=9)
        elif row['p_value'] < 0.05:
            ax.text(row['k'], row['gaba_pct'] + 2, '*', ha='center', fontsize=9)

    ax.set_xlabel('Number of Top Hub Neurons (k)')
    ax.set_ylabel('GABAergic Neurons (%)')
    ax.set_title('GABAergic Enrichment Across Hub Thresholds')
    ax.set_ylim(0, 110)
    ax.set_xscale('log')
    ax.set_xticks(ks)
    ax.set_xticklabels([str(k) for k in ks], fontsize=9)
    ax.legend(fontsize=10, loc='upper right')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'hub_sensitivity.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'hub_sensitivity.pdf', bbox_inches='tight')
    plt.close()
    print('Saved figure')
    print('DONE')

if __name__ == '__main__':
    main()