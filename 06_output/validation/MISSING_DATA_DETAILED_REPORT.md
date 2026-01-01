# Missing Data and Data Gaps Report
## Stakeholder-Distributed Distress: Measuring Financial Sustainability in Public Hospitals Under Soft Budget Constraints

**Author**: Daniel Polónia, Universidade de Aveiro
**Date**: December 31, 2025
**Purpose**: Comprehensive documentation of all missing data identified through peer review process

---

## EXECUTIVE SUMMARY

This report identifies and prioritizes **seven critical data gaps** affecting manuscript completeness and validity. Three gaps are **publication blockers** (must be addressed before submission), two are **major limitations** (require explicit discussion), and two are **desirable enhancements** (would strengthen but not essential).

### Priority Classification

| Priority | Count | Impact on Publication |
|----------|-------|----------------------|
| **CRITICAL** (Publication Blockers) | 3 | Cannot publish without addressing |
| **MAJOR** (Significant Limitations) | 2 | Can publish with explicit acknowledgment |
| **DESIRABLE** (Enhancements) | 2 | Would strengthen, optional |

---

## PART 1: CRITICAL DATA GAPS (Publication Blockers)

### Gap 1.1: October 2024 Capital Injection Micro-Data

**Status**: ❌ MISSING - PUBLICATION BLOCKER
**Priority**: CRITICAL
**Impact**: Fatal flaw - undermines entire PHFSI validation claim

#### What's Missing

**Specific Data Needed**:
```
Required Variables:
- Hospital entity name/ID (149 entities)
- Capital injection amount (€, individual allocation)
- Allocation date (month/day in October 2024)
- Allocation criteria (if documented)
- Total allocation: €500 million across 44 hospitals

Example Record:
| Entity Name | Entity_ID | Allocation_EUR | Date | Notes |
|-------------|-----------|----------------|------|-------|
| Hospital X  | HXXX      | 25,000,000     | 2024-10-15 | Initial bailout |
| Hospital Y  | HYYY      | 72,000,000     | 2024-10-22 | Large distressed |
```

**Current Status**:
- **Aggregate data available**: Ministry of Finance Decree 145/2024 states €500M total allocation
- **Micro-data unavailable**: Individual hospital allocations not publicly disclosed
- **Mentioned in manuscript**: Introduction claims PHFSI predicts this intervention, but no validation provided

#### Why It's Critical

**Peer Reviewer Comments**:

> **Healthcare Economist**: "This is a publication blocker. The entire contribution rests on PHFSI's predictive validity, yet the authors lack the validation outcome. Either (a) obtain Ministry of Finance data before submission, or (b) reframe H2 as a research agenda item."

> **Corporate Finance Scholar**: "This is like developing a credit scoring model and publishing it without ever testing whether it predicts default better than FICO scores. In any top finance journal (JF, JFE, RFS), this would be grounds for immediate rejection."

**Hypothesis at Risk**:
- **H2**: "PHFSI predicts government intervention better than Altman Z-score"
- **Cannot be tested** without outcome data
- Introduction claims AUC = 0.73 for PHFSI vs. 0.52 for Z-score, but this is never demonstrated

#### How to Obtain

**Option 1: Freedom of Information Request (PREFERRED)**

**Action Steps**:
1. Submit formal request to Portuguese Ministry of Finance (Ministério das Finanças)
   - **Legal basis**: Lei n.º 26/2016 (Access to Administrative Documents)
   - **Cite**: Academic research purpose, public interest

2. **Request Template**:
```
Subject: Freedom of Information Request - October 2024 SNS Capital Injection Data

To: Ministério das Finanças, Gabinete de Acesso à Informação

I am writing to request access to administrative documents under Lei n.º 26/2016
regarding the October 2024 capital injections to SNS hospital entities (Decree 145/2024).

Specific data requested:
1. Hospital entity name and identification code for each recipient
2. Individual capital allocation amount (€) for each recipient
3. Date of allocation/transfer for each recipient
4. Total number of recipient entities

Purpose: Academic research on public hospital financial sustainability for PhD dissertation
at Universidade de Aveiro. Research will contribute to health policy evaluation and
healthcare financing literature.

I understand the response deadline is 10 working days under Article 13 of Lei n.º 26/2016,
with possible extension to 20 working days if complexity requires.

Contact: Daniel Polónia, dpolonia@ua.pt, Universidade de Aveiro
```

3. **Send to**:
   - Email: geral@gm.mfin.gov.pt
   - Postal: Avenida Infante Dom Henrique, 1, 1149-009 Lisboa
   - Portal: https://www.portugal.gov.pt/pt/gc23/area-de-governo/financas

4. **Expected Timeline**:
   - Initial response: 10 working days (2 weeks)
   - Extension possible: Up to 20 working days (4 weeks)
   - Appeal if denied: 20 working days to Comissão de Acesso aos Documentos Administrativos (CADA)

**Option 2: Direct Contact with ACSS**

**Action Steps**:
1. Contact Administração Central do Sistema de Saúde (ACSS) - SNS financial authority
   - Email: geral@acss.min-saude.pt
   - Request as research collaboration rather than FOI

2. Leverage existing data relationship:
   - Already using ACSS Transparency Portal data
   - Frame as extension of publicly available datasets
   - Offer to share research findings with ACSS

**Option 3: Media/Parliamentary Sources**

**Action Steps**:
1. Search Portuguese parliamentary records (Assembleia da República)
   - Budget committee discussions may have hospital-level detail
   - Parliamentary questions about allocation criteria

2. Investigate media coverage:
   - Portuguese newspapers may have obtained/reported individual allocations
   - Healthcare trade publications (e.g., Jornal Médico, Revista Hospitalidade)

**Option 4: Alternative Validation Outcomes**

If capital injection data remains unavailable, use alternative outcomes:

**A. Hospital Closures/Restructuring (2017-2024)**:
```
Required Data:
- Hospital closure dates
- Merger/acquisition events
- Service line closures
- Emergency department shutdowns

Source: ACSS official announcements, hospital annual reports
```

**B. CEO/Director Turnover**:
```
Required Data:
- Hospital director appointment dates
- Director resignation/termination dates
- Reason for departure (if documented)

Source: Annual reports, hospital board meeting minutes, government gazettes
```

**C. Regulatory Interventions**:
```
Required Data:
- ACSS oversight actions (audits, performance reviews)
- Ministry of Health interventions
- Binding performance improvement plans
- External management appointments

Source: ACSS regulatory database, Ministry of Health announcements
```

**D. Credit Rating Downgrades** (if applicable):
```
Required Data:
- Hospital/SNS credit ratings (Moody's, S&P, Fitch)
- Rating change dates
- Rating justifications

Source: Rating agency reports (may be behind paywall)
```

#### Impact on Manuscript

**If Data Obtained**:
- ✅ Conduct full ROC analysis (PHFSI vs. Z-score)
- ✅ Calculate AUC with DeLong test for statistical significance
- ✅ Determine optimal PHFSI cutoff (Youden's J-statistic)
- ✅ Report sensitivity, specificity, precision at various thresholds
- ✅ Validate AUC = 0.73 claim in introduction
- ✅ Strengthen H2 from "PHFSI should predict" to "PHFSI does predict"

**If Data Not Obtained**:
- ⚠️ Must reframe H2 entirely:
  - Change from "PHFSI predicts intervention" to "PHFSI discriminates distress levels"
  - Use Table 2 (Distressed vs. Self-Sustaining comparison) as validation
  - Remove AUC claim from introduction
  - Add limitation: "Formal validation against government intervention outcomes awaits data availability"
- ⚠️ Acknowledge in Discussion: "Key limitation is inability to test predictive validity for bailout decisions"

---

### Gap 1.2: CQMI Component (Clinical Quality Maintenance Index)

**Status**: ❌ COMPLETELY MISSING - PUBLICATION BLOCKER
**Priority**: CRITICAL
**Impact**: One of five PHFSI components absent, creates methodological inconsistency

#### What's Missing

**Specific Data Needed**:

**Option A: Patient Safety Indicators (Preferred)**
```
Required Variables (by hospital-year):
- In-hospital mortality rate (age-adjusted)
- 30-day readmission rate (all-cause)
- Hospital-acquired infection rate
- Adverse event rate (if available)
- Patient safety incidents (reported)

Time Period: 2017-2024
Granularity: Annual or monthly
Source: SNS quality monitoring databases
```

**Option B: Clinical Outcomes (Alternative)**
```
Required Variables (by hospital-year):
- Hip fracture surgery within 48 hours (%)
- Stroke mortality rate (age-standardized)
- AMI (heart attack) mortality rate
- Cesarean section rate
- Average length of stay (ALOS) by DRG

Source: Already partially available in existing data
(morbilidade-mortalidade-hospitalar dataset)
```

**Option C: Minimum Viable CQMI**
```
Single Most Important Metric:
- Risk-adjusted in-hospital mortality rate by NUTS 2 region

Calculation:
CQMI_it = 1 - [(Mortality_it - Regional_Mean_t) / Regional_SD_t]

Normalization ensures cross-region comparability
Higher score = better quality maintenance
```

#### Current Problem: Entity Name Mismatch

**Root Cause**:
```
Pre-2024 Financial Data:        Quality Data (All Years):
"Centro Hospitalar Médio Ave"   "Unidade Local de Saúde do Ave"
"Centro Hospitalar Médio Tejo"  "Unidade Local de Saúde do Médio Tejo"
[44 entities renamed in 2024]   [Quality databases updated to new names]

Result: Cannot match pre-2024 financial data to quality data
```

**Why This Matters**:
- PHFSI is supposed to capture 5 dimensions of distress
- Quality deterioration is key theoretical prediction (stakeholder-distributed distress framework)
- Without CQMI, PHFSI only measures financial stress, not patient impact
- Creates inconsistency: 5-component framework → 4-component implementation

#### How to Obtain

**Solution 1: Create Entity Name Mapping (RECOMMENDED)**

**Technical Approach**:
```python
# Step 1: Extract geographic identifiers from entity names
financial_names = [
    "Centro Hospitalar Médio Ave, E.P.E.",
    "Centro Hospitalar Médio Tejo, EPE",
    # ... 44 entities
]

quality_names = [
    "UNIDADE LOCAL DE SAÚDE DO AVE, EPE",
    "UNIDADE LOCAL DE SAÚDE DO MÉDIO TEJO, EPE",
    # ... 48 entities
]

# Step 2: Fuzzy matching algorithm
import difflib

def match_entities(fin_name, qual_names):
    # Extract geographic keyword (e.g., "Médio Ave", "Médio Tejo")
    geographic = extract_location(fin_name)

    # Find best match in quality names
    matches = difflib.get_close_matches(geographic, qual_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Step 3: Manual validation
mapping = create_automated_mapping(financial_names, quality_names)
manually_verify_mapping(mapping)  # Human review of ambiguous cases
```

**Action Steps**:
1. **Week 1**: Extract all unique entity names from:
   - Financial data (2017-2024): `hospital_year_panel.parquet`
   - Quality data (2017-2024): `morbilidade-mortalidade-hospitalar.parquet`

2. **Week 1-2**: Develop fuzzy matching algorithm:
   - Use geographic keywords (e.g., "Ave", "Tejo", "Porto", "Lisboa")
   - Cross-reference with ACSS official hospital registry
   - Validate against known hospital locations (NUTS 2 regions)

3. **Week 2**: Manual review of ambiguous matches:
   - Create spreadsheet with automated matches
   - Flag low-confidence matches (similarity < 0.8)
   - Verify using hospital websites, Google Maps, ACSS directory

4. **Week 2-3**: Implement mapping:
   - Create `entity_name_crosswalk.csv`:
     ```
     financial_name,quality_name,confidence,notes
     "Centro Hospitalar Médio Ave, EPE","ULS DO AVE",0.95,"Geographic match"
     "Centro Hospitalar Médio Tejo, EPE","ULS DO MÉDIO TEJO",0.92,"Geographic match"
     ```
   - Update `phfsi_calculator.py` to use crosswalk
   - Recalculate PHFSI with all 5 components

**Estimated Effort**: 2-3 weeks programming + validation

**Solution 2: Use Institutional Identifiers (If Available)**

**Check for**:
- **ACSS Entity Code** (Código da Entidade): Stable identifier across name changes
- **Tax ID** (NIPC - Número de Identificação de Pessoa Coletiva): Never changes
- **Ministry of Health ID**: Internal SNS identifier

**Action**:
1. Check if quality datasets include institutional codes (not just names)
2. If yes, merge on codes instead of names (immediate solution)
3. Contact ACSS to request crosswalk file if codes not in public data

**Solution 3: Limit Analysis to Pre-2024 (FALLBACK)**

If mapping proves infeasible:
1. **Restrict sample to 2017-2023** (before name changes)
2. Calculate 5-component PHFSI for 2017-2023
3. Explicitly note 2024 limitation in methods:
   > "CQMI is available for 2017-2023 but unavailable for 2024 due to entity name changes during ULS integration. Analysis of 2024 uses 4-component PHFSI (OSSR, SPI, LRR, TLR)."

**Solution 4: Alternative Quality Proxy (LAST RESORT)**

If clinical quality data truly unavailable, use **process quality** proxy:
```
Alternative CQMI Metrics:
1. Average length of stay (ALOS) - available in activity data
   - Shorter ALOS suggests efficiency (good) but may indicate premature discharge (bad)
   - Requires risk adjustment

2. Bed occupancy rate - available
   - Very high (>95%) suggests overcrowding (bad for quality)
   - Very low (<60%) suggests underutilization (financial stress)

3. Emergency department wait times - if available
   - Longer waits = quality deterioration under financial stress
```

**Not ideal but defensible as financial stress → quality proxy**

#### Impact on Manuscript

**If CQMI Integrated**:
- ✅ Full 5-component PHFSI as theoretically specified
- ✅ Can test quality deterioration prediction (Theory Section 2.2)
- ✅ Stronger stakeholder-distributed distress evidence
- ✅ Component correlation matrix includes all 5 dimensions

**If CQMI Remains Missing**:
- ⚠️ Must explicitly acknowledge in Methods (Section 3.3):
  > "Due to entity name changes during 2024 ULS integration, the Clinical Quality Maintenance Index (CQMI) component could not be calculated for the full sample period. PHFSI in this study comprises four components: OSSR, SPI, LRR, and TLR. Future work will complete entity mapping to enable full 5-component analysis."
- ⚠️ Add to Discussion limitations (Section 5.4)
- ⚠️ Cannot claim to fully measure "stakeholder-distributed distress" if patient quality dimension is absent
- ⚠️ Weakens theoretical contribution (framework predicts quality deterioration but can't test it)

---

### Gap 1.3: Post-2024 ULS Integration Data

**Status**: ❌ MISSING - PUBLICATION BLOCKER (for H3)
**Priority**: CRITICAL (for ULS reform analysis only)
**Impact**: Cannot conduct proper DiD analysis, H3 is untestable

#### What's Missing

**Specific Data Needed**:

**Post-Reform Observations (2024 Q4 - 2025)**:
```
Required Variables:
- All PHFSI component data for 2024-2025 (same as 2017-2023)
- Entity names matched to pre-reform entities
- Integration dates (month/day each hospital joined ULS)
- Control group identification:
  - Which hospitals integrated in 2024?
  - Which hospitals integrated in 2025 (late adopters)?
  - Any hospitals not integrated (if exist)?

Minimum Viable Dataset for DiD:
- 2024 full-year data for treated hospitals (integrated 2024)
- 2024 full-year data for control hospitals (integrated 2025+)
- At least 6-12 months post-integration to observe effects
```

**Treatment Timing Variation**:
```
Currently: "43 of 44 hospitals integrated in 2024" (nearly simultaneous)

Ideal for DiD: Staggered adoption
- Early adopters: Jan-Jun 2024 (n = 15)
- Middle adopters: Jul-Dec 2024 (n = 15)
- Late adopters: 2025 (n = 14)
- Never treated: (n = 0, unfortunately)

Problem: With simultaneous treatment, traditional DiD is infeasible
```

#### Current Problem: No Post-Reform Data

**What We Have**:
- ✅ Pre-reform trends: 2017-2023 PHFSI trajectories for reform hospitals
- ✅ Reform identification: 45 "Centro Hospitalar" entities underwent ULS integration in 2024
- ✅ 2023 PHFSI improvement: 0.378 vs. 2022: 0.334 (p = 0.041)

**What We Don't Have**:
- ❌ 2024 PHFSI scores for integrated hospitals (entity name mismatch)
- ❌ 2025 data (doesn't exist yet - it's only December 2025)
- ❌ Control group (almost all hospitals treated simultaneously)

#### Why It's Critical

**Peer Reviewer Comments**:

> **Healthcare Economist**: "H3 (ULS integration improves sustainability) is tested only via event study (2017-2023), with no post-reform data. The 2023 PHFSI improvement could reflect anticipatory effects, selection bias, preparation funding, or regression to the mean. Without post-2024 data, this analysis adds little beyond descriptive trends."

> **Corporate Finance Scholar**: "The 'event study' shows only pre-reform trends; no post-reform data exist. Without control group and post-treatment data, this analysis is uninformative. Recommendation: Remove H3 entirely or relegate to brief appendix."

**Hypothesis at Risk**:
- **H3**: "ULS integration improves financial sustainability"
- **Current evidence**: Pre-trends only (2017-2023)
- **Needed for causal inference**: Parallel trends + post-treatment effects

#### How to Obtain

**Solution 1: Wait for 2025 Data (RECOMMENDED)**

**Timeline**:
```
Dec 2025 (Now):    2025 data doesn't exist yet
Jan-Mar 2026:      SNS hospitals report Q4 2024 data
Apr-Jun 2026:      ACSS publishes 2024 annual data
Jul-Dec 2026:      2025 data collection begins
Jan-Mar 2027:      2025 annual data becomes available

Earliest Full DiD: Mid-2026 (2024 data) to Early 2027 (2024-2025 data)
```

**Recommendation**:
1. **Current paper (submit early 2026)**:
   - Remove H3 from main contribution
   - Focus on H1 (subsidy-distress) and H2 (PHFSI validation)
   - Mention ULS reform as "future research" in conclusion

2. **Follow-up paper (2027)**:
   - Dedicated ULS reform evaluation study
   - Full DiD with 2024-2025 post-reform data
   - Compare early vs. late adopters (if timing variation exists)

**Solution 2: Immediate Partial Analysis (2024 Q1-Q3)**

If 2024 partial data available:
```
Action:
1. Request 2024 Q1-Q3 data from ACSS (may be available internally)
2. Analyze first 3-9 months post-integration
3. Frame as "short-term effects" analysis

Limitation:
- Insufficient time to observe sustained effects
- Integration may take 6-12 months to stabilize
- Results would be preliminary
```

**Solution 3: Solve Entity Name Mapping (Enables 2024 Data Use)**

Same as Gap 1.2 solution:
- Create crosswalk: "Centro Hospitalar X" → "ULS Y"
- Merge 2024 financial data (new names) to 2017-2023 data (old names)
- This enables at least 1 post-reform year (2024)

**One post-reform year is weak but better than zero:**
```
DiD Specification with Single Post Period:
PHFSI_it = β0 + β1*(Treated × Post2024) + β2*Treated + β3*Post2024 +
           Hospital_FE + ε_it

Where:
- Treated = 1 if integrated in 2024, 0 if never integrated or 2025+
- Post2024 = 1 if year ≥ 2024, 0 otherwise

Problem: With only 1 post-period, can't test dynamic effects or persistence
```

**Solution 4: Alternative Identification Strategy**

**Regression Discontinuity Design (RDD)**:
```
If ULS integration had eligibility threshold:
- E.g., "Hospitals with debt > €X million integrate first"
- E.g., "Hospitals in regions with population < Y integrate first"

Action:
1. Investigate ULS integration criteria (ACSS documents, government decrees)
2. If threshold exists, use RDD:
   - Compare hospitals just above vs. just below threshold
   - Bandwidth: Hospitals within ±10% of threshold

Requires: Documentation of integration selection criteria
```

**Instrumental Variables (IV)**:
```
If political factors drove integration timing:
- E.g., "Hospitals in regions aligned with ruling party integrated first"
- E.g., "Hospitals with newer facilities integrated first"

Instrument: Political alignment or facility age
First Stage: Instrument → Integration probability
Second Stage: Integration → PHFSI

Requires: Exogenous variation in integration timing
```

#### Impact on Manuscript

**If Post-2024 Data Obtained (2026-2027)**:
- ✅ Full DiD analysis with treatment and control groups
- ✅ Event study plot showing pre-trends + post-effects
- ✅ Test H3 properly: "ULS integration improves PHFSI by X points"
- ✅ Mechanism tests: Which PHFSI components improved most?
- ✅ Heterogeneity analysis: Did reform affect large vs. small hospitals differently?

**If Post-2024 Data Unavailable (Current Situation)**:
- ⚠️ **MUST REMOVE H3 from main manuscript**
- ⚠️ Options:
  1. **Preferred**: Relegate to appendix titled "Preliminary Descriptive Evidence on ULS Reform"
  2. **Alternative**: Remove entirely, defer to follow-up paper
- ⚠️ In Conclusion, note: "Evaluation of 2024 ULS integration reform awaits availability of post-reform data (2025+)"
- ⚠️ Cannot claim reform "improves" sustainability - only show pre-reform trends

---

## PART 2: MAJOR DATA LIMITATIONS (Require Explicit Discussion)

### Gap 2.1: Governance Data

**Status**: ⚠️ MISSING - MAJOR LIMITATION
**Priority**: MAJOR (acknowledged by authors, not publication blocker)
**Impact**: Cannot test governance heterogeneity, missing variable bias concern

#### What's Missing

**Board Composition Data**:
```
Required Variables (by hospital-year):
- Board size (number of members)
- Board composition:
  - Number of physicians on board
  - Number of external/independent directors
  - Number of financial experts
  - Number of political appointees
- Board chair credentials (medical vs. administrative background)
- Board meeting frequency
- Board compensation structure

Time Period: 2017-2024
Source: Hospital annual reports, Ministry of Health appointments
```

**CEO/Director Characteristics**:
```
Required Variables (by hospital-year):
- CEO name (for tracking turnover)
- CEO tenure (years in position)
- CEO background:
  - Medical degree (MD)?
  - MBA or management degree?
  - Prior hospital management experience?
  - Political affiliation (if identifiable)
- CEO compensation (fixed + variable)
- CEO performance metrics/incentives

Source: Hospital annual reports, board meeting minutes, government gazettes
```

**Hospital-Level Governance Indicators**:
```
Required Variables (by hospital):
- University hospital affiliation (Y/N) - HAVE THIS
- Teaching hospital status - partially available
- Research intensity (publications, clinical trials)
- Accreditation status (JCI, ISO, national certifications)
- Management system (autonomous, integrated, EPE status)
```

#### Current Proxy Variables Available

**What We Have**:
```
University Hospital Indicator:
- Binary variable: 1 if "Universitário" in hospital name, 0 otherwise
- Used in Table 3, Column 3 governance heterogeneity analysis
- Shows STRONGER subsidy moral hazard in university hospitals (β = -0.089, p = 0.058)

Hospital Size:
- Log(Operating Revenue) as size proxy
- Could proxy for governance sophistication (larger = more professional management)

Large Hospital Indicator:
- Top quartile by revenue
- Mentioned in methods but results not reported
```

**What's Missing**:
- Actual governance quality measures
- Managerial ability/talent indicators
- Board structure and composition
- CEO incentive alignment

#### Why It Matters

**Peer Reviewer Comments**:

> **Healthcare Economist**: "Governance Data Unavailable: Soft budget constraint theory predicts that managerial quality and board governance moderate subsidy-induced moral hazard, but Portuguese administrative data lack governance indicators. Our university hospital proxy is crude, capturing affiliation but not board composition, CEO tenure, or incentive structures."

> **Corporate Finance Scholar**: "Missing Variable Bias: Hospital governance (board composition, CEO tenure, managerial ability) is unobserved. This is a first-order determinant of financial performance. If better-governed hospitals receive fewer subsidies (because they're more self-sufficient), the subsidy-distress coefficient would be downward biased. Conversely, if worse-governed hospitals receive more subsidies (political capture), the coefficient would be upward biased."

**Theoretical Predictions**:
1. Better governance → Less subsidy dependence (self-sufficiency)
2. Better governance → Higher PHFSI (efficient management)
3. Better governance → Weaker subsidy-distress relationship (moral hazard mitigated)

**Cannot test these predictions without governance data**

#### How to Obtain

**Solution 1: Primary Data Collection via Survey (LONG-TERM)**

**Survey Design**:
```
Target Respondents:
- Hospital CEOs/Directors (n = 149)
- Board chairs (n = 149)
- CFOs (n = 149)

Survey Modules:
1. Board Composition (10 questions)
   - Board size, composition, meeting frequency
   - Director backgrounds, independence

2. CEO Characteristics (8 questions)
   - Tenure, background, compensation structure
   - Performance metrics, autonomy

3. Management Systems (12 questions)
   - Strategic planning processes
   - Financial control systems
   - Performance monitoring

4. Hospital Culture (10 questions)
   - Innovation orientation
   - Risk tolerance
   - Patient-centeredness

Survey Length: 40 questions, 15-20 minutes
Response Rate Target: 50-60% (n = 75-90)
```

**Action Steps**:
1. **Design survey instrument** (2-3 weeks)
   - Adapt validated governance scales (e.g., Bloom et al. 2020 management practices)
   - Pilot test with 3-5 hospital managers

2. **Obtain ethics approval** (4-6 weeks)
   - Submit to Universidade de Aveiro ethics committee
   - Prepare informed consent, data protection documents

3. **Distribute survey** (8-12 weeks)
   - Email invitation to all 149 hospital CEOs
   - Follow-up reminders (2 weeks, 4 weeks)
   - Phone calls for non-respondents

4. **Analyze results** (2-3 weeks)
   - Link survey data to financial panel
   - Test governance heterogeneity hypotheses

**Total Timeline**: 6-9 months
**Cost**: Minimal (survey software, research assistant time)
**Feasibility**: High, but outside current paper timeline

**Recommendation for Current Paper**:
- Acknowledge as limitation, defer to follow-up study
- In proposal/acknowledgments, note: "Governance survey planned for 2026"

**Solution 2: Secondary Data from Annual Reports (MEDIUM-TERM)**

**Data Extraction Plan**:
```
Source: Hospital annual reports (Relatórios e Contas Anuais)
- Available on individual hospital websites
- Required by ACSS since 2015
- Vary in detail and standardization

Information Typically Included:
✓ Board member names and titles
✓ CEO name and appointment date
✓ Organizational structure diagrams
✓ Financial statements (already have)
✓ Strategic priorities and goals
✗ Board meeting frequency (rarely reported)
✗ Director compensation (sometimes reported)
✗ CEO performance metrics (rarely reported)
```

**Action Steps**:
1. **Compile annual reports** (2-3 weeks)
   - Download PDFs for 149 hospitals × 8 years = 1,192 documents
   - Organize by hospital and year

2. **Manual coding** (4-6 weeks)
   - Extract board member names, count size
   - Code CEO changes (turnover indicator)
   - Identify physician vs. administrative backgrounds (LinkedIn, CVs)

3. **Create governance dataset** (1 week)
   - Merge coded variables to panel
   - Validate for consistency

**Variables Obtainable**:
- ✅ Board size (reliable)
- ✅ CEO turnover (reliable)
- ✅ Physician-CEO indicator (mostly reliable via LinkedIn)
- ⚠️ Board composition (partial - names available but backgrounds require research)
- ❌ Compensation, incentives (rarely disclosed)

**Total Timeline**: 2-3 months
**Cost**: Low (research assistant time for coding)
**Feasibility**: High

**Recommendation**:
- Could be done for revised manuscript if reviewers request it
- At minimum, extract CEO turnover and board size (relatively easy)

**Solution 3: Proxy Variables from Existing Data (IMMEDIATE)**

**Additional Proxies to Extract**:

**A. Hospital Complexity (Research Intensity Proxy)**:
```python
# From activity data already collected
research_intensity = {
    'teaching_beds_pct': teaching_beds / total_beds,
    'specialty_diversity': number_of_specialty_departments,
    'avg_case_complexity': mean_drg_weight,
    'icu_capacity': icu_beds / total_beds
}

Hypothesis: Higher complexity → better management → higher PHFSI
```

**B. External Recognition (Quality Proxy)**:
```python
# Can be manually collected
accreditation = {
    'jci_accredited': 1/0,  # Joint Commission International
    'iso_certified': 1/0,   # ISO 9001
    'national_awards': count_awards,
    'research_grants': 1/0 if receives_competitive_grants
}

Hypothesis: Accreditation signals governance quality
```

**C. Financial Autonomy Level**:
```python
# From legal status (can be coded from entity type)
autonomy_level = {
    'EPE': 3,  # Entidade Pública Empresarial (most autonomous)
    'SPA': 2,  # Sector Público Administrativo (medium)
    'IPO': 1   # Instituto Português Oncologia (specialized)
}

Hypothesis: More autonomy → better governance → higher PHFSI
```

**D. Geographic Competition Intensity**:
```python
# Calculate using hospital locations + population data
competition = {
    'hospitals_within_50km': count_nearby_hospitals,
    'market_concentration': hhi_index,
    'patient_choice_availability': 1/0
}

Hypothesis: Competition disciplines management
```

**Total Timeline**: 1-2 weeks
**Feasibility**: Very High - uses existing or easily obtainable data

**Recommendation for Current Paper**:
- Use available proxies (university status, size, complexity, autonomy)
- Run heterogeneity analysis by these dimensions
- Explicitly acknowledge: "Detailed governance data (board composition, CEO incentives) unavailable"

#### Impact on Manuscript

**If Governance Data Obtained**:
- ✅ Test moderating effects: Does governance weaken subsidy-moral hazard?
- ✅ Address missing variable bias concern
- ✅ Heterogeneity analysis more nuanced
- ✅ Stronger theoretical contribution (governance mechanisms)

**If Governance Data Unavailable (Current State)**:
- ⚠️ Add explicit limitation in Discussion (Section 5.4):
  > "A key limitation is absence of governance data. Hospital board composition, CEO tenure, and managerial incentive structures likely moderate the subsidy-distress relationship but could not be tested with available administrative data. The university hospital proxy is crude and captures only institutional affiliation, not governance quality. Future research should collect primary governance data via surveys or annual report coding."
- ⚠️ Acknowledge potential missing variable bias:
  > "If better-governed hospitals receive fewer subsidies (due to greater self-sufficiency), our subsidy-distress coefficient may understate the true moral hazard effect. Conversely, if political factors lead worse-governed hospitals to receive more subsidies, the coefficient may be upward biased. The fixed effects specification controls for time-invariant governance quality but not time-varying changes."
- ✅ Still publishable - reviewers acknowledge this is common limitation in administrative data studies

---

### Gap 2.2: Monthly Time-Series Data

**Status**: ⚠️ ANNUAL DATA ONLY - MAJOR LIMITATION
**Priority**: MAJOR (needed to test sequential transfer mechanism)
**Impact**: Cannot test temporal ordering of distress symptoms

#### What's Missing

**High-Frequency Financial Data**:
```
Currently Have: Annual observations (8 data points per hospital)
Years: 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024

Need: Monthly observations (96 data points per hospital)
Months: Jan 2017 - Dec 2024 (96 months)

Variables Required (monthly):
- Operating revenues (€)
- Operating expenses (€)
- Cash receipts from government
- Supplier payments made
- Outstanding supplier debt
- Overdue debt amount
- Payment delays (days)
- Staff count (FTEs)
- Patient admissions
- Emergency visits
- Mortality incidents
```

**High-Frequency Quality Data**:
```
Need: Monthly or quarterly quality metrics
- In-hospital mortality (monthly aggregates)
- Adverse events (reported monthly)
- Patient complaints (monthly)
- ER wait times (monthly averages)
- Bed occupancy rates (monthly)
```

#### Current Data Granularity

**What We Have**:
```
SNS Transparency Portal Data:
- Originally collected: MONTHLY (Jan 2017 - Dec 2024)
- Our processing: Aggregated to ANNUAL in create_panel_dataset.py

Current Code (Line 45-60 of create_panel_dataset.py):
```python
# Aggregate monthly to annual
annual_data = monthly_data.groupby(['entidade', 'year']).agg({
    'rendimentos_operacionais': 'sum',
    'gastos_operacionais': 'sum',
    'divida_total_fornecedores_externos': 'mean',  # Average over year
    'pagamentos_em_atraso': 'mean'                 # Average over year
}).reset_index()
```

**So monthly data EXISTS in raw files - we just aggregated it!**

#### Why It Matters

**Peer Reviewer Comments**:

> **Corporate Finance Scholar**: "The framework's key prediction is that distress transfers sequentially: suppliers → staff → patients → taxpayers. This implies testable lead-lag relationships. Payment delays at t should predict staff turnover at t+1. None of these predictions are tested. The mechanism tests just show cross-sectional correlations, not temporal ordering. Granger causality tests would address this."

**Sequential Transfer Predictions to Test**:
1. **Payment delays → Staff turnover** (lag: 3-6 months)
   - Hypothesis: As payment delays worsen, staff quit due to deteriorating work conditions

2. **Staff turnover → Quality decline** (lag: 3-6 months)
   - Hypothesis: Staff shortages lead to errors, longer wait times, worse outcomes

3. **Quality decline → Government intervention** (lag: 6-12 months)
   - Hypothesis: Patient complaints trigger political pressure → bailouts

**Current Analysis**: Only shows these variables are correlated, not sequentially ordered

#### How to Obtain

**Solution 1: Use Existing Monthly Data (IMMEDIATE)**

**Action**:
1. **Modify create_panel_dataset.py**:
   ```python
   # Instead of aggregating to annual, keep monthly
   monthly_panel = monthly_data.copy()
   monthly_panel['month'] = pd.to_datetime(monthly_panel['date']).dt.to_period('M')

   # Set index to (entity, month)
   monthly_panel = monthly_panel.set_index(['entidade', 'month'])

   # Save as monthly panel
   monthly_panel.to_parquet('hospital_month_panel.parquet')
   ```

2. **Advantages**:
   - ✅ Data already exists in raw files
   - ✅ No additional data collection needed
   - ✅ Can immediately run lead-lag analysis

3. **Challenges**:
   - ⚠️ Some variables may have missing months (not all hospitals report monthly)
   - ⚠️ Seasonal patterns need to be addressed (e.g., flu season)
   - ⚠️ More complex econometric models (need to account for autocorrelation)

**Total Timeline**: 1 week to restructure data, 1-2 weeks to run analysis
**Feasibility**: VERY HIGH - data exists

**Solution 2: Lead-Lag Analysis with Monthly Data**

**Granger Causality Tests**:
```python
from statsmodels.tsa.stattools import grangercausalitytests

# Test: Do payment delays Granger-cause quality decline?
# Null hypothesis: Payment delays do NOT help predict future quality

data_for_granger = monthly_panel[['pagamentos_em_atraso', 'mortality_rate']].dropna()

# Test lags 1-6 months
results = grangercausalitytests(data_for_granger, maxlag=6)

# Interpretation:
# If p < 0.05 at lag 3, then payment delays at t predict mortality at t+3
# This supports sequential transfer mechanism
```

**Panel VAR (Vector Autoregression)**:
```python
from linearmodels.panel import PanelVAR

# Specify system of equations
# Payment_Delays_t = α1 + β1*Payment_Delays_t-1 + γ1*Quality_t-1 + ε1_t
# Quality_t = α2 + β2*Payment_Delays_t-1 + γ2*Quality_t-1 + ε2_t

model = PanelVAR(monthly_panel[['pagamentos_em_atraso', 'mortality_rate']],
                  lags=3,
                  entity_effects=True)
results = model.fit()

# Impulse response functions
# How does a shock to payment delays affect quality 1, 2, 3 months later?
```

**Expected Results**:
- Payment delays → Quality decline (3-6 month lag)
- Quality decline → Government intervention (6-12 month lag)
- Confirms sequential transfer mechanism

**Total Timeline**: 2-3 weeks for analysis
**Feasibility**: HIGH if monthly data quality is good

#### Impact on Manuscript

**If Monthly Analysis Conducted**:
- ✅ Strong evidence for sequential transfer mechanism (Theory Section 2.2)
- ✅ Granger causality tests show temporal ordering
- ✅ Impulse response functions visualize distress propagation
- ✅ Major strengthening of theoretical contribution
- ✅ New figure: "Dynamics of Distress Propagation"
- ✅ Addresses corporate finance reviewer's key criticism

**If Remain with Annual Data**:
- ⚠️ Must soften claims about "sequential" transfer in Theory section:
  > "The stakeholder-distributed distress framework predicts sequential transfer of costs, though empirical verification of temporal ordering requires higher-frequency data than the annual observations available in this study. We present evidence that distress symptoms co-occur (payment delays, quality decline, bailouts) but cannot establish definitive causal ordering."
- ⚠️ Add to Limitations (Section 5.4):
  > "Our annual data do not allow testing the predicted sequential transfer mechanism. Monthly data would enable Granger causality tests establishing whether payment delays temporally precede quality deterioration, which in turn precedes government intervention. This remains for future research."

---

## PART 3: DESIRABLE ENHANCEMENTS (Optional, Would Strengthen)

### Gap 3.1: Late Adopter Control Group for DiD

**Status**: ⚠️ WEAK CONTROL GROUP
**Priority**: DESIRABLE (would enable cleaner DiD)
**Impact**: Currently have simultaneous treatment (43/44 hospitals in 2024)

#### What's Missing

**Treatment Timing Variation**:
```
Ideal Staggered Adoption:
- Early: Jan-Mar 2024 (n = 15)
- Middle: Apr-Sep 2024 (n = 15)
- Late: Oct-Dec 2024 (n = 14)
- Control: Never treated or 2025+ (n = 15)

Actual (based on manuscript):
- Treated 2024: n = 43
- Treated 2025+: n = 1-2 (?)
- Never treated: n = 0

Problem: No meaningful control group
```

**Integration Date Details**:
```
Need for Each Hospital:
- Exact integration date (day/month/year)
- Pre-announcement date (when integration was announced)
- Preparation period (time between announcement and integration)
- Integration type (voluntary vs. mandated)

Currently: Only know "integrated in 2024" (annual granularity)
```

#### How to Obtain

**Solution 1: Extract from Government Decrees**

**Sources**:
1. **Diário da República** (Official Gazette):
   - Search for ULS creation decrees (2024)
   - Each decree specifies integration effective date

2. **ACSS Announcements**:
   - Ministry of Health press releases
   - ACSS regulatory notices

**Action Steps**:
```
1. Search Diário da República database
   - Keywords: "Unidade Local de Saúde", "ULS", "integração", "2024"
   - Filter: Decree type (Decreto-Lei, Portaria)

2. Extract for each hospital:
   - Decree number and date
   - Effective integration date
   - Entities merged (Centro Hospitalar X + Primary Care Y → ULS Z)

3. Create integration events dataset:
   hospital_name | decree_number | announcement_date | integration_date | lag_days
```

**Timeline**: 1-2 weeks (manual extraction from ~40-50 decrees)
**Feasibility**: HIGH - all decrees are publicly available

**Solution 2: Retrospective Definition of Control Group**

Even with simultaneous treatment, can create "synthetic control":
```
Counterfactual Control Group Options:

A. Hospitals Scheduled for 2025 Integration:
   - If any hospitals were originally planned for 2025 but not yet integrated
   - Use their 2024 data as "never treated" counterfactual

B. Never-Merged Hospitals:
   - Standalone hospitals or specialized facilities (e.g., IPO oncology institutes)
   - Not part of ULS integration wave
   - Use as permanent control group

C. Synthetic Control Method:
   - For each treated hospital, create weighted average of never-treated hospitals
   - Weights chosen to match pre-treatment PHFSI trends
   - Compare treated to synthetic control post-2024
```

#### Impact on Manuscript

**If Treatment Timing Variation Found**:
- ✅ Proper staggered DiD (Callaway & Sant'Anna 2021 methodology)
- ✅ Can estimate dynamic treatment effects
- ✅ Test for anticipatory effects (PHFSI changes before formal integration)
- ✅ Heterogeneity by integration timing

**If No Variation (Current State)**:
- ⚠️ Cannot use traditional DiD
- ⚠️ Must use alternative identification:
  - **Option 1**: Synthetic control method
  - **Option 2**: Before-after comparison with caveats
  - **Option 3**: Defer analysis entirely to future work
- ⚠️ Current manuscript choice: Event study (pre-trends only) + acknowledge limitation

---

### Gap 3.2: Supplier-Level Data for Monopsony Analysis

**Status**: ⚠️ NO SUPPLIER DATA
**Priority**: DESIRABLE (theoretical extension, not essential for current paper)
**Impact**: Cannot test monopsony power mechanism

#### What's Missing

**Supplier-Level Financial Data**:
```
Required:
- Supplier firm ID
- Amount owed by each hospital to each supplier (€)
- Payment terms (e.g., net 60 days)
- Actual payment delays (days overdue)
- Supplier financial statements:
  - Revenue
  - Accounts receivable
  - Profitability
  - Leverage
  - Bankruptcy filings (if any)

Example Record:
hospital_id | supplier_id | year | amount_owed | days_overdue | supplier_revenue | supplier_bankrupt
H001        | S123        | 2020 | 5000000     | 180          | 50000000         | 0
H001        | S123        | 2021 | 6500000     | 240          | 48000000         | 0
```

**Hospital-Supplier Network**:
```
Required:
- Which suppliers serve which hospitals
- Supplier concentration: Does hospital have alternative suppliers?
- Hospital concentration: Does supplier have alternative customers?
- Market power indicators:
  - Herfindahl-Hirschman Index (HHI) for suppliers
  - HHI for hospitals (from supplier perspective)
```

#### Why It Would Be Valuable

**Monopsony Power Hypothesis**:
```
Theory: Hospitals exploit market power over suppliers
- Suppliers depend on hospital contracts for revenue
- Hospitals delay payments knowing suppliers can't easily switch customers
- Suppliers absorb financing costs (implicit interest on delayed payments)

Test:
- Do hospitals with higher market concentration delay payments longer?
- Do payment delays predict supplier financial distress?
- Do suppliers to distressed hospitals have worse financial performance?
```

**Stakeholder Transfer Mechanism**:
```
Current Evidence: Hospitals delay supplier payments (198 days average)

Missing Evidence:
- Do suppliers bear real costs from these delays?
- Do suppliers raise prices to compensate (passing costs back)?
- Do suppliers exit market, reducing competition?
```

#### How to Obtain

**Option 1: Request from ACSS (Low Probability)**

ACSS may have:
- Hospital procurement data (supplier contracts)
- Accounts payable aging reports

Unlikely to be public due to:
- Commercial confidentiality
- Supplier privacy concerns

**Option 2: Match to Supplier Financial Statements**

Portuguese company financial data:
- **Source**: Sistema de Informação Empresarial Simplificada (IES)
- **Availability**: Annual reports for companies above certain revenue threshold
- **Coverage**: Publicly available for large suppliers (pharmaceutical companies, medical device manufacturers)

**Action**:
```
1. Identify major hospital suppliers:
   - Pharmaceutical companies (e.g., Roche, Novartis)
   - Medical device manufacturers
   - Service contractors (cleaning, catering, security)

2. Download supplier financial statements (2017-2024)

3. Check supplier notes for "accounts receivable aging"
   - Some firms disclose % receivables >90 days overdue
   - Can infer if this correlates with SNS payment delays

4. Create hospital-supplier matched dataset
```

**Timeline**: 2-3 months (data collection + matching)
**Feasibility**: MODERATE (public data exists but matching is non-trivial)

#### Impact on Manuscript

**If Supplier Data Obtained**:
- ✅ Major theoretical extension (monopsony power mechanism)
- ✅ Test supplier financial distress from hospital payment delays
- ✅ Stronger stakeholder-distributed distress evidence
- ✅ Potential for separate "Follow-Up Paper 3: Supplier-Level Analysis"

**If Supplier Data Not Obtained (Current State)**:
- ✅ No impact on current paper (not required)
- ⚠️ Mention in Discussion as "future research direction":
  > "A promising extension would link hospital payment delays to supplier financial outcomes. Do pharmaceutical companies and medical device manufacturers experience financial distress when serving chronically late-paying public hospitals? Investigating supplier-level impacts would complete the stakeholder-distributed distress chain."

---

## PART 4: DATA PRIORITIES AND ACTION PLAN

### Immediate Priority Ranking

| Gap | Data Type | Priority | Timeline | Feasibility | Impact if Obtained |
|-----|-----------|----------|----------|-------------|-------------------|
| **1.1** | Capital injection data | CRITICAL | 2-8 weeks | MEDIUM | Enables H2 validation |
| **1.2** | CQMI (entity mapping) | CRITICAL | 2-3 weeks | HIGH | Completes 5-component PHFSI |
| **1.3** | Post-2024 ULS data | CRITICAL | 6-18 months | LOW (doesn't exist yet) | Enables H3 testing |
| **2.1** | Governance data | MAJOR | 2-6 months | MEDIUM | Tests heterogeneity |
| **2.2** | Monthly time-series | MAJOR | 1 week | VERY HIGH | Tests sequential transfer |
| **3.1** | ULS timing variation | DESIRABLE | 1-2 weeks | HIGH | Better DiD identification |
| **3.2** | Supplier-level data | DESIRABLE | 2-3 months | MEDIUM | Monopsony analysis |

### Recommended Action Sequence

**Phase 1: Immediate (Weeks 1-4) - Enable Submission**

1. **Week 1: Fix CQMI**
   - Create entity name crosswalk
   - Recalculate PHFSI with 5 components
   - Regenerate all tables/figures
   - **Deliverable**: Complete 5-component PHFSI

2. **Week 2: Extract Monthly Data**
   - Modify create_panel_dataset.py to keep monthly granularity
   - Run Granger causality tests
   - Create impulse response figure
   - **Deliverable**: Sequential transfer evidence

3. **Week 3: File FOI Request**
   - Submit capital injection data request to Ministry of Finance
   - Parallel: Extract ULS integration dates from official gazettes
   - **Deliverable**: Data requests submitted

4. **Week 4: Reframe Manuscript**
   - Remove H3 from main text (move to appendix)
   - Update limitations section
   - Revise abstract and introduction
   - **Deliverable**: Revised draft v2.0

**Phase 2: Short-Term (Weeks 5-12) - Strengthen While Waiting**

5. **Weeks 5-6: Governance Proxies**
   - Extract board size and CEO turnover from annual reports (10 largest hospitals as pilot)
   - Calculate additional proxies (complexity, autonomy, accreditation)
   - Run heterogeneity analysis
   - **Deliverable**: Governance section enhancement

6. **Weeks 7-8: Internal Review**
   - Circulate revised draft to advisor
   - Share with 2-3 colleagues
   - Incorporate feedback
   - **Deliverable**: Revised draft v2.1

7. **Weeks 9-12: Wait for FOI Response**
   - Monitor FOI request status
   - If approved: Conduct ROC analysis (Week 11-12)
   - If denied: Finalize with reframed H2
   - **Deliverable**: Final validation status

**Phase 3: Medium-Term (Months 4-6) - Conditional on Data**

8. **If Capital Injection Data Obtained**:
   - Conduct full ROC validation
   - Compare PHFSI vs. Z-score
   - Update Results section
   - **Deliverable**: Validated prediction model
   - **Submit manuscript to HCMS**

9. **If Capital Injection Data NOT Obtained**:
   - Finalize with reframed H2 (discrimination vs. prediction)
   - Add explicit limitation
   - **Deliverable**: Best-effort manuscript
   - **Submit manuscript to HCMS**

**Phase 4: Long-Term (2026-2027) - Follow-Up Papers**

10. **2026 H1: Governance Survey**
    - Design and field governance survey
    - Collect board composition, CEO characteristics
    - **Deliverable**: Governance heterogeneity paper

11. **2026 H2-2027: ULS Reform Evaluation**
    - Wait for 2024-2025 annual data
    - Complete entity mapping if not yet done
    - Full DiD analysis
    - **Deliverable**: ULS reform evaluation paper

12. **2027: Supplier Analysis**
    - Match hospital data to supplier financials
    - Test monopsony power hypotheses
    - **Deliverable**: Supplier-level distress paper

---

## PART 5: REVISED MANUSCRIPT STRUCTURE

Given missing data realities, recommended manuscript structure:

### Current Paper (Submit 2026 Q1-Q2)

**Title**: Stakeholder-Distributed Distress: Subsidy Dependence and Financial Sustainability in Public Hospitals

**Focus**:
- **Primary**: H1 (Subsidy-distress relationship) ← ROBUST, PUBLICATION-WORTHY
- **Secondary**: H2 (PHFSI discrimination) ← Reframed from "prediction"
- **Removed**: H3 (ULS reform) ← Defer to follow-up

**Key Changes**:
1. Abstract emphasizes subsidy-moral hazard finding
2. Introduction removes AUC claim (unless validated)
3. Theory Section 2.2 softens "sequential" transfer claims
4. Methods Section 3.3 acknowledges CQMI limitation (if not fixed)
5. Results focuses on Table 3 (panel regressions)
6. Discussion adds monthly data analysis if completed
7. Limitations explicitly notes: validation data, governance data, post-reform data

**Strengths**:
- ✅ Subsidy-moral hazard: β = -0.547***, robust across 7/8 specs
- ✅ Novel theoretical framework (stakeholder-distributed distress)
- ✅ True Leverage Ratio concept
- ✅ Policy-relevant (€500M+ bailouts across Europe)

**Acknowledged Limitations**:
- ⚠️ PHFSI validation pending capital injection data
- ⚠️ Single-country study (Portugal)
- ⚠️ Annual data (cannot test sequential timing)
- ⚠️ Governance unobserved (missing variable bias possible)

### Follow-Up Paper 1 (Submit 2027)

**Title**: Reform, Integration, and Financial Sustainability: Evidence from Portugal's ULS Consolidation

**Focus**: Full DiD analysis of 2024 ULS reform with post-treatment data

### Follow-Up Paper 2 (Submit 2026-2027)

**Title**: Governance Heterogeneity in Public Hospital Financial Management

**Focus**: Survey-based governance analysis

### Follow-Up Paper 3 (Submit 2027-2028)

**Title**: Monopsony Power and Supplier Distress in Public Healthcare Markets

**Focus**: Hospital-supplier matched dataset analysis

---

## CONCLUSION

**Publication-Ready Status**:
- **Current state**: Not ready (3 critical gaps)
- **With Phase 1 actions** (4 weeks): Ready for submission with acknowledged limitations
- **With Phase 2-3 actions** (3-6 months): Significantly strengthened manuscript

**Minimum Required for Submission**:
1. ✅ Fix CQMI (entity mapping) OR explicitly note 4-component limitation
2. ✅ File FOI request for capital injection data
3. ✅ Remove H3 from main text
4. ✅ Reframe H2 if validation data unavailable

**Optimal for Strong Acceptance**:
1. ✅ All of above, plus:
2. ✅ Monthly lead-lag analysis (Granger causality)
3. ✅ Capital injection validation (ROC analysis)
4. ✅ Governance heterogeneity (at least proxy variables)

**The paper's core contribution (H1: subsidy-induced moral hazard) is robust and publication-worthy regardless of missing data. The missing data primarily affects secondary analyses and theoretical extensions.**

---

**Report Prepared**: December 31, 2025
**Next Update**: After FOI response received (estimated 4-8 weeks)
