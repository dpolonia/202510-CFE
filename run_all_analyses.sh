#!/bin/bash
# Master Replication Script
# Financial Sustainability in Soft Budget Constraint Environments
# Author: Daniel Polonia
# Date: January 2026
# Estimated Runtime: ~30 minutes

set -e  # Exit on any error

echo "================================================================================"
echo "REPLICATION: Portuguese SNS Financial Sustainability Analysis"
echo "================================================================================"
echo "Author: Daniel Polonia"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Working Directory: $(pwd)"
echo ""
echo "This script will:"
echo "  1. Construct all variables (~3 min)"
echo "  2. Run main analyses (~10 min)"
echo "  3. Generate tables (~2 min)"
echo "  4. Verify outputs"
echo ""
echo "Total estimated time: ~30 minutes"
echo "================================================================================"
echo ""

# Check if in correct directory
if [ ! -d "04_code" ] || [ ! -d "03_data" ]; then
    echo "ERROR: Must run from project root directory (202512-CFE/)"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "WARNING: Virtual environment not detected"
    echo "Attempting to activate venv..."
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "✓ Virtual environment activated"
    else
        echo "ERROR: venv/ not found. Please create virtual environment first:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
fi

# Check Python version
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"
if [[ $(echo "$python_version < 3.10" | bc -l) -eq 1 ]]; then
    echo "WARNING: Python 3.10+ recommended. Current: $python_version"
fi

# Check required packages
echo ""
echo "Checking dependencies..."
python -c "import pandas; import statsmodels; import linearmodels; print('✓ Core dependencies installed')" || {
    echo "ERROR: Missing dependencies. Install with: pip install -r requirements.txt"
    exit 1
}

echo ""
echo "================================================================================"
echo "STEP 1: Variable Construction"
echo "================================================================================"
echo ""

# 1.1 Construct PHFSI components
echo "[1/3] Constructing PHFSI components..."
python 04_code/03_variable_construction/construct_phfsi_components.py
if [ $? -eq 0 ]; then
    echo "✓ PHFSI components constructed"
else
    echo "✗ Error in PHFSI construction"
    exit 1
fi

# 1.2 Construct subsidy dependence
echo ""
echo "[2/3] Constructing subsidy dependence variable..."
python 04_code/03_variable_construction/construct_subsidy_dependence.py
if [ $? -eq 0 ]; then
    echo "✓ Subsidy dependence constructed"
else
    echo "✗ Error in subsidy construction"
    exit 1
fi

# 1.3 Integrate CQMI
echo ""
echo "[3/3] Integrating CQMI for 5-component PHFSI..."
python 04_code/03_variable_construction/integrate_cqmi_complete_phfsi.py
if [ $? -eq 0 ]; then
    echo "✓ CQMI integration complete"
else
    echo "✗ Error in CQMI integration"
    exit 1
fi

echo ""
echo "================================================================================"
echo "STEP 2: Main Analyses"
echo "================================================================================"
echo ""

# 2.1 Panel regressions (main result)
echo "[1/2] Running subsidy-PHFSI panel regressions..."
python 04_code/04_analysis/subsidy_phfsi_panel_regressions.py
if [ $? -eq 0 ]; then
    echo "✓ Panel regressions complete"
else
    echo "✗ Error in panel regressions"
    exit 1
fi

# 2.2 IV analysis (documents weak instruments)
echo ""
echo "[2/2] Running IV analysis (testing instruments)..."
python 04_code/04_analysis/subsidy_endogeneity_iv_analysis.py
if [ $? -eq 0 ]; then
    echo "✓ IV analysis complete (weak instruments documented)"
else
    echo "✗ Error in IV analysis"
    exit 1
fi

echo ""
echo "================================================================================"
echo "STEP 3: Generate Tables"
echo "================================================================================"
echo ""

# 3.1 Regression table
echo "[1/1] Generating regression tables..."
python 04_code/05_visualization/generate_regression_table.py
if [ $? -eq 0 ]; then
    echo "✓ Regression table generated"
else
    echo "✗ Error generating tables"
    exit 1
fi

echo ""
echo "================================================================================"
echo "STEP 4: Verification"
echo "================================================================================"
echo ""

# Check output files exist
echo "Verifying output files..."

expected_files=(
    "03_data/processed/variables/phfsi_components_complete.parquet"
    "03_data/processed/variables/subsidy_dependence_panel.parquet"
    "03_data/processed/panel/panel_with_instruments.parquet"
    "06_output/tables/main/table5_subsidy_phfsi_regressions.tex"
    "06_output/tables/appendix/tableA7_phfsi_4vs5_comparison.tex"
)

all_exist=true
for file in "${expected_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "  ✓ $file ($size)"
    else
        echo "  ✗ MISSING: $file"
        all_exist=false
    fi
done

echo ""

if [ "$all_exist" = true ]; then
    echo "================================================================================"
    echo "SUCCESS: All analyses completed successfully!"
    echo "================================================================================"
    echo ""
    echo "Output files:"
    echo "  - Data: 03_data/processed/"
    echo "  - Tables: 06_output/tables/"
    echo "  - Logs: 06_output/logs/"
    echo ""
    echo "Key Results (from panel regressions):"
    echo "  Model 1 (Pooled OLS):      β = -1.14***, R² = 0.54"
    echo "  Model 2 (Fixed Effects):   β = -0.50***, R² (within) = 0.34"
    echo "  Model 3 (FE + Lag):        β = -0.51***, R² (within) = 0.37"
    echo ""
    echo "Interpretation:"
    echo "  1 pp increase in subsidy dependence → 0.5-1.1 pp decrease in PHFSI"
    echo "  (Moral hazard hypothesis strongly supported)"
    echo ""
    echo "Next steps:"
    echo "  - Review tables: 06_output/tables/main/table5_subsidy_phfsi_regressions.tex"
    echo "  - Check logs for detailed output: 06_output/logs/"
    echo "  - See REPLICATION.md for interpretation guide"
    echo ""
    echo "================================================================================"
    exit 0
else
    echo "================================================================================"
    echo "PARTIAL SUCCESS: Some outputs missing"
    echo "================================================================================"
    echo ""
    echo "Please check:"
    echo "  1. Log files in 06_output/logs/ for errors"
    echo "  2. REPLICATION.md troubleshooting section"
    echo "  3. Contact author if issues persist"
    echo ""
    echo "================================================================================"
    exit 1
fi
