# Code Directory

All analysis code organized by workflow stage.

## Structure

### 01_data_collection/
Scripts to download and extract data from external sources
- Eurostat API
- INE (Portuguese Statistics)
- SNS Transparency Portal
- ACSS datasets

### 02_data_processing/
Data cleaning, merging, and preparation
- Clean individual datasets
- Merge across sources
- Create panel data structure
- Handle missing values and outliers

### 03_variable_construction/
Build analysis variables
- PHFSI components
- Governance indices
- Control variables
- Interaction terms

### 04_analysis/
Statistical analysis scripts
- Descriptive statistics
- Panel regressions
- Difference-in-differences
- Validation and prediction models

### 05_visualization/
Generate publication-quality figures
- Each script should produce one or more figures
- Output to `06_output/figures/`

### utils/
Helper functions and utilities
- Data utilities
- Analysis utilities
- Plotting utilities

## Guidelines

- Use clear, descriptive filenames
- Include docstrings for all functions
- Follow PEP 8 style guidelines
- Make code reproducible (set random seeds, document versions)
- Update requirements.txt when adding new dependencies
