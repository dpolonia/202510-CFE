# Methodology Notes

## Research Design Overview

**Overall Strategy:** Sequential Explanatory Mixed Methods

### Phase 1: Developing PHFSI (Public Hospital Financial Sustainability Index)

**Components (equal-weighted):**

1. **Operational Self-Sufficiency Ratio (OSSR)**
   - Formula: `OSSR = Operating Revenue (excluding subsidies) / Operating Expenses`
   - Range: 0 (fully dependent) to 1+ (self-financing)

2. **Stakeholder Pressure Index (SPI)**
   - Formula: `SPI = [Supplier Payment Days / 90] + [Overdue Liabilities / Total Liabilities] + [Staff Turnover Rate] + [Patient Complaint Rate / 1000]`
   - Range: 0 (no pressure) to 4+ (severe pressure)

3. **Liquidity Realization Rate (LRR)**
   - Formula: `LRR = Cash Collections_t / Accrued Revenue_(t-1)`
   - Adjusts for collection lags

4. **True Leverage Ratio (TLR)**
   - Formula: `TLR = (Liabilities + NPV Expected Subsidies) / Operating Retained Earnings`
   - Accounts for implicit leverage from subsidies

5. **Clinical Quality Maintenance Index (CQMI)**
   - Formula: `CQMI = [Patient Safety Indicators + Access Metrics + Clinical Outcomes] / Regional Benchmarks`
   - Range: 0 (severe deterioration) to 1+ (above average)

### Phase 2: Panel Regression Analysis

**Model 1: Fixed Effects Panel Regression**
```
PHFSI_it = α + β₁(Governance_it) + β₂(Size_it) + β₃(Case_Mix_it) +
           β₄(Regional_Factors_it) + θᵢ + γₜ + εᵢₜ
```

Where:
- θᵢ = hospital fixed effects
- γₜ = year fixed effects
- Robust standard errors clustered at hospital level

**Model 2: Dynamic Panel (Arellano-Bond GMM)**
```
PHFSI_it = α + λ(PHFSI_i,t-1) + β₁(Governance_it) + β₂(Subsidies_it) +
           β₃(Payment_Delays_it) + εᵢₜ
```

### Phase 3: Quasi-Experimental Analysis

**Natural Experiment: 2024 ULS Integration Reform**

Staggered difference-in-differences:
```
PHFSI_it = β₀ + β₁(Treated_i × Post_t) + β₂(Treated_i) + β₃(Post_t) +
           β₄(X_it) + θᵢ + γₜ + εᵢₜ
```

**Identification assumption:** Parallel trends in PHFSI prior to integration

### Phase 4: Governance Analysis

- Board composition survey
- Archival data on manager characteristics
- Political appointment patterns
- Cluster analysis by governance quality

## Key Variables

### Dependent Variables
- PHFSI (composite index)
- Individual PHFSI components
- Government intervention (binary)

### Independent Variables
- Governance quality index
- Hospital size measures
- Case-mix complexity
- Regional economic factors
- Subsidy dependence
- Political factors

### Control Variables
- COVID period indicator
- ULS integration status
- Hospital specialty mix

## Statistical Software
- Python (pandas, statsmodels, scikit-learn)
- R (for robustness checks)
- Stata (for publication-standard tables)

## Last Updated
2025-12-31
