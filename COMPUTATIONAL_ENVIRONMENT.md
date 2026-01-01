# Computational Environment
## Financial Sustainability in Soft Budget Constraint Environments

**Project**: Corporate Finance in Public Healthcare
**Author**: Daniel Polonia
**Last Updated**: January 1, 2026

---

## System Information

### Operating System

```
OS: Ubuntu 22.04.5 LTS
Kernel: Linux 6.6.87.2-microsoft-standard-WSL2
Platform: Windows Subsystem for Linux 2 (WSL2) on Windows 11
Architecture: x86_64
```

### Hardware

```
CPU: Intel/AMD x86_64 (4+ cores recommended)
RAM: 8GB minimum (16GB recommended for full dataset)
Disk: ~2GB free space required
```

---

## Python Environment

### Python Version

```
Python 3.13.1 (main, Dec  19 2024, 10:45:43) [GCC 11.4.0]
```

**Compatibility**: Tested on Python 3.13.1, compatible with Python 3.10+

---

## Package Versions

### Core Data Science (REQUIRED)

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.3.3 | Data manipulation |
| numpy | 2.3.5 | Numerical computing |
| scipy | 1.16.0 | Statistical functions |
| pyarrow | 22.0.0 | Parquet file I/O |

### Statistical Analysis (REQUIRED)

| Package | Version | Purpose |
|---------|---------|---------|
| statsmodels | 0.14.4 | OLS, statistical tests |
| linearmodels | 7.0 | Panel regression, IV/2SLS |

### Visualization (REQUIRED)

| Package | Version | Purpose |
|---------|---------|---------|
| matplotlib | 3.10.0 | Plotting |
| seaborn | 0.13.2 | Statistical visualization |

### Web/Data Collection

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.32.3 | HTTP requests |
| beautifulsoup4 | 4.12.3 | HTML parsing |
| lxml | 5.3.0 | XML/HTML processing |

### Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| openpyxl | 3.1.5 | Excel support |
| jupyter | 1.1.1 | Notebooks (optional) |
| tqdm | 4.67.1 | Progress bars |

---

## Installation Instructions

### Option 1: Using requirements.txt (Recommended)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install from requirements.txt
pip install -r requirements.txt
```

This installs compatible versions (`>=` constraints), ensuring forward compatibility.

### Option 2: Exact Version Replication

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install exact versions
pip install pandas==2.3.3 numpy==2.3.5 scipy==1.16.0
pip install statsmodels==0.14.4 linearmodels==7.0
pip install matplotlib==3.10.0 seaborn==0.13.2
pip install pyarrow==22.0.0 openpyxl==3.1.5
pip install requests==2.32.3 beautifulsoup4==4.12.3
```

### Verification

```bash
# Verify installation
python -c "
import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt

print('✓ All core packages imported successfully')
print(f'pandas: {pd.__version__}')
print(f'numpy: {np.__version__}')
print(f'statsmodels: {sm.__version__}')
"
```

---

## Package Dependencies

### Dependency Tree

```
linearmodels (7.0)
├── statsmodels (>=0.11)
├── pandas (>=1.1)
├── numpy (>=1.17)
└── scipy (>=1.2)

statsmodels (0.14.4)
├── pandas (>=1.0)
├── numpy (>=1.18)
└── scipy (>=1.3)

matplotlib (3.10.0)
├── numpy (>=1.21)
└── pillow (>=8)

seaborn (0.13.2)
├── matplotlib (>=3.4)
├── pandas (>=1.2)
└── numpy (>=1.20)
```

**Note**: `pip` automatically resolves dependencies. Installing `linearmodels` will install compatible versions of all required packages.

---

## Execution Environment

### Runtime Performance

**Measured on**:
- OS: Ubuntu 22.04 (WSL2)
- CPU: 4-core x86_64
- RAM: 16GB
- Storage: NVMe SSD

| Script | Runtime | Peak Memory |
|--------|---------|-------------|
| `construct_phfsi_components.py` | ~45 sec | ~500MB |
| `construct_subsidy_dependence.py` | ~30 sec | ~300MB |
| `integrate_cqmi_complete_phfsi.py` | ~90 sec | ~800MB |
| `subsidy_phfsi_panel_regressions.py` | ~8 sec | ~200MB |
| `subsidy_endogeneity_iv_analysis.py` | ~5 sec | ~150MB |
| `generate_regression_table.py` | ~1 sec | ~50MB |
| **Total** | **~3 min** | **~1GB** |

**Full replication** (including data loading, I/O): ~30 minutes

---

## Known Platform-Specific Issues

### Windows (Native, not WSL)

**Issue**: Path separator differences (`\` vs `/`)

**Solution**: Scripts use `pathlib.Path()`, which handles this automatically. If errors persist:
```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
```

**Alternative**: Use WSL2 for full Linux compatibility

### macOS

**Issue**: Some packages may require XCode Command Line Tools

**Solution**:
```bash
xcode-select --install
```

**Issue**: ARM architecture (M1/M2) may require Rosetta

**Solution**: Most packages now have native ARM builds. If issues:
```bash
# Install Rosetta (one-time)
softwareupdate --install-rosetta

# OR use x86_64 Python via Rosetta
arch -x86_64 python3 -m venv venv
```

### Linux

**Issue**: Missing system libraries for `pyarrow`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install libarrow-dev

# RHEL/CentOS
sudo yum install arrow-devel
```

---

## Reproducibility Notes

### Random Seeds

Scripts **do not** use random number generation for main results. All analyses are deterministic.

**Exception**: Bootstrapping (if implemented) would require:
```python
np.random.seed(42)
```

### Floating Point Precision

Results may vary slightly across platforms due to floating-point arithmetic differences. Expected variation:
- Coefficients: ±1e-6 (6 decimal places)
- p-values: ±1e-8

**Critical results** (subsidy coefficient = -0.50 to -1.14) are robust to precision differences.

### File System Case Sensitivity

Scripts assume **case-sensitive** file system (Linux/macOS default).

**Windows users**: Ensure consistent file naming:
- Correct: `phfsi_components_complete.parquet`
- Incorrect: `PHFSI_Components_Complete.parquet`

---

## Alternative Environments

### Docker (Future)

For perfect reproducibility, a Dockerfile could be provided:

```dockerfile
FROM python:3.13.1-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY 03_data/ ./03_data/
COPY 04_code/ ./04_code/

CMD ["bash", "run_all_analyses.sh"]
```

**Status**: Not yet implemented (manual environment sufficient for current version)

### Conda

Alternative to `pip`:

```bash
conda create -n phfsi python=3.13
conda activate phfsi
conda install pandas numpy scipy statsmodels matplotlib seaborn pyarrow
pip install linearmodels  # Not available via conda
```

---

## Package Update Policy

### Versioning Philosophy

- **`>=` constraints**: Forward compatibility (recommended for users)
- **Exact versions**: This documentation (for perfect replication)

### Tested Compatibility

| Package | Tested Version | Compatible Range |
|---------|----------------|------------------|
| pandas | 2.3.3 | 2.0.0 - 2.x.x |
| numpy | 2.3.5 | 1.24.0 - 2.x.x |
| statsmodels | 0.14.4 | 0.14.0 - 0.15.x |
| linearmodels | 7.0 | 5.0 - 7.x |

### Breaking Changes to Watch

1. **pandas 2.0**: Major API changes from 1.x
   - Scripts written for pandas ≥2.0
   - May not work with pandas <2.0

2. **numpy 2.0**: Some dtype changes
   - Scripts compatible with both numpy 1.x and 2.x
   - No breaking changes expected

3. **linearmodels**: API stable since 5.0
   - Panel regression syntax unchanged

---

## Verification Commands

### Check Python Version

```bash
python --version
# Expected: Python 3.10.x or higher
```

### Check Package Versions

```bash
pip list | grep -E "(pandas|numpy|statsmodels|linearmodels)"
# Expected output:
# linearmodels       7.0
# numpy              2.3.5
# pandas             2.3.3
# statsmodels        0.14.4
```

### Generate Frozen Requirements

To create exact environment snapshot:

```bash
pip freeze > requirements_frozen_$(date +%Y%m%d).txt
```

This captures all packages with exact versions, including sub-dependencies.

---

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'linearmodels'`

**Solution**:
```bash
source venv/bin/activate  # Ensure venv active
pip install linearmodels
```

### Version Conflicts

**Problem**: `pip` reports version conflicts

**Solution 1** (Clean install):
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 2** (Explicit version):
```bash
pip install --force-reinstall linearmodels==7.0
```

### Performance Issues

**Problem**: Scripts run very slowly

**Solution**:
- Close other applications (free RAM)
- Use SSD instead of HDD
- Upgrade to Python 3.13 (performance improvements)

---

## License Compatibility

All packages used are open-source with permissive licenses:

| Package | License |
|---------|---------|
| pandas | BSD 3-Clause |
| numpy | BSD 3-Clause |
| scipy | BSD 3-Clause |
| statsmodels | BSD 3-Clause |
| linearmodels | NCSA License |
| matplotlib | PSF License |
| seaborn | BSD 3-Clause |

**No conflicts** with academic research or commercial use.

---

## Contact

For environment-specific issues:
- **General**: See `REPLICATION.md` troubleshooting section
- **Package bugs**: Report to respective package maintainers
- **This project**: daniel.polonia@[institution].edu

---

**Last Updated**: January 1, 2026

**Environment Captured**: Python 3.13.1, Ubuntu 22.04 LTS (WSL2)

