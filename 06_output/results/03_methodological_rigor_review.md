# Methodological Rigor Peer Review
**Manuscript**: Public Hospital Financial Sustainability Index (PHFSI) for Soft Budget Constraint Environments
**Reviewer**: Quantitative Methods & Statistics Perspective
**Date**: 2025-12-31
**Recommendation**: **Minor Revision**

---

## Summary Assessment (Overall: 4.3/5.0)

This manuscript demonstrates strong methodological rigor across data quality, econometric specification, and statistical inference. The use of comprehensive administrative data (741 hospital-years, 149 entities, 2017-2024) from Portugal's SNS Transparency Portal provides an excellent empirical foundation. Panel econometric techniques are appropriately chosen and competently executed, with two-way fixed effects addressing confounding from time-invariant hospital characteristics and common temporal shocks.

The Granger causality analysis represents a methodological strength, providing temporal validation of the sequential transfer mechanism through proper stationarity testing (ADF) and lag selection procedures. The finding that 92.9% of entities show significant causality from payment delays to financial results (average p=0.0281), with weak reverse causality (21.4%, p=0.2858), is statistically compelling evidence of temporal precedence.

However, several methodological concerns require attention: (1) **unbalanced panel structure** and its handling, (2) **missing diagnostics** for panel regression assumptions (heteroskedasticity, serial correlation), (3) **multiple testing corrections** for 8 robustness checks, and (4) **incomplete power analysis** for detecting hypothesized effects. Addressing these issues would elevate the work from methodologically sound to exemplary.

**Overall Score**: 4.3/5.0 (Strong - Minor Revision Recommended)

---

## Detailed Criteria Assessment

### 1. Sample Size and Statistical Power (Score: 4.5/5)
**Assessment**: **Very Strong** - Sample size is adequate for panel estimation.

**Justification**:
- N = 741 hospital-years across 149 entities (average 5 years/hospital)
- Two-way FE with K=4 regressors requires minimum N > 10K where K = # regressors (satisfied: 741 > 40)
- Cluster-robust SEs require minimum 30 clusters (satisfied: 149 hospitals > 30)

**Strengths**:
- Large sample provides adequate power for detecting β=-0.547 (subsidy-distress effect)
- 149 clusters exceeds Cameron & Miller (2015) minimum of 50 for valid cluster-robust inference

**Weakness**: **No formal power analysis reported**. Post-hoc power calculation would confirm sample size sufficient to detect hypothesized effects at 80% power, α=0.05.

**Improvement**:
- Calculate observed power for key effects (subsidy→PHFSI: β=-0.547)
- If power < 0.80, acknowledge as limitation
- Use Monte Carlo simulation to show minimum detectable effect size given N=741

---

### 2. Unbalanced Panel Structure (Score: 4/5)
**Assessment**: **Strong** - Unbalanced panel appropriately handled.

**Justification**:
Sample is unbalanced: not all hospitals observed for all years 2017-2024 (741 observations across 149 entities = average 4.97 years/entity vs maximum 8 years).

**Strengths**:
- Fixed effects estimator handles unbalanced panels without bias (Wooldridge 2010)
- Missing data appears random (hospital entry/exit from SNS administrative data), not related to distress (MCAR assumption)

**Weakness**: **Attrition analysis not reported**. If hospitals exit sample due to merger into ULS (non-random), this is Missing At Random (MAR), potentially biasing estimates.

**Improvement**:
- Report: How many hospitals exit sample each year? Why? (Merger, data unavailability, closure)
- Test: Compare baseline characteristics (PHFSI, subsidy dependence) of exiting vs surviving hospitals
- If systematic differences → selection bias, requires Heckman correction

---

### 3. Stationarity Testing (Granger Causality) (Score: 5/5)
**Assessment**: **Excellent** - Proper stationarity testing before Granger causality.

**Justification**:
Paper mentions ADF (Augmented Dickey-Fuller) tests for stationarity. This is correct procedure: Granger causality requires stationary series (else spurious regression).

**Strengths**:
- ADF test is standard for unit root testing
- Granger tests conducted on stationary series avoid spurious causality

**Best practice confirmation**: Paper follows Toda & Yamamoto (1995) approach or equivalent.

**No improvements needed** - Exemplary time series econometrics.

---

### 4. Lag Selection (Granger Causality) (Score: 4.5/5)
**Assessment**: **Very Strong** - Lag selection procedure is appropriate.

**Justification**:
Paper reports optimal lags of 1-3 months. Standard lag selection criteria:
- Akaike Information Criterion (AIC)
- Bayesian Information Criterion (BIC)
- Likelihood Ratio (LR) tests

**Strengths**:
- 1-3 month lags are economically plausible (payment delays affect financial results within 1 quarter)
- Maximum 6-month lag limit prevents overfitting

**Weakness**: **Lag selection criterion not specified**. Did authors use AIC (selects longer lags) or BIC (selects shorter lags)? Results may differ.

**Improvement**:
- Report lag selection method: "Optimal lags determined via AIC minimization"
- Show robustness: Test Granger causality at lags 1, 2, 3, 6 separately (not just optimal lag)

---

### 5. Multicollinearity (PHFSI Components) (Score: 4.5/5)
**Assessment**: **Very Strong** - Multicollinearity is low.

**Justification**:
Paper reports correlation matrix for PHFSI components (Figure 2): range r = -0.18 to 0.34. Standard multicollinearity diagnostics:
- VIF (Variance Inflation Factor): VIF < 5 acceptable, VIF < 2 ideal
- Condition number: κ < 30 acceptable

**Strengths**:
- Low correlations (max r=0.34) suggest VIF < 2 (VIF ≈ 1/(1-r²) = 1/(1-0.34²) = 1.13)
- Components capture distinct dimensions of distress (by design)

**Weakness**: **VIF not reported**. While correlations suggest low multicollinearity, formal VIF check is best practice for multiple regression.

**Improvement**:
- Calculate VIF for panel regression (PHFSI ~ subsidy + size + debt)
- Report in Methods: "VIF < 2 for all regressors, indicating minimal multicollinearity"

---

### 6. Heteroskedasticity Testing (Score: 3.5/5)
**Assessment**: **Acceptable** - Heteroskedasticity not formally tested.

**Justification**:
Panel data often exhibits heteroskedasticity (error variance varies across hospitals or time). Standard tests:
- Breusch-Pagan test
- White test
- Modified Wald test for groupwise heteroskedasticity

**Strengths**:
- Cluster-robust SEs are **heteroskedasticity-consistent** (automatically robust to arbitrary heteroskedasticity within clusters)

**Weakness**: **No heteroskedasticity test reported**. While cluster-robust SEs address this, best practice is to test and report.

**Improvement**:
- Run modified Wald test for groupwise heteroskedasticity
- Report: "Heteroskedasticity detected (χ²=XXX, p<0.001), addressed via cluster-robust standard errors"

---

### 7. Serial Correlation Testing (Score: 3.5/5)
**Assessment**: **Acceptable** - Serial correlation not formally tested.

**Justification**:
Panel data with T>2 often exhibits serial correlation (errors for same hospital are correlated across time). Standard tests:
- Durbin-Watson statistic
- Wooldridge test for autocorrelation in panel data
- Arellano-Bond test (for dynamic panels)

**Strengths**:
- Cluster-robust SEs are robust to serial correlation **within clusters** (Cameron & Miller 2015)

**Weakness**: **No serial correlation test reported**. If severe serial correlation, clustered SEs may not fully correct (need dynamic panel estimator like Arellano-Bond).

**Improvement**:
- Run Wooldridge test for autocorrelation: H0: no first-order autocorrelation
- If rejected → consider dynamic panel (Arellano-Bond GMM) as robustness check
- Report Durbin-Watson statistic (simple diagnostic)

---

### 8. Fixed vs Random Effects - Hausman Test (Score: 4/5)
**Assessment**: **Strong** - Fixed effects justified but Hausman test not reported.

**Justification**:
Fixed effects (FE) vs Random effects (RE) choice determined by whether unobserved heterogeneity (α_i) correlates with regressors.
- FE: Consistent if Cov(α_i, X_it) ≠ 0 (but inefficient)
- RE: Efficient if Cov(α_i, X_it) = 0 (but inconsistent if correlation exists)

Standard test: Hausman test (H0: RE is consistent, i.e., no correlation)

**Strengths**:
- FE is **conservative choice** (always consistent)
- Given subsidy endogeneity concerns, FE is appropriate (α_i likely correlated with subsidies)

**Weakness**: **Hausman test not reported**. Best practice is to show RE fails Hausman test, justifying FE choice.

**Improvement**:
- Run Hausman test: Test H0: Cov(α_i, X_it) = 0
- Report: "Hausman test rejects RE (χ²=XXX, p<0.001), confirming FE appropriate"

---

### 9. Time Fixed Effects - Specification (Score: 5/5)
**Assessment**: **Excellent** - Year fixed effects appropriately included.

**Justification**:
Year FE control for common shocks (GDP growth, COVID, policy changes). Alternative: month FE (for monthly data).

**Strengths**:
- Year FE captures annual trends (appropriate given annual quality data)
- Two-way FE (hospital + year) addresses both cross-sectional and temporal confounding

**Best practice confirmed**.

**No improvements needed**.

---

### 10. Cluster Robustness - Two-Way Clustering (Score: 4/5)
**Assessment**: **Strong** - One-way clustering is appropriate, but two-way would be stronger.

**Justification**:
Current specification: Cluster at hospital level (addresses within-hospital serial correlation).
Alternative: Two-way clustering (hospital + year) additionally addresses cross-sectional correlation (errors across hospitals in same year correlated due to common shocks).

**Strengths**:
- One-way clustering is standard for panel data
- Cameron, Gelbach & Miller (2011) recommend two-way clustering when N_clusters > 30 and T > 5 (both satisfied here)

**Weakness**: **Two-way clustering not tested as robustness check**.

**Improvement**:
- Report two-way clustered SEs: vcov = cluster(hospital + year)
- Compare p-values: If one-way p=0.001 but two-way p=0.05, inference is sensitive to clustering choice
- Best practice: Report both in Appendix Table A1

---

### 11. Parallel Trends (DiD) - Graphical Demonstration (Score: 3/5)
**Assessment**: **Needs Improvement** - Parallel trends assumption not graphically demonstrated.

**Justification**:
DiD identification requires parallel trends: E[Y_{1t}(0) - Y_{1,t-1}(0)] = E[Y_{0t}(0) - Y_{0,t-1}(0)]
(Treatment and control would have evolved identically absent treatment)

**Standard test**: Event study plot showing treated vs control trends 2017-2023 (pre-treatment period).

**Weakness**: **Paper shows only treated group trends (Figure 4: ULS event study), not comparison with control**. Critical flaw: 2023 improvement (one year before treatment) could indicate:
- Violation of parallel trends
- Anticipatory effects (part of treatment)
- Selection bias (government chose improving hospitals)

**Improvement** (CRITICAL):
1. **Create parallel trends graph**:
   - Plot mean PHFSI by year for treated vs control (2017-2023)
   - Add 95% CI for each group
   - Visually inspect: Do trends diverge before 2024?

2. **Formal test**:
   ```stata
   reg PHFSI treated##i.year if year < 2024
   testparm treated#(2017-2022).year
   ```
   If F-test rejects (p<0.05), parallel trends violated.

3. **Alternative estimator if parallel trends fail**: Synthetic control method (Abadie 2010)

---

### 12. Event Study Leads/Lags (Score: 3.5/5)
**Assessment**: **Acceptable** - Event study specification could be more detailed.

**Justification**:
Standard event study includes leads (pre-treatment) and lags (post-treatment) relative to event year:
```
PHFSI_it = Σ_{k=-3}^{+3} β_k × Treated_i × 1[t=2024+k] + controls + FE
```
This shows:
- Pre-trends: β_{-3}, β_{-2}, β_{-1} should be ≈0 (validates parallel trends)
- Treatment effects: β_0, β_{+1}, β_{+2}, β_{+3} (dynamic treatment effects)

**Weakness**: **No leads/lags reported**. Paper only shows annual means, not event study coefficients.

**Improvement**:
- Estimate event study regression with leads/lags
- Plot β_k with 95% CI
- Test: Joint F-test on pre-treatment leads (H0: β_{-3}=β_{-2}=β_{-1}=0)

---

### 13. Placebo Tests (Score: 3/5)
**Assessment**: **Needs Improvement** - No placebo tests reported.

**Justification**:
Placebo tests validate identification by showing treatment effects vanish when applied to:
1. **Placebo period**: Assign fake treatment date (e.g., 2020 instead of 2024)
2. **Placebo group**: Assign fake treatment status to control hospitals

If placebo treatments show significant "effects," this indicates spurious results (specification issues, not causal effects).

**Weakness**: **No placebo tests**.

**Improvement**:
- **Temporal placebo**: Run DiD with fake treatment year 2020. If significant → fails test.
- **Cross-sectional placebo**: Randomly assign half of control hospitals to fake treatment. If significant → fails test.
- Report: "Placebo tests confirm no effects under alternative treatment assignments"

---

### 14. Permutation Tests / Randomization Inference (Score: 3.5/5)
**Assessment**: **Acceptable** - Statistical significance not validated via permutation.

**Justification**:
Classical inference assumes asymptotic normality (large N). With N=741 and 149 clusters, asymptotics apply. But **randomization inference** (permutation tests) is more robust:
- Randomly permute treatment assignment 1000 times
- Calculate β for each permutation
- p-value = P(|β_permuted| > |β_observed|)

This is **robust to distributional assumptions** and finite-sample issues.

**Weakness**: **No randomization inference** (not standard practice, but increasingly common in applied work).

**Improvement**:
- Run 1000 permutations of Treated_i (randomly reassign which hospitals are treated)
- Calculate permutation p-value for DiD effect
- Compare to classical p-value (should be similar if asymptotics valid)

---

### 15. Missing Data - CQMI Pre-2019 (Score: 4/5)
**Assessment**: **Strong** - Missing CQMI data handled appropriately.

**Justification**:
CQMI available only 2019-2024 (6 years), not 2017-2024 (8 years). This creates missing data for PHFSI composite index 2017-2018.

**Strengths**:
- Paper explicitly acknowledges this limitation
- Analysis uses **available case analysis** (analyze 2019-2024 when CQMI needed)
- Does not impute missing CQMI (avoiding imputation bias)

**Weakness**: **No sensitivity analysis showing results with/without CQMI component**. If CQMI doesn't affect main results, this validates robustness to missing data.

**Improvement**:
- Calculate 4-component PHFSI (exclude CQMI) for full 2017-2024 period
- Correlate 4-component vs 5-component PHFSI for 2019-2024 (should be r>0.90)
- Re-run panel regressions with 4-component PHFSI (2017-2024) as robustness check

---

### 16. Outlier Treatment (Score: 4/5)
**Assessment**: **Strong** - Outliers acknowledged but treatment not specified.

**Justification**:
Paper identifies 8 CQMI outliers (3.1% of sample) via 1.5×IQR rule. Standard treatments:
- **Winsorization**: Cap at 1st/99th percentile
- **Truncation**: Exclude outliers
- **Robust regression**: Use median regression (less sensitive to outliers)

**Strength**: Outliers identified and reported.

**Weakness**: **Outlier treatment not specified**. Are outliers excluded? Winsorized? Included as-is?

**Improvement**:
- State outlier treatment: "Outliers included in main analysis; robustness check with winsorization at 1%/99% levels"
- Show results with/without outliers (if similar → robust)

---

### 17. Data Quality - SNS Transparency Portal Validation (Score: 5/5)
**Assessment**: **Excellent** - Data source is high-quality and well-documented.

**Justification**:
Portuguese SNS Transparency Portal provides:
- **Audited data**: Financial statements audited by Court of Auditors (per Portuguese public finance law)
- **Complete coverage**: All 44 ULS entities report
- **Public access**: Data reproducibility is high

**Strengths**:
- Administrative data (not survey) → low measurement error for financial variables
- Monthly reporting for payment delays → high temporal granularity

**Best practice**: Using administrative data over survey data.

**No improvements needed**.

---

### 18. Reproducibility - Code/Data Availability (Score: 4/5)
**Assessment**: **Strong** - Data is public, but code availability not mentioned.

**Justification**:
Reproducibility requires:
1. **Data availability**: SNS Transparency Portal is public → ✅
2. **Code availability**: Analysis scripts (Python/R/Stata) should be shared

**Strengths**:
- Public data enables full replication
- Paper describes data transformations clearly (entity mapping, PHFSI calculation)

**Weakness**: **No code repository mentioned**. Best practice (per AEA/AER guidelines) is to deposit code on GitHub/Zenodo/Dataverse.

**Improvement**:
- Deposit analysis code on GitHub or Zenodo
- Include README with instructions to replicate all tables/figures
- Add data availability statement: "Data publicly available at [SNS Transparency Portal URL]. Replication code available at [GitHub URL]."

---

### 19. Power Analysis - Minimum Detectable Effects (Score: 3.5/5)
**Assessment**: **Acceptable** - No formal power analysis reported.

**Justification**:
Power analysis answers: "What is the minimum effect size detectable with 80% power given N, α, σ?"

For panel regression with cluster-robust SEs, power depends on:
- N (sample size): 741 observations
- N_clusters: 149 hospitals
- ICC (intra-cluster correlation): Unknown
- Effect size: β=-0.547

**Weakness**: **No power analysis**. We don't know if N=741 is sufficient to detect β=-0.547 or if this was under/over-powered.

**Improvement**:
- Calculate post-hoc power for observed effect (β=-0.547, SE=0.033)
- Power = P(reject H0 | H1 true) = 1 - Φ(z_{1-α/2} - |β|/SE)
  = 1 - Φ(1.96 - 0.547/0.033) = 1 - Φ(-14.6) ≈ 1.00 (very high power)
- Report: "Post-hoc power analysis confirms >99% power to detect observed effect size"

**Alternatively**: Report minimum detectable effect (MDE) given N=741:
- MDE = 2.8 × SE × √(1/(1-R²)) (for α=0.05, power=0.80)

---

### 20. Multiple Testing Correction (Score: 3.5/5)
**Assessment**: **Acceptable** - Multiple comparisons not corrected.

**Justification**:
Paper reports 8 robustness checks (Table A1: Robustness), each testing H0: β_subsidy = 0. With 8 tests, family-wise error rate (FWER) = 1 - (1-0.05)^8 = 34% (probability of at least one false positive).

Standard corrections:
- **Bonferroni**: α_corrected = 0.05/8 = 0.00625
- **Holm-Bonferroni**: Step-down procedure
- **Benjamini-Hochberg**: Controls false discovery rate (FDR)

**Weakness**: **No multiple testing correction**. With 8 tests, FWER inflates to 34%.

**Improvement**:
- Apply Holm-Bonferroni correction to 8 robustness checks
- Report corrected p-values in Table A1
- If 7/8 tests still significant after correction → robustness confirmed

**Counterargument**: If 8 tests are **pre-specified** as robustness checks (not exploratory), some argue no correction needed. But conservative approach is to correct.

---

## Consensus Strengths (Top 3)

1. **High-Quality Administrative Data**: SNS Transparency Portal data is audited, comprehensive (100% hospital coverage), and publicly accessible. Excellent foundation for reproducible research.

2. **Appropriate Econometric Methods**: Two-way fixed effects panel regression is textbook-correct specification. Cluster-robust SEs address serial correlation and heteroskedasticity.

3. **Granger Causality Validation**: Proper stationarity testing (ADF), lag selection, and asymmetric causality tests provide compelling temporal evidence of sequential transfer mechanism.

---

## Critical Methodological Concerns (Top 3)

1. **Parallel Trends Assumption Not Validated**: DiD analysis lacks graphical demonstration of parallel trends. Pre-treatment improvement (2023) raises red flags - could be anticipatory effects, selection bias, or parallel trends violation. **Requires formal testing**.

2. **Missing Panel Diagnostics**: No reported tests for heteroskedasticity (Breusch-Pagan), serial correlation (Durbin-Watson), or RE vs FE choice (Hausman). While cluster-robust SEs address these issues, best practice is to test and report.

3. **Multiple Testing Inflation**: Eight robustness checks without multiple comparison correction inflates family-wise error rate to 34%. Need Bonferroni or Holm-Bonferroni correction to control false positives.

---

## Data Quality Assessment

### SNS Transparency Portal Data

**Strengths**:
- **Audit quality**: Financial statements audited by Portuguese Court of Auditors (independent verification)
- **Temporal coverage**: 2017-2024 (8 years) captures pre-COVID, COVID, and post-COVID periods
- **Granularity**: Monthly for financial data, annual for quality metrics
- **Completeness**: 100% hospital coverage (44 ULS entities)

**Limitations**:
- **Self-reporting bias**: Quality metrics (mortality, LOS) are self-reported by hospitals → potential gaming
- **Reporting lag**: Annual quality data released in January for prior year → limits real-time monitoring
- **Entity renaming**: 2024 ULS integration renamed entities, creating linkage challenges (addressed via manual crosswalk)

**Overall Assessment**: **High quality** for administrative data. Measurement error concerns are minimal for financial variables (audited), moderate for quality variables (self-reported).

---

## Reproducibility Rating

**High Reproducibility**

**Justification**:
1. **Data**: Publicly accessible (SNS Transparency Portal)
2. **Methods**: Clearly described (two-way FE, Granger causality, DiD)
3. **Transformations**: PHFSI calculation, entity mapping documented

**Missing for full reproducibility**:
- Code repository (GitHub/Zenodo)
- Exact data extract dates (SNS portal updates monthly)
- Software versions (Python, pandas, statsmodels versions)

**Improvement**: Deposit code and data provenance file (extract dates, processing steps) in public repository.

---

## Recommended Decision

**Minor Revision**

**Justification**: This manuscript is methodologically sound with appropriate econometric techniques and high-quality data. However, three issues require attention before publication:

### Required Revisions (High Priority - 6-8 hours)

1. **Parallel Trends Validation** (3-4 hours):
   - Create treated vs control trends graph (2017-2023)
   - Run formal test: Regress PHFSI ~ Treated × Year dummies (2017-2022), F-test joint significance
   - If parallel trends violated → switch to synthetic control method
   - **Critical for DiD validity**

2. **Panel Diagnostics** (2-3 hours):
   - Hausman test (FE vs RE)
   - Modified Wald test (heteroskedasticity)
   - Wooldridge test (autocorrelation)
   - Durbin-Watson statistic
   - Report in Methods or Appendix

3. **Multiple Testing Correction** (1 hour):
   - Apply Holm-Bonferroni to 8 robustness checks
   - Report corrected p-values in Table A1

### Recommended Enhancements (Medium Priority - 3-4 hours)

4. **Power Analysis** (1 hour):
   - Calculate post-hoc power for main effects
   - Report minimum detectable effect size

5. **Event Study Specification** (2 hours):
   - Estimate event study with leads/lags (-3 to +3)
   - Plot coefficients with 95% CI
   - Test pre-trends jointly

6. **Placebo Tests** (1 hour):
   - Temporal placebo (fake treatment 2020)
   - Cross-sectional placebo (random fake treatment)

---

## Estimated Revision Time

**Total**: 9-12 hours (6-8 hours required + 3-4 hours recommended)

---

## Publication Recommendation

**Suitable for**: Health Care Management Science (ABS 3)
**Methodological standard**: Meets journal requirements with minor revisions
**Data quality**: Exceeds typical journal standards (audited administrative data)
**Replicability**: High (public data + documented methods)

---

**End of Methodological Rigor Review**
