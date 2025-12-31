# Data Sources Documentation

## Primary Data Sources

### 1. SNS Transparency Portal
**URL:** https://transparencia.sns.gov.pt/

**Datasets:**
- Financial statements (annual balance sheets, income statements)
- Payment delays and overdue debt
- Operational performance metrics
- Quality indicators
- Government transfers

**Coverage:** 2017-present
**Granularity:** Hospital-level, monthly and annual
**Format:** Multiple formats available (CSV, JSON, Parquet, XLSX)

### 2. Eurostat
**Regional Data:**
- Population demographics by age, sex, region
- Regional GDP (NUTS classification)
- Employment by region
- Unemployment rates
- Health resources (physicians, hospital beds)
- Mortality and life expectancy

**Macro Indicators:**
- Economic indicators
- Health system statistics

**Location:** `03_data/raw/eurostat/`

### 3. INE (Instituto Nacional de Estatística)
**Portuguese Statistical Institute**

**Current Data:**
- National health statistics
- Demographic data
- Economic indicators

**Historical Data:**
- Time series data for trend analysis

**Location:** `03_data/raw/ine/`

### 4. ACSS (Administração Central do Sistema de Saúde)
**Central Health System Administration**

**Data:**
- Hospital budgets
- Performance contracts
- Payment mechanisms
- Audit reports
- Recent datasets on hospital benchmarking

**Location:** `03_data/raw/acss/`

## Secondary Data Sources

### 5. Ministry of Finance
- Capital injection allocations (e.g., October 2024: €500M)
- Historical bailout patterns
- ULS integration timeline

### 6. Tribunal de Contas (Court of Auditors)
- Hospital financial audits
- Management quality assessments
- Identified irregularities

## Data Organization

All data is organized in `03_data/` with the following structure:
- `raw/` - Original, unmodified data
- `processed/` - Cleaned and processed data
- `external/` - External validation data
- `metadata/` - Data documentation

## Data Quality Notes

- SNS data is generally high quality and updated regularly
- Some historical gaps exist for certain metrics
- Regional data may have classification changes (NUTS 2013 vs 2024)
- Payment delay data is self-reported by hospitals

## Access and Permissions

- SNS Transparency Portal: Public access, no authentication required
- Eurostat: Public access via API
- INE: Public access, some datasets require registration
- ACSS: Some detailed data requires formal request
- Tribunal de Contas: Public audit reports available online

## Last Updated
2025-12-31
