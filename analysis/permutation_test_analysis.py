import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / 'results'
FIGURES_DIR = Path(__file__).resolve().parent.parent / 'figures'
FIGURES_DIR.mkdir(exist_ok=True)

OBSERVED_GABA_GABA = 0.3962489482398285
OBSERVED_ACH_GABA = 0.0005375292100965318

def main():
    print('Permutation Test Analysis (Corrected)')
    df = pd.read_csv(RESULTS_DIR / 'permutation_test_results.csv')
    n_perm = len(df)
    print('Loaded', n_perm, 'permutation iterations')

    null_gaba = df['gaba_gaba_transitivity'].values
    null_ach_gaba = df['ach_gaba_transitivity'].values

    p_value_gaba = np.sum(null_gaba >= OBSERVED_GABA_GABA) / n_perm

    null_mean = np.mean(null_gaba)
    null_median = np.median(null_gaba)
    null_std = np.std(null_gaba)
    null_ci_low = np.percentile(null_gaba, 2.5)
    null_ci_high = np.percentile(null_gaba, 97.5)
    null_max = np.max(null_gaba)
    fold_vs_null = OBSERVED_GABA_GABA / null_mean

    print('--- GABA-GABA Transitivity ---')
    print('Observed:', round(OBSERVED_GABA_GABA, 4))
    print('Null mean:', round(null_mean, 4))
    print('Null median:', round(null_median, 4))
    print('Null std:', round(null_std, 4))
    print('Null 95pct CI: [' + str(round(null_ci_low, 4)) + ', ' + str(round(null_ci_high, 4)) + ']')
    print('Null max:', round(null_max, 4))
    print('Fold (obs/null):', round(fold_vs_null, 1))
    print('p-value:', p_value_gaba)
    if p_value_gaba == 0:
        print('  => p <', round(1/n_perm, 4), '(none of', n_perm, 'permutations reached observed)')

    n_ach_zero = np.sum(null_ach_gaba == 0.0)
    print('--- ACh-GABA Under Null ---')
    print('Observed:', round(OBSERVED_ACH_GABA, 6))
    print('Null == 0.0:', str(n_ach_zero) + '/' + str(n_perm))

    p_val_str = str(p_value_gaba) if p_value_gaba > 0 else '<' + str(1/n_perm)
    summary = pd.DataFrame([{
        'test': 'GABA-GABA transitivity vs null',
        'observed_gaba_gaba': OBSERVED_GABA_GABA,
        'null_mean_gaba_gaba': null_mean,
        'null_median_gaba_gaba': null_median,
        'null_std_gaba_gaba': null_std,
        'null_ci_95_low': null_ci_low,
        'null_ci_95_high': null_ci_high,
        'null_max': null_max,
        'fold_obs_vs_null_mean': fold_vs_null,
        'p_value': p_val_str,
        'n_permutations': n_perm,
        'ach_gaba_null_zero_frac': n_ach_zero / n_perm,
    }])
    summary.to_csv(RESULTS_DIR / 'permutation_test_summary.csv', index=False)
    print('Saved summary')

    # Figure
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    ax.hist(null_gaba, bins=50, color='#3498DB', alpha=0.7, edgecolor='black', label='Null distribution')
    ax.axvline(OBSERVED_GABA_GABA, color='#E74C3C', linewidth=2.5, linestyle='--',
               label='Observed = ' + str(round(OBSERVED_GABA_GABA, 4)))
    ax.axvline(null_mean, color='#2ECC71', linewidth=1.5, linestyle=':',
               label='Null mean = ' + str(round(null_mean, 4)))
    ax.set_xlabel('GABA-GABA Transitivity')
    ax.set_ylabel('Count')
    ax.set_title('A. Permutation Test: GABA-GABA Transitivity')
    ax.legend(fontsize=9)
    p_str = 'p < ' + str(round(1/n_perm, 4)) if p_value_gaba == 0 else 'p = ' + str(round(p_value_gaba, 4))
    ax.text(0.95, 0.85, p_str + '\n' + str(round(fold_vs_null, 1)) + 'x enrichment\nn = ' + str(n_perm),
            transform=ax.transAxes, ha='right', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax = axes[1]
    ax.hist(null_gaba, bins=50, color='#3498DB', alpha=0.7, edgecolor='black', label='Null (shuffled labels)')
    ax.axvline(OBSERVED_GABA_GABA, color='#E74C3C', linewidth=2.5, linestyle='--',
               label='Observed (' + str(round(OBSERVED_GABA_GABA, 3)) + ')')
    ax.set_xlim(-0.01, OBSERVED_GABA_GABA * 1.1)
    ax.set_xlabel('GABA-GABA Transitivity')
    ax.set_ylabel('Count')
    ax.set_title('B. Full Scale: Observed vs Null')
    ax.legend(fontsize=9)
    ylim = ax.get_ylim()
    ax.annotate('', xy=(OBSERVED_GABA_GABA, ylim[1]*0.5),
                xytext=(null_max, ylim[1]*0.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    gap_mid = (OBSERVED_GABA_GABA + null_max) / 2
    ax.text(gap_mid, ylim[1]*0.55, str(round(fold_vs_null)) + 'x gap',
            ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'permutation_test_null_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'permutation_test_null_distribution.pdf', bbox_inches='tight')
    plt.close()
    print('Saved figures')
    print('DONE')

if __name__ == '__main__':
    main()