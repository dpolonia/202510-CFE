# Corporate Finance Research: Portuguese SNS Financial Sustainability

PhD research project applying corporate finance theory to analyze financial distress in Portugal's National Health Service (SNS).

## Project Overview

This project develops a novel framework for assessing financial sustainability in tax-funded healthcare systems, where traditional bankruptcy-based models fail. The research extends soft budget constraint theory to mission-critical public services and develops the **Public Hospital Financial Sustainability Index (PHFSI)**.

### Research Questions

1. How can corporate finance theory be adapted to measure, predict, and manage financial distress in public healthcare entities operating under soft budget constraints?
2. What alternative theoretical framework captures "transferred distress" to suppliers, taxpayers, and patients?
3. How do capital structure decisions in public hospitals differ from private firms?
4. What governance mechanisms predict financial sustainability in the absence of market discipline?

### Key Contributions

- **Theoretical**: Extension of soft budget constraint theory to healthcare, stakeholder-distributed financial distress framework
- **Empirical**: Development and validation of PHFSI, causal evidence from Portugal's ULS integration reform
- **Methodological**: Multi-method approach combining panel data, quasi-experimental design, and governance analysis
- **Practical**: Actionable policy recommendations for Portuguese Ministry of Health

## Directory Structure

```
202512-CFE/
├── 01_admin/              # Administrative documents and proposals
├── 02_literature/         # Bibliography and references
├── 03_data/              # All data files (raw, processed, external)
├── 04_code/              # Analysis code organized by workflow
├── 05_notebooks/         # Jupyter notebooks for exploration
├── 06_output/            # Figures, tables, and results
├── 07_writing/           # Manuscript and presentations
├── 08_documentation/     # Project documentation
├── venv/                 # Python virtual environment
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

See `REORGANIZATION_PLAN.md` for detailed directory structure and organization principles.

## Data Sources

- **SNS Transparency Portal**: Hospital financial statements, payment delays, operational metrics (2017-present)
- **Eurostat**: Regional demographics, economic indicators, health resources
- **INE**: Portuguese national statistics
- **ACSS**: Hospital budgets, performance contracts, audits
- **Ministry of Finance**: Capital injections, bailout data
- **Tribunal de Contas**: Financial audits, management assessments

See `08_documentation/data_sources.md` for complete documentation.

## Methodology

**Research Design**: Sequential Explanatory Mixed Methods

1. **PHFSI Development**: Five-component index measuring financial sustainability
2. **Panel Regression**: Fixed effects and dynamic panel models
3. **Quasi-Experimental**: Difference-in-differences using ULS integration reform
4. **Governance Analysis**: Survey and archival data on board composition

See `08_documentation/methodology_notes.md` for detailed methodology.

## Installation and Setup

### Prerequisites
- Python 3.12+
- Git
- Virtual environment support

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd 202512-CFE
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

## Usage

### Data Collection
```bash
# Extract Eurostat data
python 04_code/01_data_collection/eurostat_macro_extractor.py

# Additional data collection scripts in 04_code/01_data_collection/
```

### Data Processing
```bash
# Process and consolidate data
python 04_code/02_data_processing/consolidate_macro_indicators.py
```

### Analysis
```bash
# Run main analysis
python 04_code/04_analysis/run_analysis.py

# Generate figures
python 04_code/05_visualization/generate_all_figures.py
```

### Notebooks
```bash
# Launch Jupyter
jupyter notebook 05_notebooks/
```

## Project Timeline

- **Months 1-3**: Data collection and cleaning
- **Months 4-6**: Variable construction and PHFSI development
- **Months 7-9**: Preliminary analysis
- **Months 10-12**: Governance survey
- **Months 13-18**: Main analysis and robustness checks
- **Months 19-24**: Writing and submission

## Target Journals

1. **Journal of Health Economics** (primary target)
2. Strategic Management Journal
3. Management Science
4. Journal of Corporate Finance
5. Organization Science

See research proposal in `01_admin/proposal/` for publication strategy.

## Key Files

- `01_admin/proposal/research_proposal.md` - Full research proposal
- `REORGANIZATION_PLAN.md` - Directory structure documentation
- `08_documentation/methodology_notes.md` - Methodology details
- `08_documentation/data_sources.md` - Data documentation
- `requirements.txt` - Python package dependencies

## Contributing

This is a PhD research project. For questions or collaboration inquiries, please contact the author.

## License

Academic research project. Data sources have their own licenses - see individual data provider terms.

## Acknowledgments

- SNS Transparency Portal for open data access
- Eurostat and INE for statistical data
- PhD supervisors and collaborators

## Contact

Daniel Polonia
PhD Candidate, Corporate Finance
[Contact information]

## Last Updated

2025-12-31 - Major directory reorganization completed

---

**Note**: This project follows reproducible research best practices. All analysis code is version controlled, data sources are documented, and outputs are traceable to source code.
