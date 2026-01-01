"""
Generate Regression Table for Subsidy-PHFSI Analysis
=====================================================

Creates publication-ready LaTeX table with 3 models:
1. Pooled OLS
2. Fixed Effects (Entity + Year)
3. Fixed Effects + Lagged Subsidy

Author: Claude Code + Daniel Polonia
Date: January 2026
"""

import pandas as pd
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "06_output"

# Regression results (manually entered from output)
results = {
    'Model 1': {
        'title': 'Pooled OLS',
        'subsidy_coef': -1.1418,
        'subsidy_se': 0.2023,
        'subsidy_pval': 0.0000,
        'lag_coef': None,
        'lag_se': None,
        'lag_pval': None,
        'covid_coef': -0.0094,
        'covid_se': 0.0233,
        'covid_pval': 0.6854,
        'r2': 0.5381,
        'r2_within': None,
        'n': 79,
        'entities': None,
        'entity_fe': False,
        'year_fe': False
    },
    'Model 2': {
        'title': 'Fixed Effects',
        'subsidy_coef': -0.4988,
        'subsidy_se': 0.1247,
        'subsidy_pval': 0.0004,
        'lag_coef': None,
        'lag_se': None,
        'lag_pval': None,
        'covid_coef': None,  # Absorbed by year FE
        'covid_se': None,
        'covid_pval': None,
        'r2': None,
        'r2_within': 0.3439,
        'n': 79,
        'entities': 41,
        'entity_fe': True,
        'year_fe': True
    },
    'Model 3': {
        'title': 'FE + Lagged Control',
        'subsidy_coef': -0.5114,
        'subsidy_se': 0.1169,
        'subsidy_pval': 0.0002,
        'lag_coef': 0.1264,
        'lag_se': 0.1156,
        'lag_pval': 0.2838,
        'covid_coef': None,  # Absorbed by year FE
        'covid_se': None,
        'covid_pval': None,
        'r2': None,
        'r2_within': 0.3730,
        'n': 46,
        'entities': None,  # Not reported for Model 3
        'entity_fe': True,
        'year_fe': True
    }
}

def format_coef(coef, se, pval):
    """Format coefficient with stars and standard error."""
    if coef is None:
        return '', ''

    # Determine significance stars
    if pval < 0.01:
        stars = '***'
    elif pval < 0.05:
        stars = '**'
    elif pval < 0.1:
        stars = '*'
    else:
        stars = ''

    # Format coefficient and SE
    coef_str = f"{coef:.4f}{stars}"
    se_str = f"({se:.4f})"

    return coef_str, se_str

# Generate LaTeX table
latex = r'''\begin{table}[htbp]
\centering
\caption{Subsidy Dependence and Financial Sustainability (PHFSI)}
\label{tab:subsidy_phfsi}
\begin{tabular}{lccc}
\toprule
'''

# Column headers
latex += r'& \textbf{(1)} & \textbf{(2)} & \textbf{(3)} \\' + '\n'
latex += r'& Pooled OLS & Fixed Effects & FE + Lag \\' + '\n'
latex += r'\midrule' + '\n'

# Subsidy dependence (current)
latex += r'Subsidy Dependence & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    coef_str, _ = format_coef(
        results[model]['subsidy_coef'],
        results[model]['subsidy_se'],
        results[model]['subsidy_pval']
    )
    latex += coef_str
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

# Standard errors
latex += r'& '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    _, se_str = format_coef(
        results[model]['subsidy_coef'],
        results[model]['subsidy_se'],
        results[model]['subsidy_pval']
    )
    latex += se_str
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

# Subsidy dependence (lag 1)
latex += r'Subsidy Dependence$_{t-1}$ & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['lag_coef'] is not None:
        coef_str, _ = format_coef(
            results[model]['lag_coef'],
            results[model]['lag_se'],
            results[model]['lag_pval']
        )
        latex += coef_str
    else:
        latex += ''
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

# Standard errors for lag
latex += r'& '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['lag_coef'] is not None:
        _, se_str = format_coef(
            results[model]['lag_coef'],
            results[model]['lag_se'],
            results[model]['lag_pval']
        )
        latex += se_str
    else:
        latex += ''
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

# COVID
latex += r'COVID (2020-2021) & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['covid_coef'] is not None:
        coef_str, _ = format_coef(
            results[model]['covid_coef'],
            results[model]['covid_se'],
            results[model]['covid_pval']
        )
        latex += coef_str
    else:
        latex += ''  # Absorbed by year FE
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

# Standard errors for COVID
latex += r'& '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['covid_coef'] is not None:
        _, se_str = format_coef(
            results[model]['covid_coef'],
            results[model]['covid_se'],
            results[model]['covid_pval']
        )
        latex += se_str
    else:
        latex += ''
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

latex += r'\midrule' + '\n'

# Fixed effects indicators
latex += r'Entity Fixed Effects & No & Yes & Yes \\' + '\n'
latex += r'Year Fixed Effects & No & Yes & Yes \\' + '\n'

latex += r'\midrule' + '\n'

# Model statistics
latex += r'$R^2$ & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['r2'] is not None:
        latex += f"{results[model]['r2']:.4f}"
    else:
        latex += ''
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

latex += r'$R^2$ (within) & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['r2_within'] is not None:
        latex += f"{results[model]['r2_within']:.4f}"
    else:
        latex += ''
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

latex += r'Observations & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    latex += str(results[model]['n'])
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

latex += r'Entities & '
for i, model in enumerate(['Model 1', 'Model 2', 'Model 3'], 1):
    if results[model]['entities'] is not None:
        latex += str(results[model]['entities'])
    else:
        latex += ''
    if i < 3:
        latex += ' & '
latex += r' \\' + '\n'

latex += r'\bottomrule' + '\n'
latex += r'\end{tabular}' + '\n'
latex += r'''\begin{tablenotes}
\footnotesize
\item \textit{Notes}: Dependent variable is PHFSI 4-component index (0-1 scale). Subsidy dependence is the ratio of operating deficit to operating revenue. Standard errors in parentheses. Models (2) and (3) use cluster-robust standard errors (clustered by entity). COVID variable absorbed by year fixed effects in models (2) and (3). *** p<0.01, ** p<0.05, * p<0.1.
\end{tablenotes}
\end{table}
'''

# Save table
output_path = OUTPUT_DIR / "tables" / "main" / "table5_subsidy_phfsi_regressions.tex"
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w') as f:
    f.write(latex)

print("="*80)
print("Regression Table Generated")
print("="*80)
print(f"Output: {output_path}")
print(f"\nPreview:")
print(latex)
