# PEER REVIEW: Healthcare Economist Perspective
## Health Care Management Science

**Manuscript**: Stakeholder-Distributed Distress: Measuring Financial Sustainability in Public Hospitals Under Soft Budget Constraints

**Reviewer Profile**: Healthcare economist with expertise in hospital financing, payment systems, and health policy

---

## SUMMARY

This manuscript makes a significant contribution to healthcare finance literature by developing a theoretically grounded financial sustainability index specifically designed for public hospitals operating under soft budget constraints. The authors cleverly extend Kornai's soft budget constraint theory to mission-critical healthcare services and provide rigorous empirical evidence from Portugal's National Health Service. The PHFSI's ability to predict government intervention while capturing stakeholder-distributed distress represents a genuine methodological innovation. The finding that subsidy dependence reduces financial sustainability by 0.547 standard deviations (p < 0.001) has important policy implications for Beveridgean healthcare systems worldwide.

---

## MAJOR STRENGTHS

1. **Novel Theoretical Framework**: The stakeholder-distributed distress mechanism is an elegant extension of SBC theory. The sequential transfer logic (suppliers → staff → patients → taxpayers) is well-motivated and testable, addressing a genuine gap in the healthcare economics literature.

2. **Methodological Rigor**: Two-way fixed effects with hospital and year FE, clustered SEs, and eight robustness checks demonstrate careful econometric practice. The within-R² of 0.81 suggests strong explanatory power even after absorbing fixed effects.

3. **Policy Relevance**: The manuscript directly addresses the €500M October 2024 Portuguese bailout and similar interventions across Europe. The estimated 15-20% cost savings from PHFSI-based early warning systems is concrete and actionable.

4. **Data Transparency**: Use of publicly available administrative data from Portugal's Transparency Portal enhances replicability. The 741 hospital-year panel (149 entities, 2017-2024) provides sufficient statistical power.

5. **Strong Empirical Support for H1**: The subsidy-moral hazard relationship holds across 7/8 robustness tests, with economically significant effect sizes. The mechanism tests showing payment delay escalation (β = 87.3 days) are particularly compelling.

---

## MAJOR WEAKNESSES

1. **PHFSI Validation Incomplete** (Critical):
   - H2 (PHFSI predicts government intervention) cannot be fully tested because October 2024 capital injection micro-data is unavailable.
   - The entire contribution rests on PHFSI's predictive validity, yet the authors lack the validation outcome.
   - **Recommendation**: This is a publication blocker. Either (a) obtain Ministry of Finance data before submission, or (b) reframe H2 as a research agenda item for future work and focus the paper on H1 (subsidy-distress relationship).
   - **Mitigation**: Table 2 showing PHFSI discriminates across distress levels (267 vs. 98-day payment delays) provides face validity, but formal ROC analysis is essential for the "prediction model" framing.

2. **Limited External Validity** (Major):
   - Single-country study limits generalizability claims. Portugal's SNS has unique features (DRG prices below cost recovery, 180-240 day payment delays) that may not apply to UK NHS, Spanish regions, or Italian SSN.
   - The abstract and introduction make sweeping claims ("applies to any Beveridgean system") without empirical support.
   - **Recommendation**: Tone down generalizability claims or conduct multi-country validation (even descriptive replication in Spain/Italy would strengthen significantly).

3. **CQMI Component Missing** (Major):
   - One of five PHFSI components (Clinical Quality Maintenance Index) is entirely missing due to entity name mapping issues.
   - This creates a 4-component vs. 5-component PHFSI inconsistency across years, potentially biasing time trends.
   - The PHFSI is supposed to capture quality deterioration as a distress symptom, but CQMI is absent from all analyses.
   - **Recommendation**: Either (a) complete entity mapping to integrate CQMI, or (b) explicitly analyze 4-component PHFSI and discuss quality data limitations prominently in methods section.

4. **ULS Reform Analysis Inconclusive** (Major):
   - H3 (ULS integration improves sustainability) is tested only via event study (2017-2023), with no post-reform data.
   - The 2023 PHFSI improvement (0.378 vs. 2022: 0.334) is intriguing but could reflect:
     - (a) Anticipatory effects (hospitals improve knowing integration is coming)
     - (b) Selection bias (government chose better hospitals for early integration)
     - (c) Preparation funding (government injected capital pre-integration)
     - (d) Regression to the mean
   - Without post-2024 data, this analysis adds little beyond descriptive trends.
   - **Recommendation**: Either defer H3 to a follow-up paper or reframe as "preliminary evidence" and focus the paper on H1.

---

## MINOR ISSUES

1. **Terminology Precision**:
   - "Subsidy dependence" is not clearly operationalized. Does this include only direct Ministry of Health transfers, or also DRG underpayments (which effectively function as subsidies)?
   - The "True Leverage Ratio" (TLR) includes NPV(Expected Subsidies) but the discount rate choice (3-year rolling average at sovereign bond rate) seems arbitrary. Sensitivity analysis to discount rate would be valuable.

2. **Component Weighting**:
   - Equal weighting of PHFSI components is pragmatic but theoretically unmotivated. Why should SPI (stakeholder pressure) weight equally with OSSR (operational self-sufficiency)?
   - Robustness check uses PCA-based weights, but results are relegated to appendix. Main text should discuss whether component weights matter.

3. **Payment Delay Measurement**:
   - Average payment delays of 180-240 days are extraordinary (3-4× statutory limit). Are these measured correctly? Could there be data quality issues?
   - How are payment delays calculated? Days Sales Outstanding (DSO)? Accounts Payable Days?
   - Hospital heterogeneity in payment delays (SD?) would be informative.

4. **Missing Descriptive Statistics**:
   - Table 1 presents summary statistics but lacks correlations between key variables (subsidy dependence, payment delays, PHFSI).
   - Distribution plots (histograms) of PHFSI would help readers assess whether clustering into 3 groups (Distressed/Stable/Self-Sustaining) is natural or arbitrary.

5. **Governance Heterogeneity Underexplored**:
   - University hospital interaction (Column 3, Table 3) is marginally significant (p = 0.058) and shows *stronger* subsidy-induced moral hazard in university hospitals.
   - This counterintuitive finding deserves deeper discussion. Are university hospitals politically stronger (softer budget constraints) or weaker (more scrutiny)?

6. **COVID Period Treatment**:
   - COVID years (2020-2021) receive minimal attention despite massive healthcare disruptions.
   - Were there emergency subsidies during COVID that might confound the subsidy-distress relationship?
   - Robustness check excludes COVID years, but main results include them. Why not present COVID-excluded as the main spec?

---

## DETAILED COMMENTS BY SECTION

### Introduction (Excellent)
- **Strengths**: Compelling hook with €500M bailout, clear research gap, strong motivation.
- **Weakness**: Claims that PHFSI achieves AUC of 0.73 vs. Z-score AUC of 0.52, but these results are absent from the manuscript. Either include validation or remove this claim.
- Line "Preliminary evidence from Portugal's 2024 ULS integration reform indicates potential sustainability improvements" is overstated—evidence is very preliminary (pre-trends only).

### Theoretical Framework (Very Strong)
- **Strengths**: Excellent synthesis of soft budget constraints, stakeholder theory, and capital structure. The sequential transfer mechanism is well-developed and novel.
- **Weakness**: The framework predicts an *ordered sequence* (payment delays → staff turnover → quality decline), but empirical tests don't establish this ordering (would require Granger causality or lead-lag analysis).
- Prediction 2 ("SBC effects intensify with political salience") is mentioned but not tested. The Lisbon/Porto exclusion (robustness check) might address this, but it's not framed that way.

### Data and Methods (Solid)
- **Strengths**: Clear description of data sources, PHFSI construction, and econometric strategy. Sample size is adequate (741 hospital-years).
- **Weaknesses**:
  - CQMI component is described but missing from analysis (confusing).
  - Event study specification (Equation 8) is trivial (just year dummies on treated hospitals). This isn't really an "event study" in the modern econometrics sense (Borusyak et al. 2024, Callaway & Sant'Anna 2021).
  - No discussion of listwise deletion bias. With 741 observations from 149 entities over 8 years (theoretical max: 1,192), ~38% of observations are missing. Is missingness random?

### Results (Strong Empirics, Presentation Needs Work)
- **Strengths**: Main finding (subsidy → -0.547 SD on PHFSI) is economically large and statistically robust. Mechanism tests (payment delays) support the theory.
- **Weaknesses**:
  - Table 3 is difficult to interpret. Column headers need more detail. What are the DVs in Columns 2 and 3?
  - Figure 4 (ULS event study) shows only 2017-2023, but the figure caption mentions "Before and After." This is misleading—there's no "after."
  - Component-level effects (Table A2) are relegated to appendix but seem more important than some main text content.
  - The Lisbon/Porto exclusion (robustness check) showing no subsidy effect (β = -0.134, p = 0.312) is concerning. This suggests the effect concentrates in specific regions, raising external validity questions.

### Discussion (Good but Needs Revision)
- **Strengths**: Policy implications are concrete (PHFSI early warning, payment acceleration, subsidy conditionality). Literature contributions are clearly stated.
- **Weaknesses**:
  - Oversells generalizability. The sentence "our framework applies broadly to organizations with weak bankruptcy constraints" needs hedging—framework is tested only in Portuguese SNS hospitals.
  - Limitation section (5.4) is frank about missing governance data and entity mapping, which is good, but should also acknowledge validation data absence upfront.
  - The "15-20% cost savings" estimate is mentioned but not derived. Where does this number come from? Needs calculation or citation.

### Conclusion (Adequate)
- Appropriately restates contributions without overselling.
- Could be strengthened by previewing the follow-up research agenda (governance survey, multi-country replication).

---

## RECOMMENDATION

**MAJOR REVISION**

This manuscript has genuine merit and makes important contributions to healthcare finance. The theoretical framework is novel, the econometric execution is solid, and the policy relevance is high. However, three critical issues must be addressed before publication:

1. **PHFSI Validation**: Obtain October 2024 capital injection data or reframe the paper to focus on subsidy-distress relationship (H1) rather than prediction (H2).

2. **CQMI Integration**: Either complete entity mapping to include the 5th component or explicitly analyze 4-component PHFSI with clear documentation of the limitation.

3. **ULS Reform Analysis**: Either obtain post-2024 data for proper DiD estimation or remove H3 entirely and focus the paper on the subsidy-moral hazard mechanism.

Additionally, I recommend:
- Toning down generalizability claims in abstract/introduction until multi-country evidence exists.
- Expanding discussion of the Lisbon/Porto null result (suggests effect heterogeneity worth exploring).
- Adding diagnostic plots (PHFSI distribution, payment delay distribution).

With these revisions, this would be a strong contribution to *Health Care Management Science*. The subsidy-moral hazard finding alone (H1) is publication-worthy, and the PHFSI framework offers a valuable tool for healthcare policymakers.

---

## ADDITIONAL SUGGESTIONS FOR AUTHORS

1. **Consider a two-paper strategy**:
   - Paper 1 (current): PHFSI development + subsidy-distress relationship + validation (once data obtained)
   - Paper 2 (follow-up): ULS reform evaluation with full post-treatment data + governance mechanisms

2. **Engage with recent literature**: The manuscript cites foundational work (Kornai 1986, Altman 1968) but misses recent healthcare finance papers:
   - Bloom et al. (2020) on management practices in healthcare (*QJE*)
   - Gowrisankaran et al. (2021) on hospital mergers and quality (*AER*)
   - Chandra et al. (2016) on healthcare productivity (*JEP*)

3. **Data transparency**: Consider uploading replication package to Zenodo or Harvard Dataverse pre-submission (helps reviewers assess robustness).

---

**Reviewer Expertise**: Healthcare economics, hospital financing, empirical healthcare research

**Conflicts of Interest**: None

**Recommendation Timeline**: Major Revision → Conditional Accept (assuming authors address validation and CQMI issues)
