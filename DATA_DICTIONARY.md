# Data Dictionary
## Financial Sustainability in Soft Budget Constraint Environments

**Project**: Corporate Finance in Public Healthcare
**Author**: Daniel Polonia
**Last Updated**: January 2026

---

## Table of Contents

1. [Key Constructed Variables](#key-constructed-variables)
2. [PHFSI Components](#phfsi-components)
3. [Financial Variables](#financial-variables)
4. [Instrumental Variables](#instrumental-variables)
5. [Control Variables](#control-variables)
6. [Panel Structure Variables](#panel-structure-variables)
7. [Data Sources Reference](#data-sources-reference)

---

## Key Constructed Variables

### PHFSI (Public Hospital Financial Sustainability Index)

**Variable Name**: `phfsi_4comp`, `phfsi_5comp`

**Definition**: Composite index measuring financial sustainability in soft budget constraint environments

**Scale**: 0 to 1 (higher = better sustainability)

**Construction**:
- **4-component**: Equal-weighted average of OSSR, SPI (reversed), LRR, TLR (reversed)
- **5-component**: Equal-weighted average of OSSR, SPI (reversed), LRR, TLR (reversed), CQMI

**Formula**:
```
PHFSI_4comp = (OSSR + (1-SPI) + LRR + (1-TLR)) / 4
PHFSI_5comp = (OSSR + (1-SPI) + LRR + (1-TLR) + CQMI) / 5
```

**Coverage**:
- 4-component: 79/741 observations (10.7%)
- 5-component: 25/741 observations (3.4%, 2024 only)

**Source File**: `phfsi_components_complete.parquet`

**Validation**: Predicts 2024 government intervention (AUC = TBD)

---

### Subsidy Dependence

**Variable Name**: `subsidy_dependence`

**Definition**: Proportion of operating revenue that must be covered by government subsidies

**Scale**: 0 to infinity (typically 0 to 0.50 in data)

**Formula**:
```
subsidy_dependence = |min(0, operating_results)| / operating_revenue
```

**Interpretation**:
- 0 = Hospital is self-sufficient (no subsidy needed)
- 0.10 = Hospital requires subsidies equal to 10% of revenue to break even
- 0.50 = Hospital requires subsidies equal to 50% of revenue

**Mean**: 0.136 (13.6%)
**SD**: Varies by year (0.05 to 0.15)

**Source File**: `subsidy_dependence_panel.parquet`

**Calculation Script**: `construct_subsidy_dependence.py`

---

## PHFSI Components

### 1. OSSR (Operational Self-Sufficiency Ratio)

**Variable Names**: `ossr`, `ossr_raw`

**Definition**: Ability to cover operating expenses without government subsidies

**Formula**:
```
OSSR = operating_revenue_excl_subsidies / operating_expenses
```

**Scale**:
- **Raw** (`ossr_raw`): 0 to infinity (unbounded)
- **Normalized** (`ossr`): 0 to 1 (capped at 1.0)

**Interpretation**:
- OSSR = 1.0: Fully self-sufficient
- OSSR = 0.80: Can cover 80% of expenses without subsidies
- OSSR > 1.0: Operating surplus (rare in public hospitals)

**Coverage**: 373/741 observations (50.3%)

**Source**: SNS Transparency Portal - Financial Statements
- `rendimentos_operacionais` (operating revenue)
- `gastos_operacionais` (operating expenses)

**Notes**: Subsidies are backed out of operating revenue using operating results

---

### 2. SPI (Stakeholder Pressure Index)

**Variable Names**: `spi`, `spi_payment_delay`, `spi_overdue_ratio`

**Definition**: Composite measure of pressure from suppliers and creditors

**Formula**:
```
SPI = (payment_delay / 90) + (overdue_liabilities / total_liabilities)
```

**Components**:
- **Payment Delay** (`spi_payment_delay`): Average days to pay suppliers ÷ 90 days
- **Overdue Ratio** (`spi_overdue_ratio`): Overdue liabilities ÷ Total liabilities

**Scale**: 0 to ~2 (higher = worse pressure)

**Interpretation**:
- SPI = 0: No payment delays, no overdue debt
- SPI = 1.0: 90-day payment delays or 100% overdue
- SPI = 2.0: Both severe delays AND high overdue ratio

**Coverage**:
- Full SPI: 141/741 observations (19.0%)
- Payment delay only: 434/741 (58.6%)
- Overdue ratio only: 438/741 (59.1%)

**Source**: SNS Transparency Portal
- `prazo_medio_pagamento` (average payment days)
- `divida_vencida` (overdue debt)
- `divida_total` (total liabilities)

**In PHFSI**: Used as (1 - SPI) to reverse direction

---

### 3. LRR (Liquidity Realization Rate)

**Variable Names**: `lrr`, `lrr_raw`

**Definition**: Ability to convert receivables to cash

**Formula**:
```
LRR = cash_collections_t / accrued_revenue_t-1
```

**Scale**:
- **Raw** (`lrr_raw`): 0 to infinity
- **Normalized** (`lrr`): 0 to 1 (capped at 1.0)

**Interpretation**:
- LRR = 1.0: Full collection of last year's receivables
- LRR = 0.80: Collected 80% of last year's receivables
- LRR > 1.0: Collected more than last year's receivables (clearing backlog)

**Coverage**: 373/741 observations (50.3%)

**Source**: SNS Transparency Portal - Cash Flow Statements
- Cash collections (current year)
- Accrued revenue (lagged 1 year)

**Notes**: First year (2017) has missing LRR due to lag requirement

---

### 4. TLR (True Leverage Ratio)

**Variable Names**: `tlr`, `tlr_raw`, `tlr_capped`

**Definition**: Total leverage including implicit government guarantees (expected subsidies)

**Formula**:
```
TLR = (liabilities + NPV_expected_subsidies) / operating_retained_earnings
```

**Scale**:
- **Raw** (`tlr_raw`): 0 to infinity
- **Capped** (`tlr_capped`): 0 to 5 (outlier cap)
- **Normalized** (`tlr`): 0 to 1 (reverse-scaled for PHFSI)

**Interpretation**:
- TLR = 1.0: Liabilities equal equity
- TLR = 2.0: Liabilities twice equity (leverage ratio 2:1)
- TLR > 5.0: Extreme leverage (financial distress)

**Simplification**: NPV expected subsidies approximated as 3-year average of past subsidies

**Coverage**: 79/741 observations (10.7%)

**Source**: SNS Transparency Portal - Balance Sheet
- Total liabilities
- Equity
- Operating subsidies (3-year average)

**In PHFSI**: Used as (1 - TLR_normalized) to reverse direction

---

### 5. CQMI (Clinical Quality Maintenance Index)

**Variable Names**: `cqmi`, `cqmi_mortality`, `cqmi_hip_fracture`

**Definition**: Whether clinical quality is maintained under financial stress

**Formula**:
```
CQMI = (normalized_mortality_index + hip_fracture_timeliness) / 2
```

**Components**:
- **Mortality** (`cqmi_mortality`): Standardized mortality ratio (lower = better)
- **Hip Fracture** (`cqmi_hip_fracture`): % surgeries within 48h (higher = better)

**Scale**: 0 to 1 (higher = better quality maintenance)

**Interpretation**:
- CQMI = 1.0: Best-in-class quality
- CQMI = 0.50: Average quality
- CQMI = 0: Worst-in-class quality

**Coverage**:
- Full CQMI: 107/741 observations (14.4%)
- Mortality only: 107/741 (14.4%, 2019-2024)
- Hip fracture only: 150/741 (20.2%)

**Source**: SNS Transparency Portal - Quality Metrics
- `morbilidade_mortalidade` (mortality data)
- `fraturas_anca_48h` (hip fracture timeliness)

**Notes**: Only available 2019-2024 due to data collection period

---

## Financial Variables

### Operating Revenue

**Variable Name**: `rendimentos_operacionais`

**Definition**: Total operating revenue from hospital operations

**Units**: Euros (€)

**Source**: SNS - Financial Statements

**Typical Range**: €100,000 to €500,000,000 (varies by hospital size)

---

### Operating Expenses

**Variable Name**: `gastos_operacionais`

**Definition**: Total operating expenses

**Units**: Euros (€)

**Components**: Staff salaries, supplies, utilities, etc.

**Source**: SNS - Financial Statements

---

### Operating Results

**Variable Name**: `resultados_operacionais`

**Definition**: Operating revenue minus operating expenses

**Units**: Euros (€)

**Formula**: `rendimentos_operacionais - gastos_operacionais`

**Sign Convention**:
- Positive: Operating surplus
- Negative: Operating deficit (requires subsidy)

**Key Finding**: 86-96% of hospitals have negative operating results annually

---

### Operating Deficit

**Variable Name**: `operating_deficit`

**Definition**: Absolute value of negative operating results

**Formula**: `|min(0, resultados_operacionais)|`

**Units**: Euros (€)

**Use**: Numerator in subsidy dependence calculation

---

### Operating Margin

**Variable Name**: `operating_margin`

**Definition**: Operating results as percentage of revenue

**Formula**: `resultados_operacionais / rendimentos_operacionais`

**Scale**: -infinity to +infinity (typically -0.50 to +0.10)

**Interpretation**:
- 0.10: 10% operating margin (surplus)
- 0: Break-even
- -0.10: -10% margin (10% deficit)

---

## Instrumental Variables

### Political Instrument

**Variable Names**: `minister_left`, `minister_center`, `minister_right`, `minister_ideology`, `minister_party`

**Definition**: Political affiliation of Portuguese Minister of Health

**Values**:
- `minister_left`: 1 if Left government, 0 otherwise
- `minister_center`: 1 if Center/Independent, 0 otherwise
- `minister_right`: 1 if Right government, 0 otherwise

**Ideology Coding**:
- **Left**: PS (Partido Socialista)
- **Center**: Independent ministers
- **Right**: PSD (Partido Social Democrata)

**Coverage**: 741/741 observations (100%, 2017-2024)

**Source**: Political data collection (Wikipedia, government websites)
- File: `/03_data/external/political/minister_health_portugal_2017_2024.csv`

**Usage**: Attempted IV for subsidy allocation (FAILED - F=2.26, p=0.845)

**Key Finding**: Political ideology does NOT predict subsidy allocation in Portugal

---

### Historical Subsidy Instrument

**Variable Names**: `subsidy_dependence_lag1`, `subsidy_dependence_lag3`, `subsidy_dependence_lag4`, `subsidy_dependence_historical`

**Definition**: Lagged subsidy dependence as predictor of current subsidies

**Lags**:
- `lag1`: 1 year prior
- `lag3`: 3 years prior
- `lag4`: 4 years prior
- `historical`: Average of lag3 and lag4

**Rationale**: Path dependence in subsidy allocation, but long lag ensures no reverse causality

**Coverage**: 314/741 observations (42.2%) for historical instrument

**Correlation with Current**: r = 0.516 (moderate persistence)

**Usage**: IV for subsidy (p=0.041, but F=2.26 overall → weak instrument)

---

## Control Variables

### COVID Indicator

**Variable Name**: `covid`

**Definition**: Indicator for COVID-19 pandemic years

**Values**:
- 1: Years 2020-2021
- 0: All other years

**Coverage**: 741/741 observations (100%)

**In Regressions**: Absorbed by year fixed effects in FE models

---

### Time Trend

**Variable Name**: `time_trend`

**Definition**: Linear time trend

**Formula**: `year - min(year)`

**Values**: 0 (2017), 1 (2018), ..., 7 (2024)

**Usage**: Alternative to year fixed effects in some specifications

---

## Panel Structure Variables

### Entity Identifier

**Variable Name**: `entidade`

**Definition**: Hospital or health unit name

**Type**: String

**Values**: 149 unique entities
- Mix of pre-reform hospital names and post-reform ULS names
- Example: "Centro Hospitalar Universitário do Algarve, E.P.E."
- Example: "Unidade Local de Saúde de Gaia/Espinho, E. P. E."

**Note**: 2024 ULS reform created mergers (95 hospitals → 31 ULS)
- Crosswalk file: `hospital_to_uls_mapping_corrected.csv`

---

### Year

**Variable Name**: `year`

**Definition**: Calendar year of observation

**Type**: Integer

**Range**: 2017 to 2024 (main analysis)
- Full data: 2014 to 2025

**Panel Structure**: Hospital-year (unbalanced panel)

---

### Completeness Indicators

**Variable Names**: `has_ossr`, `has_spi`, `has_lrr`, `has_tlr`, `has_cqmi`, `n_components`

**Definition**: Flags indicating which PHFSI components are available

**Values**: Boolean (True/False) or Integer (count)

**Usage**: Sample selection for analysis

---

### Analysis Flags

**Variable Names**: `has_phfsi`, `has_subsidy`, `has_instruments`, `complete_for_iv`

**Definition**: Indicators for sample inclusion in specific analyses

- `has_phfsi`: Has 4-component PHFSI
- `has_subsidy`: Has subsidy dependence variable
- `has_instruments`: Has both political and historical instruments
- `complete_for_iv`: Has all required variables for IV analysis

**Coverage**:
- `has_phfsi`: 79/741 (10.7%)
- `has_subsidy`: 373/741 (50.3%)
- `has_instruments`: 313/741 (42.2%)
- `complete_for_iv`: 43/741 (5.8%)

---

## Data Sources Reference

### Primary Sources

| Source | URL | Coverage | License |
|--------|-----|----------|---------|
| SNS Transparency Portal | https://transparencia.sns.gov.pt | 2014-2025 | Public Domain |
| Eurostat | https://ec.europa.eu/eurostat | 1975-2024 | CC BY 4.0 |
| Political Data | Wikipedia + Gov sites | 2017-2024 | Public Info |

### File Locations

| Variable Category | Source File |
|-------------------|-------------|
| PHFSI Components | `/03_data/processed/variables/phfsi_components_complete.parquet` |
| Subsidy Data | `/03_data/processed/variables/subsidy_dependence_panel.parquet` |
| Panel (Merged) | `/03_data/processed/panel/panel_with_instruments.parquet` |
| Political Data | `/03_data/external/political/minister_health_portugal_2017_2024.csv` |
| Entity Crosswalk | `/03_data/processed/crosswalks/hospital_to_uls_mapping_corrected.csv` |

---

## Missing Data Codes

**Convention**:
- `NaN` (pandas): Missing data
- `None`: Not applicable

**No special codes used** (e.g., -999, 9999). All missing data represented as `NaN`.

---

## Units Summary

| Variable | Units |
|----------|-------|
| Financial amounts | Euros (€) |
| Ratios/Indices | Unitless (0-1 scale or ratio) |
| Percentages | Proportions (0-1, not 0-100) |
| Time | Years (integer), Days (integer) |

---

## Version History

- **v1.0** (January 2026): Initial data dictionary
  - All variables from Issues 2-9 included
  - Aligned with working paper version

---

**For questions about variable definitions**: See individual issue completion reports or contact author.

**Last Updated**: January 1, 2026
