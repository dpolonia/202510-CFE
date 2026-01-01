# Data Availability Statement
## Financial Sustainability in Soft Budget Constraint Environments

**Project**: Corporate Finance in Public Healthcare
**Author**: Daniel Polonia
**Last Updated**: January 2026

---

## Summary

**All data used in this study are publicly available** from government transparency portals and official statistical agencies. No proprietary, restricted, or confidential data are used.

**Processed datasets** are included in this repository for replication purposes. Raw data can be independently downloaded from the sources listed below.

---

## Data Sources

### 1. SNS Transparency Portal (Primary Source)

**Provider**: Portuguese National Health Service (SNS) / Ministry of Health
**URL**: https://transparencia.sns.gov.pt
**Access**: Open data, no authentication required
**License**: Public domain (Portuguese government open data)

**Data Coverage**:
- **Time Period**: 2014-01-01 to 2025-06-30 (continuously updated)
- **Entities**: 95 public hospitals and health units
- **Update Frequency**: Monthly for financial data, quarterly for quality metrics
- **File Size**: ~542MB (raw data, multiple formats)

**Variables Used**:
| Dataset | Variables | Purpose |
|---------|-----------|---------|
| Financial Statements | Operating revenue, expenses, results | OSSR, subsidy dependence |
| Balance Sheet | Assets, liabilities, equity | TLR (leverage) |
| Cash Flow | Collections, payments | LRR (liquidity) |
| Payment Delays | Average payment days, overdue debt | SPI (stakeholder pressure) |
| Quality Metrics | Mortality rates, surgical timeliness | CQMI (quality maintenance) |

**Download Instructions**:
1. Navigate to https://transparencia.sns.gov.pt
2. Select "Dados Abertos" (Open Data)
3. Download datasets:
   - `agregados-economico-financeiros` (financial aggregates)
   - `divida-total-vencida-e-pagamentos` (payment delays)
   - `morbilidade-mortalidade-hospitalar` (mortality data)
   - `fraturas-anca-cirurgias-48h` (hip fracture quality)
4. Available formats: CSV, JSON, Parquet, XLSX

**Alternative Access**: SNS Data API (documentation at transparency portal)

**Data Quality Notes**:
- Some hospitals have missing data for certain periods (unbalanced panel)
- 2024 ULS reform created entity name changes (handled with crosswalk mapping)
- Quality data (CQMI) only available from 2019 onwards

---

### 2. Eurostat (Macroeconomic Controls)

**Provider**: European Statistical Office (European Commission)
**URL**: https://ec.europa.eu/eurostat
**Access**: Open data via web interface or API
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

**Data Coverage**:
- **Time Period**: 1975-2024 (historical national accounts)
- **Geographic Level**: National (Portugal) and NUTS2 regions
- **Update Frequency**: Annual for GDP, quarterly for some indicators
- **File Size**: ~17MB (regional GDP extracts)

**Variables Used**:
| Dataset Code | Variable | Purpose |
|--------------|----------|---------|
| nama_10_gdp | National GDP | Control variable |
| nama_10r_3gdp | Regional GDP (NUTS2) | Instrumental variable (attempted) |
| une_rt_a | Unemployment rate | Control variable |
| demo_r_pjangrp3 | Regional demographics | Control variable |

**Download Instructions**:
1. Navigate to https://ec.europa.eu/eurostat/data/database
2. Select theme: "Economy and finance" → "National accounts"
3. Filter by:
   - Country: Portugal
   - Time: 2014-2024
4. Download in CSV or XML format

**Alternative Access**: Eurostat API
```bash
# Example: Download GDP data
curl "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?geo=PT&format=JSON" > eurostat_gdp.json
```

**Preprocessing**: Raw Eurostat data converted to Parquet for performance
- Script: `04_code/02_data_processing/consolidate_macro_indicators.py`
- Output: `03_data/processed/eurostat/macro_indicators_consolidated.parquet`

---

### 3. Political Data (Instrumental Variables)

**Source**: Web research from publicly available sources
**Primary Sources**:
- Wikipedia: https://en.wikipedia.org/wiki/Minister_of_Health_(Portugal)
- Portuguese Government: https://www.portugal.gov.pt
- Legislative archives: https://www.parlamento.pt

**Access**: Public information, manually compiled
**License**: Public domain (factual information)

**Data Coverage**:
- **Time Period**: 2017-2024
- **Variables**: Minister name, political party, ideology (Left/Center/Right), tenure dates
- **File**: `/03_data/external/political/minister_health_portugal_2017_2024.csv` (included in repository)

**Ministers Documented**:
1. Adalberto Campos Fernandes (PS/Left, 2015-2018)
2. Marta Temido (Independent→PS, 2018-2022)
3. Manuel Pizarro (PS/Left, 2022-2024)
4. Ana Paula Martins (PSD/Right, 2024-present)

**Data Collection Method**:
- Web scraping from official government websites and Wikipedia
- Cross-validated against multiple sources
- Political party affiliation verified from official party records

**Reproducibility**: Source URLs documented in CSV file comments

---

## Processed Datasets (Included in Repository)

### Location: `/03_data/processed/`

All processed datasets are included in this repository and can be used directly for replication **without** downloading raw data.

### Key Files

| File | Size | Observations | Variables | Description |
|------|------|--------------|-----------|-------------|
| `variables/phfsi_components_complete.parquet` | ~200KB | 741 | 23 | Main PHFSI data with 5 components |
| `variables/subsidy_dependence_panel.parquet` | ~100KB | 557 | 15 | Subsidy analysis data |
| `panel/panel_with_instruments.parquet` | ~300KB | 741 | 39 | Complete merged panel for regressions |
| `crosswalks/hospital_to_uls_mapping_corrected.csv` | ~10KB | 95 | 3 | Hospital-ULS entity mapping |
| `external/political/minister_health_portugal_2017_2024.csv` | <1KB | 12 | 8 | Political instruments |

### File Formats

**Parquet**: Columnar storage format
- Advantages: Fast I/O, compression, type preservation
- Read with: `pandas.read_parquet()` (requires `pyarrow` package)

**CSV**: Comma-separated values
- Advantages: Human-readable, universal compatibility
- Read with: `pandas.read_csv()`

---

## Data Sharing and Reuse

### Researcher Access

**For replication**:
- All processed data included in this repository
- No data request or agreement required
- Clone repository and run analyses immediately

**For new research using these data**:
- Raw SNS data: Download directly from SNS Transparency Portal
- Eurostat data: Download from Eurostat website
- Processed data: Use from this repository (CC BY 4.0 license)

### Citation Requirements

**If using raw data**:
```
SNS Transparency Portal. (2025). Financial and operational data
for Portuguese public hospitals [Dataset]. Ministry of Health.
https://transparencia.sns.gov.pt
```

**If using processed data from this repository**:
```
Polonia, D. (2026). Portuguese SNS hospital financial sustainability
data [Dataset]. GitHub. https://github.com/[repo]/202512-CFE
```

**If using methodology or index**:
```
Polonia, D. (2026). Financial sustainability in soft budget
constraint environments: Evidence from Portuguese public hospitals
[Working Paper].
```

---

## Embargo and Restrictions

**None**.

All data are:
- ✅ Publicly available
- ✅ No embargo period
- ✅ No institutional access required
- ✅ No data use agreement needed
- ✅ No personal or sensitive information
- ✅ No proprietary data

---

## Long-Term Archiving

### Current Repository

**GitHub**: https://github.com/[your-repo]/202512-CFE
- Processed data included
- Version controlled
- Public access

### Planned Archiving (Upon Publication)

**Zenodo** (DOI assignment):
- Permanent archive of complete replication package
- Includes: data, code, documentation
- Citable with DOI
- Long-term preservation guarantee

**Format**:
```
Polonia, Daniel. (2026). Replication Package: Financial
Sustainability in Soft Budget Constraint Environments [Data set].
Zenodo. https://doi.org/10.5281/zenodo.[XXXXXX]
```

---

## Data Updates

### SNS Data

**Current Version**: Snapshot as of 2025-06-30
**Update Frequency**: SNS portal updated monthly

**To update analysis with new data**:
1. Download latest data from SNS portal
2. Re-run data processing scripts: `04_code/02_data_processing/`
3. Re-run variable construction: `04_code/03_variable_construction/`
4. Re-run analyses: `04_code/04_analysis/`

**Expected Changes**: Sample size will increase as new months are added

### Eurostat Data

**Current Version**: 2024 data (published 2025)
**Update Frequency**: Annual GDP data released ~6 months after year-end

**Note**: Historical data rarely revised, results stable

---

## Ethical Considerations

### Data Privacy

**No personal data** are used in this study:
- All data are at hospital/institution level (aggregated)
- No patient-level information
- No staff-level information
- No identifiable individuals

**IRB Approval**: Not required (public, aggregated data only)

### Data Sensitivity

**Financial data**: Public institutions' financial performance
- Already public via transparency portal
- No commercial sensitivity
- Public accountability purpose

**Quality data**: Hospital-level quality metrics
- Already public via SNS transparency
- No patient identifiers
- Public health monitoring purpose

---

## Third-Party Verification

### Independent Replication

**Encouraged**: Researchers are encouraged to:
1. Download raw data independently from SNS and Eurostat
2. Verify processed datasets match raw sources
3. Replicate all analyses from scratch
4. Report any discrepancies to author

### Data Integrity Checks

**Checksums** (for processed data):
```bash
# Verify data file integrity
md5sum 03_data/processed/variables/phfsi_components_complete.parquet
# Expected: [to be added]
```

**Verification Script** (planned):
```bash
bash scripts/verify_data_integrity.sh
```

---

## Contact for Data Questions

**General Data Availability**:
- SNS Portal: https://transparencia.sns.gov.pt/contact
- Eurostat: estat-user-support@ec.europa.eu

**This Project**:
- Author: Daniel Polonia
- Email: [your email]
- GitHub Issues: https://github.com/[repo]/202512-CFE/issues

**For data issues**:
- SNS data: Contact SNS transparency team
- Eurostat data: Contact Eurostat help desk
- Processed data: Open GitHub issue or email author

---

## Compliance with Journal Policies

### Data Availability Policies

**Compliant with**:
- Journal of Health Economics: Data availability statement required ✅
- Health Care Management Science: Open data preferred ✅
- AEA/AFA guidelines: Replication package required ✅

**Exceeds minimum requirements**:
- ✅ All raw data publicly available (not just processed)
- ✅ Complete replication package in repository
- ✅ Detailed documentation and scripts
- ✅ Expected runtime <1 hour

---

## Appendix: Data Download Log

### SNS Transparency Portal

**Last Accessed**: December 31, 2025
**Data Version**: Up to 2025-06-30
**Files Downloaded**:
- agregados-economico-financeiros.parquet (542MB)
- divida-total-vencida-e-pagamentos.parquet (85MB)
- morbilidade-mortalidade-hospitalar.parquet (112MB)
- fraturas-anca-cirurgias-48h.parquet (8MB)

**Total Raw Data Size**: ~750MB

### Eurostat

**Last Accessed**: December 15, 2025
**Data Version**: 2024 annual release
**Datasets Downloaded**:
- nama_10_gdp (Portugal GDP, 1975-2024)
- nama_10r_3gdp (Regional GDP NUTS2, 2000-2023)
- une_rt_a (Unemployment, 2010-2024)

**Total Size**: ~17MB

---

**Data Availability Statement Version**: 1.0
**Date**: January 1, 2026
**Complies With**: Journal of Health Economics data policy

