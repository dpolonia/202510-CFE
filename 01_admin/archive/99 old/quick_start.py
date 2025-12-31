#!/usr/bin/env python3
"""
SNS Data Collection - Quick Start Guide
========================================

Interactive guide for setting up and running the SNS data collection pipeline.
"""

import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")


def print_section(number, title):
    """Print section header"""
    print(f"\n{'─'*70}")
    print(f"  {number}. {title}")
    print(f"{'─'*70}\n")


def check_dependencies():
    """Check if required Python packages are installed"""
    print_section(1, "Checking Dependencies")
    
    required = ['requests', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies satisfied")
        return True


def show_data_overview():
    """Show overview of data to be collected"""
    print_section(2, "Data Collection Overview")
    
    print("""
📊 SNS Transparency Portal Datasets

Priority 1 - Essential Financial Data (4 datasets)
  • Total debt, overdue debt, late payments (Monthly, 2017-2024)
  • Economic-financial aggregates (Monthly, 2017-2024)
  • Average payment period to suppliers (Monthly, 2017-2024)
  • Comprehensive SNS accounts (Annual, 2017-2024)

Priority 2 - Operational & Staffing (4 datasets)
  • Headcount by professional group (Monthly, 2017-2024)
  • Headcount by employment type (Monthly, 2017-2024)
  • Absence days by reason (Monthly, 2017-2024)
  • Overtime costs percentage (Monthly, 2017-2024)

Priority 3 - Clinical Quality (4+ datasets)
  • Inpatient admissions and mortality (Quarterly, 2017-2024)
  • Mortality by age group (Quarterly, 2017-2024)
  • Stroke mortality rates (Annual, 2017-2024)
  • Hip fracture surgery timing (Monthly, 2017-2024)

Expected Download:
  • Total datasets: 12-15 core datasets
  • Expected size: 2-5 GB
  • Time required: 10-30 minutes (depends on connection)
  • Coverage: ~100-150 SNS institutions, 2017-2024
    """)


def run_downloads():
    """Run the download scripts"""
    print_section(3, "Download Options")
    
    print("""
Choose your download method:

1. Main Downloader (Recommended)
   - Uses API with pagination
   - Better error handling
   - Progress tracking
   - Resumable downloads
   
2. Simple Downloader (Backup)
   - Direct CSV exports
   - Faster but less flexible
   - Use if main downloader has API issues
   
3. Manual Download
   - Instructions only
   - Download from browser
    """)
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("\n🚀 Launching main downloader...")
        print("This will download Priority 1 datasets first, then ask about Priority 2 & 3.\n")
        try:
            subprocess.run([sys.executable, "sns_data_downloader.py"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("\n❌ Main downloader encountered errors")
            return False
        except FileNotFoundError:
            print("\n❌ sns_data_downloader.py not found in current directory")
            return False
    
    elif choice == "2":
        print("\n🚀 Launching simple downloader...")
        try:
            subprocess.run([sys.executable, "sns_data_downloader_simple.py"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("\n❌ Simple downloader encountered errors")
            return False
        except FileNotFoundError:
            print("\n❌ sns_data_downloader_simple.py not found in current directory")
            return False
    
    elif choice == "3":
        print("""
📥 Manual Download Instructions:

1. Visit: https://transparencia.sns.gov.pt
2. Search for each dataset by name (see DATA_SOURCE_MAPPING.md)
3. Click "Export" and select CSV format
4. Save to organized folders:
   - priority_1_essential/
   - priority_2_operational/
   - priority_3_quality/

Dataset names to search for:
  Priority 1:
    - "dívida total vencida pagamentos"
    - "agregados económico financeiros"
    - "tempo médio pagamento fornecedores"
    - "conta serviço nacional saúde"
  
  (See DATA_SOURCE_MAPPING.md for complete list)
        """)
        return False
    
    else:
        print("❌ Invalid choice")
        return False


def run_validation():
    """Run data validation"""
    print_section(4, "Data Validation")
    
    data_dirs = ["sns_data", "sns_data_simple"]
    found_dir = None
    
    for d in data_dirs:
        if Path(d).exists():
            found_dir = d
            break
    
    if not found_dir:
        print("❌ No data directory found. Download data first.")
        return False
    
    print(f"📂 Found data directory: {found_dir}")
    print("\nValidating downloaded datasets...")
    
    try:
        subprocess.run([sys.executable, "validate_sns_data.py", found_dir], check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n⚠️  Validation completed with warnings/errors")
        print(f"Check {found_dir}/validation_report.html for details")
        return False
    except FileNotFoundError:
        print("\n❌ validate_sns_data.py not found")
        return False


def show_next_steps():
    """Show next steps after data collection"""
    print_section(5, "Next Steps")
    
    print("""
✅ Data Collection Complete!

Now you can:

1. 📊 Data Analysis
   - Load datasets into Python/R
   - Merge on institution and date
   - Calculate PHFSI components
   - Run descriptive statistics

2. 📧 ACSS Data Request
   - Request cash flow statements
   - Request case mix index data
   - Request subsidy breakdown
   - See ACSS_request_letter_template.md

3. 📜 Manual Collection
   - Download TC audit reports
   - Search Diário da República for ULS dates
   - Collect INE demographic data
   - Review ACSS annual reports

4. 🔬 Research Execution
   - Construct panel dataset
   - Run DiD analysis (ULS reform)
   - Validate PHFSI vs Z-scores
   - Predict interventions

📚 Documentation:
   - README.md - Complete usage guide
   - DATA_SOURCE_MAPPING.md - All data sources
   - validation_report.html - Data quality check
   - download_report.html - Download summary

🎓 Research Proposals:
   - Gemini_-_00.md - Research framework
   - ChatGPT_-_00.md - Ten research ideas
   - Claude_-_00.md - Topic proposals

Happy researching! 🎉
    """)


def main():
    """Main quick start workflow"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     SNS DATA COLLECTION - QUICK START GUIDE                  ║
    ║                                                              ║
    ║     Portuguese NHS Financial Distress Research               ║
    ║     Advanced Corporate Finance Study                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("""
This guide will help you:
  ✓ Check dependencies
  ✓ Download SNS Portal datasets
  ✓ Validate data quality
  ✓ Understand next steps
    """)
    
    input("\nPress Enter to begin...")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install dependencies before continuing")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Show overview
    show_data_overview()
    proceed = input("\nProceed with download? (y/n): ")
    
    if proceed.lower() not in ['y', 'yes']:
        print("\n✋ Download cancelled")
        sys.exit(0)
    
    # Step 3: Run downloads
    download_success = run_downloads()
    
    if not download_success:
        print("\n⚠️  Download not completed through script")
        proceed_validation = input("\nValidate existing data anyway? (y/n): ")
        if proceed_validation.lower() not in ['y', 'yes']:
            sys.exit(1)
    
    # Step 4: Validate data
    print("\n" + "="*70)
    validate_choice = input("Validate downloaded data? (y/n): ")
    
    if validate_choice.lower() in ['y', 'yes']:
        run_validation()
    
    # Step 5: Next steps
    show_next_steps()
    
    print("\n✅ Quick start complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Interrupted by user")
        sys.exit(1)
