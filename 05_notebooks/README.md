# Notebooks Directory

This directory contains Jupyter notebooks for exploratory analysis and interactive data exploration.

## Purpose

Use notebooks for:
- Initial data exploration
- Prototyping analyses
- Generating preliminary visualizations
- Testing code before moving to production scripts

## Guidelines

- Number notebooks in order of workflow (e.g., `01_`, `02_`, etc.)
- Include clear markdown documentation
- Once analysis is finalized, convert to production Python scripts in `04_code/`
- Commit notebooks with outputs cleared (use `jupyter nbconvert --clear-output`)

## Suggested Notebooks

1. `01_exploratory_data_analysis.ipynb` - Initial data exploration
2. `02_phfsi_development.ipynb` - Developing PHFSI components
3. `03_preliminary_results.ipynb` - Testing regression models
4. `04_visualization_prototypes.ipynb` - Creating draft figures
