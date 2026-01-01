# Replication Guide
## Financial Sustainability in Soft Budget Constraint Environments: Evidence from Portuguese Public Hospitals

**Author**: Daniel Polonia
**Date**: January 2026
**Estimated Time**: 30 minutes (on standard laptop with 8GB RAM)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Data Access](#data-access)
4. [Step-by-Step Replication](#step-by-step-replication)
5. [Expected Outputs](#expected-outputs)
6. [Troubleshooting](#troubleshooting)
7. [Verification](#verification)

---

## Prerequisites

### System Requirements

**Hardware**:
- CPU: 2+ cores (4+ recommended)
- RAM: 8GB minimum (16GB recommended)
- Disk: ~2GB free space

**Software**:
- Operating System: Linux, macOS, or WSL2 (Windows Subsystem for Linux)
  - Tested on: Ubuntu 22.04 LTS (WSL2)
- Python: 3.10 or higher
  - Tested on: Python 3.13.1
- Git: For cloning repository

**Tested Environment**:
```
OS: Ubuntu 22.04 LTS (WSL2 on Windows 11)
Python: 3.13.1
Kernel: Linux 6.6.87.2-microsoft-standard-WSL2
Date: January 2026
```

---

## Installation

### Step 1: Clone Repository

```bash
# Clone from GitHub (or download ZIP)
git clone https://github.com/[your-repo]/202512-CFE.git
cd 202512-CFE

# Verify directory structure
ls -la
# You should see: 01_admin/ 02_literature/ 03_data/ 04_code/ etc.
```

### Step 2: Create Virtual Environment

```bash
# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Verify activation (should show venv path)
which python
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This will install:
# - pandas, numpy, scipy (data processing)
# - statsmodels, linearmodels (statistical analysis)
# - matplotlib, seaborn (visualization)
# - pyarrow (Parquet file support)
# - And other dependencies

# Verify installation
python -c "import pandas; import linearmodels; print('✓ Dependencies installed')"
```

**Expected Time**: 2-5 minutes

---

## Data Access

### Data are Already Included

**Good news**: All processed data files are included in this repository under `/03_data/processed/`. You do NOT need to download raw data from SNS or Eurostat to replicate the main results.

**Directory**: `/03_data/processed/`
- `variables/phfsi_components_complete.parquet` - Main PHFSI data (741 obs)
- `variables/subsidy_dependence_panel.parquet` - Subsidy analysis data (557 obs)
- `panel/panel_with_instruments.parquet` - Complete merged panel (741 obs, 39 vars)
- `crosswalks/hospital_to_uls_mapping_corrected.csv` - Entity mapping

**If you want to start from raw data** (optional):
- SNS data: Download from https://transparencia.sns.gov.pt
- Eurostat data: Download via https://ec.europa.eu/eurostat
- See `08_documentation/data_sources.md` for detailed instructions

---

## Step-by-Step Replication

### Full Replication (All Analyses)

**Option A: Run Master Script** (recommended)

```bash
# From project root
bash run_all_analyses.sh

# This runs all scripts in order (~30 minutes)
```

**Option B: Run Individual Scripts** (for debugging)

Follow the steps below:

---

### Step 1: Variable Construction (~3 minutes)

#### 1.1 Construct PHFSI Components

```bash
python 04_code/03_variable_construction/construct_phfsi_components.py
```

**What it does**:
- Loads SNS financial data
- Calculates 5 PHFSI components (OSSR, SPI, LRR, TLR, CQMI)
- Normalizes components to [0,1] scale
- Computes equal-weighted composite index

**Output**:
- `/03_data/processed/variables/phfsi_components.parquet`
- Log: `/06_output/logs/phfsi_components.log`

**Expected**: ✓ PHFSI calculated for 741 observations

---

#### 1.2 Construct Subsidy Dependence Variable

```bash
python 04_code/03_variable_construction/construct_subsidy_dependence.py
```

**What it does**:
- Calculates subsidy dependence from operating deficits
- Creates lagged variables (1, 3, 4 years)
- Constructs historical subsidy instrument
- Aggregates to hospital-year level

**Output**:
- `/03_data/processed/variables/subsidy_dependence_panel.parquet`
- `/06_output/results/descriptive/subsidy_dependence_summary.csv`
- Log: `/06_output/logs/subsidy_dependence.log`

**Expected**: ✓ 557 hospital-year observations created

---

#### 1.3 Integrate CQMI for 5-Component PHFSI

```bash
python 04_code/03_variable_construction/integrate_cqmi_complete_phfsi.py
```

**What it does**:
- Loads CQMI (quality) component
- Matches entity names (handles 2024 ULS reform)
- Creates complete 5-component PHFSI
- Validates against 4-component version

**Output**:
- `/03_data/processed/variables/phfsi_components_complete.parquet`
- `/03_data/processed/variables/phfsi_5comp_complete_observations.parquet`
- Log: `/06_output/logs/cqmi_integration.log`

**Expected**: ✓ 25 observations with all 5 components (r=0.92 correlation with 4-comp)

---

### Step 2: Main Analyses (~10 minutes)

#### 2.1 Subsidy-PHFSI Panel Regressions (Main Result)

```bash
python 04_code/04_analysis/subsidy_phfsi_panel_regressions.py
```

**What it does**:
- Runs 3 regression specifications:
  1. Pooled OLS
  2. Fixed Effects (Entity + Year)
  3. Fixed Effects + Lagged Subsidy Control
- Tests H1: Subsidy Dependence → Lower PHFSI

**Output**:
- Log: `/06_output/logs/panel_regressions.log`

**Expected Results**:
```
Model 1 (Pooled OLS):  β = -1.14***, R² = 0.54
Model 2 (Fixed Effects): β = -0.50***, R² (within) = 0.34
Model 3 (FE + Lag):     β = -0.51***, R² (within) = 0.37
```

---

#### 2.2 IV Analysis (Documents Weak Instruments)

```bash
python 04_code/04_analysis/subsidy_endogeneity_iv_analysis.py
```

**What it does**:
- Loads political instruments (minister ideology)
- Tests instrument relevance (first-stage F-test)
- Documents why IV approach failed

**Output**:
- `/03_data/processed/panel/panel_with_instruments.parquet`
- Log: `/06_output/logs/iv_analysis.log`

**Expected**:
```
First-Stage F-statistic: 2.26 (< 10, weak instruments)
Political instrument: p=0.845 (NOT significant)
Historical subsidy: p=0.041 (significant but insufficient alone)
```

**Conclusion**: IV approach not feasible → OLS + FE is preferred

---

### Step 3: Generate Tables (~2 minutes)

#### 3.1 Main Regression Table

```bash
python 04_code/05_visualization/generate_regression_table.py
```

**Output**:
- `/06_output/tables/main/table5_subsidy_phfsi_regressions.tex`

**Table**: 3-column regression table (Pooled OLS, FE, FE+Lag)

---

#### 3.2 Robustness Tables (Already Generated)

**Table A7**: 4-comp vs 5-comp PHFSI comparison
- Location: `/06_output/tables/appendix/tableA7_phfsi_4vs5_comparison.tex`
- Generated by: `integrate_cqmi_complete_phfsi.py` (Step 1.3)

---

### Step 4: Verification

#### 4.1 Check Key Results Match Paper

```bash
# Verify subsidy-PHFSI coefficient
python -c "
import pandas as pd
df = pd.read_parquet('03_data/processed/panel/panel_with_instruments.parquet')
print(f'Sample size: {len(df)}')
print(f'Complete for regression: {df[\"has_phfsi\"].sum()} / {len(df)}')
"
```

**Expected**:
```
Sample size: 741
Complete for regression: 79 / 741
```

---

#### 4.2 Verify Output Files Exist

```bash
# Check main outputs
ls -lh 06_output/tables/main/table5_subsidy_phfsi_regressions.tex
ls -lh 06_output/tables/appendix/tableA7_phfsi_4vs5_comparison.tex
ls -lh 03_data/processed/variables/phfsi_components_complete.parquet

# All should exist
```

---

## Expected Outputs

### Data Files (Processed)

| File | Size | Observations | Description |
|------|------|--------------|-------------|
| `phfsi_components_complete.parquet` | ~200KB | 741 | Main PHFSI data |
| `subsidy_dependence_panel.parquet` | ~100KB | 557 | Subsidy analysis |
| `panel_with_instruments.parquet` | ~300KB | 741 | Merged panel |

### Tables (LaTeX)

| File | Description |
|------|-------------|
| `table5_subsidy_phfsi_regressions.tex` | Main regression results (3 models) |
| `tableA7_phfsi_4vs5_comparison.tex` | Robustness: 4-comp vs 5-comp validation |

### Logs

| File | Description |
|------|-------------|
| `phfsi_components.log` | PHFSI construction log |
| `subsidy_dependence.log` | Subsidy variable construction |
| `cqmi_integration.log` | 5-component integration |
| `panel_regressions.log` | **Main results** (regression output) |
| `iv_analysis.log` | IV analysis (weak instruments documented) |

---

## Troubleshooting

### Common Errors

#### Error: `ModuleNotFoundError: No module named 'linearmodels'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### Error: `FileNotFoundError: [Errno 2] No such file or directory`

**Solution**:
```bash
# Ensure you're running from project root
pwd  # Should show: /path/to/202512-CFE

# If not, navigate to project root:
cd /path/to/202512-CFE

# Then run scripts
python 04_code/04_analysis/subsidy_phfsi_panel_regressions.py
```

---

#### Error: `MemoryError` or system freeze

**Solution**:
- Close other applications to free RAM
- Or reduce sample size in scripts (modify code):
  ```python
  # In analysis scripts, add this after loading data:
  df = df.sample(frac=0.5, random_state=42)  # Use 50% of data
  ```

---

#### Error: Regression results don't match paper

**Check**:
1. Correct Python version (3.10+)?
2. Correct package versions? Run: `pip freeze > installed_packages.txt`
3. Correct data files loaded?
4. Random seed set (if applicable)?

**If still not matching**:
- Contact author: [your email]
- Open GitHub issue with details

---

### Platform-Specific Issues

#### Windows (Native, not WSL)

**Issue**: Path separator differences
**Solution**: Scripts use `Path()` from `pathlib`, which handles this automatically. If errors persist, use WSL2 instead.

#### macOS

**Issue**: Some packages may require XCode Command Line Tools
**Solution**:
```bash
xcode-select --install
```

---

## Verification Checklist

Use this checklist to verify successful replication:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list` shows pandas, linearmodels, etc.)
- [ ] All 3 variable construction scripts run without errors
- [ ] Panel regression log shows:
  - Model 1: β ≈ -1.14, p < 0.001
  - Model 2: β ≈ -0.50, p < 0.001
  - Model 3: β ≈ -0.51, p < 0.001
- [ ] IV analysis log shows F-statistic ≈ 2.26 (weak instruments)
- [ ] Table 5 (LaTeX) generated and formatted correctly
- [ ] Table A7 (LaTeX) shows r ≈ 0.92 between 4-comp and 5-comp PHFSI

**If all checks pass**: ✓ Replication successful!

---

## Advanced: Replication from Raw Data

**Note**: This is NOT required for replicating the main results. Only attempt if you want to verify data processing from scratch.

### Step 1: Download Raw SNS Data

```bash
# Use SNS API (if available) or manual download
# See: 04_code/01_data_collection/README.md
```

### Step 2: Run Data Processing

```bash
python 04_code/02_data_processing/process_sns_financial.py
python 04_code/02_data_processing/consolidate_macro_indicators.py
```

**Warning**: This may take 1-2 hours and requires ~1GB additional disk space.

---

## Citation

If replicating this work for your research, please cite:

```bibtex
@unpublished{polonia2026financial,
  author = {Polonia, Daniel},
  title = {Financial Sustainability in Soft Budget Constraint Environments:
           Evidence from Portuguese Public Hospitals},
  year = {2026},
  note = {Working Paper}
}
```

---

## Getting Help

**Issues with replication**:
1. Check this guide's Troubleshooting section
2. Review logs in `/06_output/logs/`
3. Open GitHub issue: https://github.com/[your-repo]/202512-CFE/issues
4. Email author: [your email]

**Include in help request**:
- Error message (full traceback)
- Log file contents
- System info: `python --version`, `uname -a`
- Output of: `pip freeze`

---

## Last Updated

January 1, 2026

---

**End of Replication Guide**

For questions about methodology or interpretation, see the main paper and issue completion reports in the repository root.
