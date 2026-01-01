# PEER REVIEW: Corporate Finance Scholar Perspective
## Health Care Management Science

**Manuscript**: Stakeholder-Distributed Distress: Measuring Financial Sustainability in Public Hospitals Under Soft Budget Constraints

**Reviewer Profile**: Corporate finance professor with expertise in capital structure, financial distress prediction, and empirical corporate finance methods

---

## SUMMARY

This paper attempts to bridge corporate finance distress prediction models with public sector organizations that cannot file bankruptcy. The core insight—that public hospital distress manifests as stakeholder burden distribution rather than discrete failure—is conceptually appealing and potentially generalizable. The empirical execution using Portuguese hospital data is competent, employing panel fixed effects models with appropriate robustness checks. However, the paper suffers from three fundamental issues: (1) the PHFSI index lacks external validation against actual government intervention decisions, rendering the "prediction" claim unsubstantiated; (2) the theoretical framework, while creative, makes testable predictions about sequential stakeholder burden transfer that are never empirically verified; and (3) the manuscript oversells generalizability to private sector settings (SOEs, SIFIs, municipalities) without any evidence beyond healthcare.

---

## MAJOR STRENGTHS

1. **Addresses Genuine Theoretical Puzzle**: The Xanthakis et al. (2009) finding that Altman Z-score achieves AUC ≈ 0.50 for Greek public hospitals is striking. This paper correctly identifies that conventional distress models fail because they assume bankruptcy constraints exist. The stakeholder-distributed distress framework is a creative solution.

2. **Robust Econometric Design**: Two-way fixed effects (hospital + year FE) with clustered standard errors is appropriate. The within-R² of 0.81 indicates strong fit after absorbing fixed effects. Eight robustness checks (Table A1) demonstrate that the subsidy-distress relationship is not driven by specification choices—this is good empirical practice.

3. **Effect Size Economically Meaningful**: A one-percentage-point increase in subsidy dependence reducing PHFSI by 0.547 standard deviations translates to moving from 25th to 75th percentile (subsidy dependence: 0.12 → 0.24) reducing PHFSI by 19% of sample mean. This is large enough to matter for policy.

4. **Novel Capital Structure Insight**: The "True Leverage Ratio" concept—incorporating NPV of expected future subsidies into leverage calculation—is genuinely innovative. This addresses a real conceptual gap: conventional debt ratios severely understate public sector leverage because implicit government guarantees don't appear on balance sheets.

5. **Transparent Data**: Using publicly available administrative data enhances credibility. Replication potential is high (unlike many corporate finance papers using proprietary BoardEx or Credit Suisse data).

---

## MAJOR WEAKNESSES

1. **PHFSI Lacks Validation** (Fatal Flaw):
   - The entire contribution rests on PHFSI being a better predictor of government intervention than Altman Z-score.
   - Hypothesis 2 explicitly states: "PHFSI should exhibit superior predictive validity for government capital injections compared to conventional bankruptcy prediction models."
   - **But the validation is never conducted.** The authors cite October 2024 capital injection micro-data as unavailable.
   - This is like developing a credit scoring model and publishing it without ever testing whether it predicts default better than FICO scores.
   - **From a corporate finance perspective, this is a publication blocker.** Prediction models must demonstrate out-of-sample predictive power. In-sample fit (R² = 0.81) is insufficient.

   **Recommendation**: Either:
   - (a) Obtain Ministry of Finance data and conduct proper ROC analysis, or
   - (b) Reframe the paper as "developing and describing" PHFSI rather than "validating" it, or
   - (c) Use an alternative validation outcome (e.g., hospital closures, CEO turnover, regulatory intervention)

2. **Sequential Transfer Mechanism Untested** (Major):
   - The theoretical framework's key prediction is that distress transfers sequentially: suppliers → staff → patients → taxpayers.
   - This implies testable lead-lag relationships:
     - Payment delays at t should predict staff turnover at t+1
     - Staff turnover at t should predict quality deterioration at t+1
     - Quality deterioration at t should predict bailouts at t+1
   - **None of these predictions are tested.** The mechanism tests (Section 4.3) just show cross-sectional correlations between subsidy dependence and various distress symptoms, not their temporal ordering.
   - From a finance perspective, establishing *timing* is critical. Does liquidity stress *cause* quality decline, or do they co-occur? Granger causality tests would address this.

   **Recommendation**: Either conduct lead-lag analysis using monthly data or soften claims about "sequential" transfer.

3. **Endogeneity Concerns Insufficiently Addressed** (Major):
   - The subsidy-distress relationship (H1) could reflect reverse causality: governments increase subsidies *in response to* distress, not subsidies *causing* distress.
   - The authors use two-way fixed effects, which controls for time-invariant hospital characteristics and common time shocks. But this doesn't address time-varying endogeneity.
   - Ideally, you'd want:
     - (a) An instrument for subsidy dependence (e.g., political alignment between hospital region and national government, or lagged subsidy eligibility rules), or
     - (b) A natural experiment (e.g., did subsidy allocation rules change discontinuously, creating regression discontinuity design?), or
     - (c) Explicit discussion acknowledging the endogeneity problem and what it implies for interpretation.

   **Recommendation**: Frame the subsidy-distress relationship as "correlational" rather than "causal," or pursue IV strategy if feasible.

4. **Limited Comparison to Alternative Models** (Moderate):
   - The paper claims PHFSI outperforms Altman Z-score but never *shows* this comparison.
   - Table 2 demonstrates PHFSI discriminates across distress levels (Distressed vs. Self-Sustaining hospitals), but so would many simple metrics (e.g., current ratio, ROA, leverage).
   - What's the incremental value of PHFSI over simpler alternatives?
   - **From a finance perspective**: If PHFSI = f(OSSR, SPI, LRR, TLR), does the equal-weighted composite predict better than just using OSSR alone? Or just payment delays alone?

   **Recommendation**: Run "horse race" regressions comparing PHFSI predictive power to:
   - Altman Z-score (adapted for nonprofits)
   - Simple leverage ratio
   - Payment delays alone
   - First principal component of the 4 PHFSI components

---

## MINOR ISSUES

1. **Component Independence Assumption**:
   - PHFSI equal-weights four components, implicitly assuming they're independent dimensions of distress.
   - But Figure 2 shows correlations ranging from -0.18 to 0.34. Why not use factor analysis to determine empirical weights?
   - The PCA robustness check (Table A1) shows β = -0.563, very close to the main result (β = -0.547), suggesting weights don't matter much. This is reassuring but should be highlighted in main text.

2. **Missing Variable Bias**:
   - Hospital governance (board composition, CEO tenure, managerial ability) is unobserved. This is a first-order determinant of financial performance.
   - Authors acknowledge this limitation but don't discuss direction of bias. If better-governed hospitals receive *fewer* subsidies (because they're more self-sufficient), the subsidy-distress coefficient would be *downward* biased (i.e., you're understating the true moral hazard effect). Conversely, if worse-governed hospitals receive *more* subsidies (political capture), the coefficient would be *upward* biased.

3. **Cluster Definitions Arbitrary**:
   - PHFSI < 0.4 = Distressed, 0.4–0.7 = Stable, ≥ 0.7 = Self-Sustaining. Where do these thresholds come from?
   - In corporate finance, we typically use empirically-motivated cutoffs (e.g., quintiles, or thresholds that maximize prediction accuracy).
   - Appendix should justify these choices or show robustness to alternative cutoffs.

4. **Sample Selection**:
   - The panel has 741 observations from potential 1,192 (149 entities × 8 years), implying 38% missingness.
   - What causes missingness? New hospital entries/exits? Mergers? Data reporting gaps?
   - If missingness is non-random (e.g., distressed hospitals stop reporting), this creates selection bias.

5. **ULS Reform Analysis Adds Little**:
   - H3 (ULS integration improves sustainability) is empirically weak. The "event study" shows only pre-reform trends; no post-reform data exist.
   - The 2023 PHFSI improvement (0.378 vs. 2022: 0.334, p = 0.041) is statistically significant but could easily be:
     - Regression to the mean (2022 was a trough)
     - Preparation funding (government injected capital before formal integration)
     - Sample composition changes (hospital exits/entries)
   - Without control group and post-treatment data, this analysis is uninformative.

   **Recommendation**: Remove H3 entirely or relegate to a brief appendix section titled "Preliminary descriptive evidence on ULS reform."

---

## DETAILED COMMENTS BY SECTION

### Introduction
- **Line claiming AUC = 0.73 for PHFSI vs. 0.52 for Z-score**: This result doesn't appear anywhere in the manuscript. Remove or demonstrate it.
- "Strongly support H1" (page 6): This language is appropriate.
- "Preliminary evidence suggests ULS integration may improve sustainability": This is fine if framed as speculative.

### Theoretical Framework
- **Section 2.1 (Soft Budget Constraints)**: Excellent literature synthesis. The extension to mission-critical services is well-motivated.
- **Section 2.2 (Stakeholder-Distributed Distress)**: Creative framework, but the sequential transfer mechanism needs empirical verification. As written, it's a theoretical conjecture.
- **Section 2.3 (Capital Structure)**: The modified pecking order with implicit subsidies is insightful. However, the claim that "optimal leverage is theoretically zero" is too strong. Even without tax benefits or bankruptcy costs, hospitals might use *strategic* debt to signal distress and extract bailouts (Kornai 2003). This point is mentioned but could be developed further.
- **Hypothesis 1**: Well-specified. The equation (Equation 1) appropriately includes hospital and year fixed effects.
- **Hypothesis 3 (ULS Reform)**: The parallel trends assumption is stated but never tested. Event study plots should show coefficient estimates for each pre-treatment year (2017–2023) to assess pre-trends.

### Data and Methods
- **Sample description**: Clear and comprehensive.
- **PHFSI construction**: Transparent, though component weighting rationale is weak.
- **Econometric strategy**: Appropriate. Clustered SEs at hospital level is correct choice.
- **Event study specification (Equation 8)**: This isn't a true event study—it's just year dummies. For modern event study methodology, see Borusyak et al. (2024) or Callaway & Sant'Anna (2021). Not a major issue, but terminology is misleading.

### Results
- **Table 3 (Panel Regressions)**: Well-presented. Column headers could be clearer. What are the DVs in Columns 2 and 3? From reading the text, I infer Column 2 = Payment Delays and Column 3 = PHFSI again with governance interactions, but this should be explicit.
- **Robustness checks**: Excellent. The Lisbon/Porto exclusion showing β = -0.134 (p = 0.312) is concerning—suggests the effect is geographically concentrated. This deserves discussion.
- **Figure 4**: Misleading caption. It says "Before and After ULS Integration Reform" but only shows "before." Either fix the caption or add post-reform data.

### Discussion
- **Policy implications**: Concrete and actionable. The 15-20% cost savings estimate needs derivation or citation.
- **Generalizability claims**: Overstated. The sentence "our framework applies to any organization with weak bankruptcy constraints" is speculative. You've tested it only in Portuguese hospitals.
- **Limitations (Section 5.4)**: Refreshingly honest about missing data (capital injection micro-data, entity mapping, governance data). I appreciate the transparency.

### Conclusion
- Appropriately cautious. Avoids overselling.

---

## RECOMMENDATION

**MAJOR REVISION** (borderline **REJECT AND RESUBMIT**)

From a corporate finance methodology perspective, this paper has a fatal flaw: **it develops a prediction model but never validates it**. Hypothesis 2 explicitly claims PHFSI predicts government intervention better than Z-score, but this is never demonstrated. In any top finance journal (JF, JFE, RFS), this would be grounds for immediate rejection.

However, the paper has redeeming qualities:
1. The subsidy-moral hazard finding (H1) is robust and economically meaningful.
2. The stakeholder-distributed distress framework is conceptually interesting (though empirically incomplete).
3. The PHFSI index itself has potential policy value, even if not validated as a prediction tool.

**Required Revisions**:

1. **Validation or Reframing**:
   - Option A (Preferred): Obtain October 2024 capital injection data and conduct ROC analysis (PHFSI vs. Z-score).
   - Option B: Reframe the paper as "PHFSI Development and Descriptive Analysis" rather than "Validation."
   - Option C: Use alternative validation outcome (hospital closures, CEO turnover).

2. **Sequential Transfer Evidence**:
   - Either conduct lead-lag analysis (Granger causality tests) to verify temporal ordering, or
   - Acknowledge that the framework predicts sequential transfer but this hasn't been empirically established.

3. **Endogeneity Discussion**:
   - Add subsection explicitly discussing reverse causality concern (governments subsidize distressed hospitals).
   - Frame results as "correlational" or pursue IV strategy.

4. **ULS Reform Analysis**:
   - Remove from main contribution or clearly label as "preliminary descriptive evidence."

**Optional But Recommended**:

5. **Model Comparison**: Show PHFSI predictive power vs. simpler alternatives (Altman Z, leverage ratio, payment delays alone).

6. **Empirical Weighting**: Use factor analysis or PCA to derive data-driven component weights (move from appendix to main text).

With these revisions, this could be a strong paper for *Health Care Management Science*. The subsidy-moral hazard finding alone is publication-worthy in a health economics journal. However, **as currently written, it would not meet standards for a top-tier finance journal** (JF, JFE, RFS) due to the validation gap.

---

## COMPARISON TO RELATED LITERATURE

The paper positions itself relative to:
- **Altman (1968) / Ohlson (1980)**: Classic bankruptcy prediction. Fair comparison, but you don't actually *show* PHFSI outperforms these models.
- **Kornai (1986, 2003)**: Soft budget constraints. Excellent use of this literature.
- **Xanthakis et al. (2009)**: The motivating paper. You correctly identify their finding (Z-score fails for Greek public hospitals) but don't empirically verify your model succeeds where theirs failed.

Missing comparisons:
- **Recent distress prediction**: Bauer & Agarwal (2014), Barboza et al. (2017) use machine learning for bankruptcy prediction. Have these been applied to public sector?
- **Hospital financial distress**: Langabeer & Ozcan (2009) on hospital bankruptcy prediction, though this uses US private/nonprofit hospitals.
- **Government bailout literature**: Gropp et al. (2014) on bank bailouts could inform your bailout prediction framework.

---

## ADDITIONAL SUGGESTIONS

1. **Consider splitting into two papers**:
   - Paper 1: PHFSI development + subsidy-distress relationship + validation (pending data)
   - Paper 2: ULS reform evaluation (pending post-treatment data)

2. **Sharpen theoretical contribution**: The stakeholder-distributed distress framework is this paper's unique theoretical contribution. Consider developing it more formally (e.g., a simple model where stakeholders differ in exit costs and distress sequentially transfers from low-exit-cost [suppliers] to high-exit-cost [patients] stakeholders).

3. **Address "so what" question**: Why does it matter that subsidy dependence reduces PHFSI? From a welfare perspective, is this inefficient? Or is it optimal redistribution (government subsidizes hospitals serving poor patients, who have worse outcomes for reasons unrelated to hospital quality)?

---

**Reviewer Expertise**: Corporate finance, capital structure, financial distress and bankruptcy, empirical corporate finance

**Conflicts of Interest**: None

**Recommendation**: Major Revision → Conditional Accept (contingent on addressing validation issue)

**Timeline Estimate**: If authors obtain validation data quickly, this could be publishable within one revision cycle. If validation data remain unavailable, the paper needs substantial reframing.
