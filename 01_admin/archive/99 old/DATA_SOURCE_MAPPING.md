# COMPREHENSIVE DATA SOURCE MAPPING
## Corporate Finance Research on Portuguese SNS Financial Distress

**Document Date:** October 25, 2025  
**Purpose:** Complete inventory of required data sources, download priorities, and access strategies

---

## PART I: SNS TRANSPARENCY PORTAL DATASETS (IMMEDIATE DOWNLOAD)

### **Priority 1: ESSENTIAL FINANCIAL DATA (Start Today)**

#### 1. **Dívida Total, Vencida e Pagamentos em Atraso**
- **Dataset ID:** `divida-total-vencida-e-pagamentos`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/divida-total-vencida-e-pagamentos
- **Description:** Monthly evolution of total debt, overdue debt, and late payments to suppliers
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - Total Debt (Dívida Total)
  - Overdue Debt (Dívida Vencida)
  - Late Payments (Pagamentos em Atraso)
  - By institution and month
- **PHFSI Component:** Stakeholder Pressure Index (SPI) - Overdue Liabilities ratio
- **Critical Importance:** ⭐⭐⭐⭐⭐ (Core dependent variable data)
- **Expected Time Coverage:** 2017-2024 (96 months)

---

#### 2. **Agregados Económico Financeiros**
- **Dataset ID:** `agregados-economico-financeiros`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/agregados-economico-financeiros
- **Description:** Monthly evolution of economic-financial aggregates (revenues, expenses, assets, liabilities)
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - Total Revenue (Receitas Totais)
  - Operating Revenue (Receitas Operacionais)
  - Total Expenses (Despesas Totais)
  - Operating Expenses (Despesas Operacionais)
  - Total Assets (Ativo Total)
  - Total Liabilities (Passivo Total)
  - Equity (Capital Próprio)
  - Net Income (Resultado Líquido)
- **PHFSI Components:** 
  - Operational Self-Sufficiency Ratio (OSSR)
  - True Leverage Ratio (TLR)
- **Critical Importance:** ⭐⭐⭐⭐⭐ (Core financial statement data)
- **Expected Time Coverage:** 2017-2024 (96 months)
- **Known Limitation:** Does NOT disaggregate government subsidies from operating revenue

---

#### 3. **Prazo Médio de Pagamento a Fornecedores**
- **Dataset ID:** `tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores
- **Description:** Average payment period (PMP) from SNS institutions to suppliers
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - Average Payment Days (Prazo Médio de Pagamento)
  - By institution and month
- **PHFSI Component:** Stakeholder Pressure Index (SPI) - Supplier Payment Days
- **Critical Importance:** ⭐⭐⭐⭐⭐ (Direct measure of supplier pressure)
- **Expected Time Coverage:** 2017-2024 (96 months)
- **Research Note:** Compare to Greek 1,485-day average

---

#### 4. **Conta do Serviço Nacional de Saúde**
- **Dataset ID:** `conta-do-servico-nacional-de-saude`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/conta-do-servico-nacional-de-saude
- **Description:** Comprehensive SNS financial accounts (validation source)
- **Update Frequency:** Annual
- **Coverage:** Aggregate SNS level
- **Variables Provided:**
  - Consolidated financial statements
  - System-level aggregates
  - Subsidy allocations (aggregate)
- **PHFSI Component:** Validation and benchmarking
- **Critical Importance:** ⭐⭐⭐⭐ (System-level context)
- **Expected Time Coverage:** 2017-2024 (8 years)

---

### **Priority 2: OPERATIONAL & STAFFING DATA (Week 1)**

#### 5. **Trabalhadores por Grupo Profissional**
- **Dataset ID:** `trabalhadores-por-grupo-profissional`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/trabalhadores-por-grupo-profissional
- **Description:** Monthly headcount by professional group
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - Number of workers by professional category
  - Physicians, Nurses, Administrative, Technical, etc.
  - By institution and month
- **PHFSI Component:** Stakeholder Pressure Index (SPI) - Staff Turnover proxy
- **Critical Importance:** ⭐⭐⭐⭐ (Workforce stability indicator)
- **Expected Time Coverage:** 2017-2024 (96 months)
- **Calculation Method:** Month-over-month % change as proxy turnover
- **Limitation:** Does NOT directly provide hires/separations

---

#### 6. **Trabalhadores por Modalidade de Vinculação**
- **Dataset ID:** `trabalhadores-por-modalidade-de-vinculacao`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/trabalhadores-por-modalidade-de-vinculacao
- **Description:** Monthly headcount by employment type (permanent, temporary, contract)
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - Workers by contract type
  - Permanent (Contrato sem Termo)
  - Temporary (Contrato a Termo)
  - Commission (Comissão de Serviço)
  - Other modalities
- **PHFSI Component:** Supplementary for SPI - precarious employment indicator
- **Critical Importance:** ⭐⭐⭐ (Workforce quality indicator)
- **Research Note:** High temporary % may indicate financial stress

---

#### 7. **Ausência ao Trabalho por Tipologia**
- **Dataset ID:** `contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia
- **Description:** Monthly cumulative absence days by reason
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - Absence days by type (sick leave, training, maternity, etc.)
  - By institution and month
- **PHFSI Component:** Supplementary for SPI - workforce stress indicator
- **Critical Importance:** ⭐⭐⭐ (Indirect financial stress signal)
- **Research Note:** Rising sick leave may correlate with morale/stress from financial problems

---

#### 8. **Percentagem de Gastos com TE e Suplementos no Total Gastos com Pessoal**
- **Dataset ID:** `percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal
- **Description:** % of overtime and supplements in total personnel costs
- **Update Frequency:** Monthly
- **Coverage:** All SNS institutions
- **Variables Provided:**
  - % Overtime/Supplements in total payroll
- **PHFSI Component:** Cost structure indicator (related to OSSR)
- **Critical Importance:** ⭐⭐⭐ (Operational efficiency)
- **Research Note:** High % may indicate understaffing (efficiency problem)

---

### **Priority 3: CLINICAL QUALITY & OUTCOMES DATA (Week 1-2)**

#### 9. **Morbilidade e Mortalidade Hospitalar por Instituição**
- **Dataset ID:** `morbilidade-e-mortalidade-hospitalar`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/morbilidade-e-mortalidade-hospitalar
- **Description:** Quarterly inpatient admissions, days, and deaths by institution
- **Update Frequency:** Quarterly
- **Coverage:** All SNS hospitals
- **Variables Provided:**
  - Inpatient episodes
  - Patient days
  - Deaths
  - By institution, quarter, and ICD chapter
- **PHFSI Component:** Clinical Quality Maintenance Index (CQMI) - mortality rate
- **Critical Importance:** ⭐⭐⭐⭐ (Core outcome measure)
- **Expected Time Coverage:** 2017-2024 (32 quarters)
- **Calculation Method:** Deaths / Episodes = Crude Mortality Rate

---

#### 10. **Morbilidade e Mortalidade Hospitalar por Faixa Etária**
- **Dataset ID:** `morbilidade-e-mortalidade-hospitalar-por-faixa-etaria`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/morbilidade-e-mortalidade-hospitalar-por-faixa-etaria
- **Description:** Quarterly inpatient data by age group
- **Update Frequency:** Quarterly
- **Coverage:** All SNS hospitals
- **Variables Provided:**
  - Admissions, days, deaths by age bracket
- **PHFSI Component:** CQMI - age-adjusted mortality calculation
- **Critical Importance:** ⭐⭐⭐⭐ (Enables risk adjustment)
- **Research Note:** Essential for SMR (Standardized Mortality Ratio)

---

#### 11. **Mortalidade por AVC Isquémico e Hemorrágico**
- **Dataset ID:** `taxa-de-mortalidade-por-avc-isquemico-e-hemorragico`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/taxa-de-mortalidade-por-avc-isquemico-e-hemorragico
- **Description:** Stroke mortality rates by institution
- **Update Frequency:** Annual/Quarterly
- **Coverage:** Hospitals treating stroke
- **Variables Provided:**
  - Ischemic stroke mortality rate
  - Hemorrhagic stroke mortality rate
- **PHFSI Component:** CQMI - condition-specific outcome
- **Critical Importance:** ⭐⭐⭐ (High-quality indicator)
- **Research Note:** Stroke care is sensitive to resource constraints

---

#### 12. **Fraturas da Anca (Cirurgias nas primeiras 48h)**
- **Dataset ID:** `fraturas-da-anca-cirurgias-nas-primeiras-48h`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/fraturas-da-anca-cirurgias-nas-primeiras-48h
- **Description:** % hip fractures operated within 48 hours
- **Update Frequency:** Monthly
- **Coverage:** All SNS hospitals
- **Variables Provided:**
  - Total hip fractures
  - Number operated within 48h
  - % within 48h
- **PHFSI Component:** CQMI - process quality indicator
- **Critical Importance:** ⭐⭐⭐⭐ (Internationally recognized quality metric)
- **Research Note:** Delays often due to resource constraints (OR availability, staffing)

---

#### 13. **Notificação de Incidentes de Segurança**
- **Dataset ID:** `notificacao-de-incidentes-de-seguranca-em-unidades-prestadoras-de-cuidados-de-sa`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/notificacao-de-incidentes-de-seguranca-em-unidades-prestadoras-de-cuidados-de-sa
- **Description:** Safety incident notifications from healthcare units
- **Update Frequency:** Continuous/Monthly aggregation
- **Coverage:** Participating units (voluntary reporting)
- **Variables Provided:**
  - Number of incidents by type
  - Severity level
  - By institution
- **PHFSI Component:** CQMI - patient safety proxy
- **Critical Importance:** ⭐⭐⭐ (Best available safety measure)
- **Limitation:** Voluntary reporting = underreporting bias
- **Research Note:** Use as inverse indicator (more reports may = better culture OR worse safety)

---

#### 14. **Partos e Cesarianas nos Cuidados de Saúde Hospitalares**
- **Dataset ID:** `partos-e-cesarianas`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/partos-e-cesarianas
- **Description:** Monthly births and cesarean sections
- **Update Frequency:** Monthly
- **Coverage:** All maternity hospitals
- **Variables Provided:**
  - Total births
  - Cesarean sections
  - Cesarean rate (%)
- **PHFSI Component:** CQMI - appropriateness of care indicator
- **Critical Importance:** ⭐⭐⭐ (WHO benchmark: <25%)
- **Research Note:** High cesarean rate may indicate defensive medicine or capacity constraints

---

### **Priority 4: ACCESS & UTILIZATION DATA (Week 2)**

#### 15. **Inscritos em LIC dentro do TMRG (180 dias)**
- **Dataset ID:** `inscritos-em-lic-dentro-do-tmrg-180-dias`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/inscritos-em-lic-dentro-do-tmrg-180-dias
- **Description:** % surgical patients within 180-day maximum guaranteed wait time
- **Update Frequency:** Monthly
- **Coverage:** All SNS hospitals with surgical services
- **Variables Provided:**
  - Patients on surgical waiting list (LIC)
  - Patients within 180-day limit
  - % compliance
- **PHFSI Component:** CQMI - access indicator
- **Critical Importance:** ⭐⭐⭐⭐ (Government performance target)
- **Research Note:** Non-compliance may trigger government intervention

---

#### 16. **Primeiras Consultas em Tempo Adequado**
- **Dataset ID:** `consultas-em-tempo-real`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/consultas-em-tempo-real
- **Description:** First consultations provided within appropriate timeframe
- **Update Frequency:** Monthly
- **Coverage:** Outpatient services
- **Variables Provided:**
  - Consultations by priority level
  - Wait times
  - % within targets
- **PHFSI Component:** CQMI - access indicator
- **Critical Importance:** ⭐⭐⭐⭐ (Core access metric)

---

#### 17. **Demora Média antes da Cirurgia**
- **Dataset ID:** `demora-media-antes-da-cirurgia`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/demora-media-antes-da-cirurgia
- **Description:** Average wait time before surgery
- **Update Frequency:** Monthly
- **Coverage:** All surgical services
- **Variables Provided:**
  - Average days waiting
  - By hospital and specialty
- **PHFSI Component:** CQMI - access indicator
- **Critical Importance:** ⭐⭐⭐⭐ (Patient experience + clinical risk)
- **Research Note:** Long waits for urgent procedures = major quality problem

---

#### 18. **Atendimentos por Tipo de Urgência Hospitalar**
- **Dataset ID:** `atendimentos-por-tipo-de-urgencia-hospitalar-link`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/atendimentos-por-tipo-de-urgencia-hospitalar-link
- **Description:** Emergency department visits by type
- **Update Frequency:** Monthly
- **Coverage:** All emergency departments
- **Variables Provided:**
  - ED visits
  - By hospital and urgency type (medical, surgical, trauma, etc.)
- **PHFSI Component:** Activity level indicator (control variable)
- **Critical Importance:** ⭐⭐⭐ (Demand proxy)

---

#### 19. **Atendimentos em Urgência Hospitalar por Triagem de Manchester**
- **Dataset ID:** `atendimentos-em-urgencia-triagem-manchester`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/atendimentos-em-urgencia-triagem-manchester
- **Description:** ED visits by Manchester Triage priority level
- **Update Frequency:** Monthly
- **Coverage:** EDs using Manchester protocol
- **Variables Provided:**
  - Visits by triage color (Red=immediate, Orange=very urgent, Yellow=urgent, etc.)
- **PHFSI Component:** Case mix complexity proxy
- **Critical Importance:** ⭐⭐⭐ (Acuity measure)
- **Research Note:** Higher acuity = higher costs

---

#### 20. **Taxa de Ocupação Hospitalar**
- **Dataset ID:** `ocupacao-do-internamento`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/ocupacao-do-internamento
- **Description:** Inpatient bed occupancy rate
- **Update Frequency:** Monthly
- **Coverage:** All inpatient hospitals
- **Variables Provided:**
  - % bed occupancy
  - By hospital
- **PHFSI Component:** Operational efficiency indicator
- **Critical Importance:** ⭐⭐⭐ (Capacity utilization)
- **Research Note:** >85% = overcrowding, <70% = underutilization

---

### **Priority 5: HOSPITAL CHARACTERISTICS (Week 2)**

#### 21. **Lotação Hospitalar para Doentes Agudos**
- **Dataset ID:** `lotacao-praticada-por-tipo-de-cama`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/lotacao-praticada-por-tipo-de-cama
- **Description:** Hospital bed capacity by type
- **Update Frequency:** Annual/As changed
- **Coverage:** All hospitals
- **Variables Provided:**
  - Total beds
  - By bed type (acute, ICU, maternity, etc.)
- **PHFSI Component:** Hospital size measure (control variable)
- **Critical Importance:** ⭐⭐⭐⭐ (Key hospital characteristic)
- **Research Use:** Alternative size measure to total assets

---

#### 22. **Caracterização das Valências de Urgência**
- **Dataset ID:** `caracterizacao-das-valencias-de-urgencia`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/caracterizacao-das-valencias-de-urgencia
- **Description:** Characterization of emergency services by capability level
- **Update Frequency:** Annual/As changed
- **Coverage:** All emergency departments
- **Variables Provided:**
  - ED type (Basic, Médico-Cirúrgica, Polivalente, etc.)
  - Resources available
  - Services provided
- **PHFSI Component:** Hospital capability classification (control variable)
- **Critical Importance:** ⭐⭐⭐ (Hospital type identifier)

---

#### 23. **Atividade de Internamento Hospitalar**
- **Dataset ID:** `atividade-de-internamento-hospitalar`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/atividade-de-internamento-hospitalar
- **Description:** Inpatient activity metrics
- **Update Frequency:** Monthly
- **Coverage:** All inpatient hospitals
- **Variables Provided:**
  - Admissions
  - Discharges
  - Patient days
  - Average length of stay (ALOS)
- **PHFSI Component:** Activity volume (control variable) + ALOS for complexity proxy
- **Critical Importance:** ⭐⭐⭐⭐ (Core activity measure)
- **Research Note:** ALOS ↑ as proxy for case mix complexity

---

#### 24. **Intervenções Cirúrgicas nos Cuidados de Saúde Hospitalares**
- **Dataset ID:** `intervencoes-cirurgicas`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/intervencoes-cirurgicas
- **Description:** Surgical interventions (scheduled, emergency, ambulatory)
- **Update Frequency:** Monthly
- **Coverage:** All surgical hospitals
- **Variables Provided:**
  - Surgeries by type
  - By hospital
- **PHFSI Component:** Activity volume (control variable)
- **Critical Importance:** ⭐⭐⭐ (Surgical activity level)

---

#### 25. **Cirurgias em Ambulatório**
- **Dataset ID:** `cirurgias-em-ambulatorio`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/cirurgias-em-ambulatorio
- **Description:** Ambulatory (day) surgeries
- **Update Frequency:** Monthly
- **Coverage:** Hospitals performing ambulatory surgery
- **Variables Provided:**
  - Number of ambulatory surgeries
  - By hospital
- **PHFSI Component:** Efficiency indicator (ambulatory cheaper than inpatient)
- **Critical Importance:** ⭐⭐⭐ (Efficiency metric)

---

### **Priority 6: PHARMACEUTICAL & SUPPLY COSTS (Week 2-3)**

#### 26. **Despesa com Medicamentos nos Hospitais do SNS**
- **Dataset ID:** `despesa-com-medicamentos-nos-hospitais-do-sns`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/despesa-com-medicamentos-nos-hospitais-do-sns
- **Description:** Monthly pharmaceutical expenditure in SNS hospitals
- **Update Frequency:** Monthly
- **Coverage:** All SNS hospitals
- **Variables Provided:**
  - Total pharmaceutical spending
  - By hospital and month
- **PHFSI Component:** Cost structure (supplement to financial aggregates)
- **Critical Importance:** ⭐⭐⭐ (Major cost category)
- **Research Note:** Drug costs ~15-20% of hospital budgets

---

#### 27. **Dispensa de Medicamentos**
- **Dataset ID:** `evolucao-da-dispensa-de-medicamentos`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/evolucao-da-dispensa-de-medicamentos
- **Description:** Outpatient pharmaceutical dispensing
- **Update Frequency:** Monthly
- **Coverage:** Pharmacy dispensing to SNS beneficiaries
- **Variables Provided:**
  - Prescriptions dispensed
  - Packages dispensed
- **PHFSI Component:** Not directly used (outpatient focus)
- **Critical Importance:** ⭐⭐ (Context only)

---

### **Priority 7: ADDITIONAL CONTEXT DATASETS (Week 3-4)**

#### 28. **Consultas Médicas Hospitalares**
- **Dataset ID:** `01_sica_evolucao-mensal-das-consultas-medicas-hospitalares`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/01_sica_evolucao-mensal-das-consultas-medicas-hospitalares
- **Description:** Monthly outpatient consultations in hospitals
- **Update Frequency:** Monthly
- **Coverage:** All hospitals with outpatient services
- **Variables Provided:**
  - Number of consultations by hospital
- **PHFSI Component:** Activity volume (control variable)
- **Critical Importance:** ⭐⭐⭐ (Activity level)

---

#### 29. **Consultas em Telemedicina**
- **Dataset ID:** `consultas-em-telemedicina`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/consultas-em-telemedicina
- **Description:** Telemedicine consultations
- **Update Frequency:** Monthly
- **Coverage:** Participating hospitals
- **Variables Provided:**
  - Telemedicine consultations by hospital
- **PHFSI Component:** Innovation adoption indicator
- **Critical Importance:** ⭐⭐ (Post-COVID trend)
- **Research Note:** May indicate efficiency/adaptation

---

#### 30. **Certificados de Óbito por Instituição de Saúde**
- **Dataset ID:** `certificados-de-obito-por-instituicao-de-saude`
- **URL:** https://transparencia.sns.gov.pt/explore/dataset/certificados-de-obito-por-instituicao-de-saude
- **Description:** Death certificates by health institution
- **Update Frequency:** Monthly
- **Coverage:** All institutions certifying deaths
- **Variables Provided:**
  - Number of death certificates by institution
- **PHFSI Component:** Mortality volume (supplement to morbidity/mortality dataset)
- **Critical Importance:** ⭐⭐ (Alternative mortality measure)

---

## SUMMARY: PORTAL DATASETS TO DOWNLOAD

### **Essential (Download Week 1):**
1. Dívida Total, Vencida e Pagamentos em Atraso ⭐⭐⭐⭐⭐
2. Agregados Económico Financeiros ⭐⭐⭐⭐⭐
3. Prazo Médio de Pagamento a Fornecedores ⭐⭐⭐⭐⭐
4. Conta do Serviço Nacional de Saúde ⭐⭐⭐⭐
5. Trabalhadores por Grupo Profissional ⭐⭐⭐⭐
6. Morbilidade e Mortalidade Hospitalar por Instituição ⭐⭐⭐⭐
7. Morbilidade e Mortalidade Hospitalar por Faixa Etária ⭐⭐⭐⭐
8. Fraturas da Anca (Cirurgias nas primeiras 48h) ⭐⭐⭐⭐
9. Inscritos em LIC dentro do TMRG (180 dias) ⭐⭐⭐⭐
10. Primeiras Consultas em Tempo Adequado ⭐⭐⭐⭐
11. Demora Média antes da Cirurgia ⭐⭐⭐⭐
12. Lotação Hospitalar para Doentes Agudos ⭐⭐⭐⭐
13. Atividade de Internamento Hospitalar ⭐⭐⭐⭐

### **Important (Download Week 2):**
14. Trabalhadores por Modalidade de Vinculação ⭐⭐⭐
15. Ausência ao Trabalho por Tipologia ⭐⭐⭐
16. Percentagem de Gastos com TE e Suplementos ⭐⭐⭐
17. Mortalidade por AVC Isquémico e Hemorrágico ⭐⭐⭐
18. Notificação de Incidentes de Segurança ⭐⭐⭐
19. Partos e Cesarianas ⭐⭐⭐
20. Atendimentos por Tipo de Urgência Hospitalar ⭐⭐⭐
21. Atendimentos em Urgência por Triagem de Manchester ⭐⭐⭐
22. Taxa de Ocupação Hospitalar ⭐⭐⭐
23. Caracterização das Valências de Urgência ⭐⭐⭐
24. Intervenções Cirúrgicas ⭐⭐⭐
25. Cirurgias em Ambulatório ⭐⭐⭐
26. Despesa com Medicamentos nos Hospitais ⭐⭐⭐
27. Consultas Médicas Hospitalares ⭐⭐⭐

### **Supplementary (Download Week 3-4):**
28. Consultas em Telemedicina ⭐⭐
29. Certificados de Óbito por Instituição ⭐⭐
30. Dispensa de Medicamentos ⭐⭐

**Total Portal Datasets to Download: 30 out of 138**

---

## PART II: EXTERNAL DATA SOURCES (REQUIRE FORMAL REQUESTS)

### **CATEGORY A: ACSS (Administração Central do Sistema de Saúde)**

**Entity:** ACSS - Central Health System Administration  
**Website:** https://www.acss.min-saude.pt  
**Contact:** Through formal letter (template provided separately)  
**Expected Response Time:** 2-3 months  
**Probability of Access:** 40-60%

---

#### **ACSS-1: Detailed Hospital Financial Statements**

**What's Needed:**
- Monthly balance sheets (2017-2024)
- Monthly income statements (2017-2024)
- Monthly cash flow statements (2017-2024)
- Notes to financial statements showing:
  - Government subsidy disaggregation (operational vs. capital)
  - Accounts receivable aging schedule
  - Accounts payable aging schedule
  - Long-term debt details (if any)
  - Related party transactions

**Why Portal Data Insufficient:**
- `Agregados Económico Financeiros` provides high-level aggregates only
- Does NOT disaggregate:
  - Operating subsidies from capital grants
  - Cash vs. accrual revenues
  - Current vs. non-current receivables
- No cash flow statement equivalent in portal

**PHFSI Components Enabled:**
- Liquidity Realization Rate (LRR) - requires cash collections data
- True Leverage Ratio (TLR) - requires subsidy detail
- Operational Self-Sufficiency Ratio (OSSR) - requires clean subsidy separation

**Request Specifics:**
- Format: Excel spreadsheets with standardized chart of accounts
- Level: Individual hospital (not consolidated)
- Frequency: Monthly
- Period: January 2017 - December 2024
- Institutions: All ULS + standalone hospitals (n~70)

**Alternative if Denied:**
- Use portal aggregates with documented assumptions
- Approximate subsidies using historical averages
- Proxy cash collections from A/R changes

---

#### **ACSS-2: Case Mix Index (CMI) Data**

**What's Needed:**
- Monthly Case Mix Index by hospital (2017-2024)
- DRG-level activity data (if available)
- Patient classification system documentation

**Why Portal Data Insufficient:**
- `Atividade de Internamento Hospitalar` provides volume but not complexity
- `Morbilidade e Mortalidade` provides diagnoses but not DRG weights
- No standardized complexity measure in portal

**PHFSI Components Enabled:**
- Case mix adjustment for mortality rates (CQMI)
- Hospital size/complexity control variable
- Resource intensity expectations

**Request Specifics:**
- Monthly CMI by hospital
- Documentation of CMI calculation methodology
- If available: DRG distribution by hospital

**Alternative if Denied:**
- Construct proxy CMI from:
  - Average length of stay (ALOS) - from portal
  - % ICU beds / total beds - from hospital websites
  - Teaching hospital status - from public records
  - Specialty services offered - from characterization dataset

---

#### **ACSS-3: €500 Million Capital Injection Allocation (October 2024)**

**What's Needed:**
- Hospital-level allocation amounts
- Disbursement dates
- Allocation criteria/formula used
- Conditions attached to transfers
- Monitoring/reporting requirements

**Why Portal Data Insufficient:**
- Capital injections mentioned in aggregate budget documents (CFE.pdf)
- Individual hospital allocations NOT in transparency portal
- No dataset tracking extraordinary capital transfers

**PHFSI Components Enabled:**
- Instrumental variable for DiD analysis
- Liquidity shock exogenous to current management
- Validates government intervention as outcome variable

**Request Specifics:**
- Hospital-by-hospital breakdown of €500M
- Timing of disbursement (month)
- Allocation formula (was it proportional to arrears?)
- Any earmarking (e.g., must pay specific suppliers)

**Alternative Sources if ACSS Denies:**
1. **Tribunal de Contas audits** (see Section B below)
2. **Hospital annual reports** (Q4 2024 / Q1 2025) - will show capital increases
3. **Parliamentary budget documents** - sometimes include annexes with breakdowns
4. **Media reports** - may cite specific hospital amounts

**Research Implication:**
- If we cannot get allocation data, we lose the IV strategy
- Can still use ULS reform DiD
- Can still validate PHFSI against any government intervention

---

#### **ACSS-4: Hospital Manager Characteristics**

**What's Needed:**
- CEO/Executive Director appointment dates
- Educational background (degree, field, institution)
- Previous work experience
- Political affiliation (if applicable)
- Compensation structure
- Contract type and duration

**Why Portal Data Insufficient:**
- Zero HR/governance data in transparency portal
- Manager names sometimes in activity reports but no characteristics

**PHFSI Components Enabled:**
- Governance quality variables
- Test heterogeneous treatment effects
- Control for manager fixed effects in panel

**Request Specifics:**
- For all hospitals, 2017-2024:
  - Current and past CEOs/Executive Directors
  - Appointment and departure dates
  - CV information (education, experience)
  - Appointment mechanism (competition, direct appointment)

**Alternative Sources:**
1. **Hospital websites** - often have CEO bios
2. **LinkedIn** - professional profiles
3. **Diário da República** - appointment announcements for public positions
4. **News articles** - especially for major appointments
5. **Governance survey** (see Section C)

**Data Collection Strategy:**
- Start with publicly available sources (websites, DR)
- Fill gaps with ACSS request
- Survey as last resort for detailed governance data

---

#### **ACSS-5: ULS Integration Implementation Timeline**

**What's Needed:**
- Legal creation date for each ULS (Decreto-Lei number and date)
- Operational integration milestones:
  - Shared services implementation date
  - Unified budget date
  - Clinical integration date
  - IT system integration date
- Pre-integration hospital identifiers → Post-integration ULS mapping

**Why Portal Data Insufficient:**
- Portal datasets use current institutional identifiers
- No explicit "ULS creation date" field
- Some institutions changed codes after integration

**PHFSI Components Enabled:**
- Treatment variable for DiD analysis
- Key to entire quasi-experimental strategy

**Request Specifics:**
- Complete list of ULS created 2024
- For each: constituent hospitals + creation date
- Integration timeline/roadmap if available

**Alternative Sources (EASIER):**
1. **Diário da República (Official Gazette)** - Primary legal source
   - URL: https://diariodarepublica.pt
   - Search: "Unidade Local de Saúde" + 2024
   - Each ULS created by specific Decreto-Lei with exact date
   - **This is publicly available and authoritative**

2. **SNS Press Releases**
   - URL: https://www.sns.gov.pt/noticias/
   - 2024 announcements of ULS creation
   - Example found in handover: https://www.sns.gov.pt/noticias/2024/01/01/arranca-nova-fase-da-organizacao-do-sns/

3. **Ministry of Health Legislation Database**
   - https://www.dgs.pt/legislacao.aspx
   - Healthcare organizational laws

**Data Collection Priority:**
- **Week 1:** Manual search of Diário da República
- Create spreadsheet: ULS Name | Creation Date | Constituent Hospitals | Legal Reference
- This is ESSENTIAL for DiD and can be done immediately without waiting for ACSS

---

#### **ACSS-6: Government Intervention Events (Validation Outcome)**

**What's Needed:**
- Database of extraordinary government interventions in hospitals (2017-2024):
  - Emergency capital injections (beyond routine subsidies)
  - Forced mergers or restructurings
  - Ministry-imposed management oversight
  - Special audits or investigations
  - Service suspensions
  - Financial rescue packages

**Why Portal Data Insufficient:**
- Routine subsidies in `Agregados Económico Financeiros` but not extraordinary interventions
- No dataset tracking "crisis events"

**PHFSI Components Enabled:**
- **Dependent variable for validation analysis**
- Does PHFSI predict which hospitals get emergency intervention?
- This is critical for demonstrating PHFSI superiority over Z-scores

**Request Specifics:**
- Hospital-level intervention database
- Event type, date, amount (if financial)
- Trigger/reason for intervention

**Alternative Sources:**
1. **Tribunal de Contas audit reports** (Section B)
2. **Parliamentary questions/debates** - interventions often discussed
3. **Media database search** - "resgate financeiro hospital" + hospital name
4. **Ministry annual reports** - sometimes list problem institutions

**Research Approach:**
- Construct intervention database from multiple sources
- Binary variable: Intervention (Yes/No) by hospital-year
- Continuous variable: Intervention intensity (€ or number of events)

---

### **CATEGORY B: TRIBUNAL DE CONTAS (COURT OF AUDITORS)**

**Entity:** Tribunal de Contas - Portuguese Court of Auditors  
**Website:** https://www.tcontas.pt  
**Contact:** Public access to audit reports; deeper access via research request  
**Expected Response Time:** Immediate for published reports; 1-2 months for archives  
**Probability of Access:** 90% (public reports); 40% (detailed audit files)

---

#### **TC-1: Hospital Financial Audit Reports (2017-2024)**

**What's Available:**
- Annual financial audits of major hospitals
- Special audits of problematic institutions
- System-wide healthcare financing audits
- Compliance audit findings
- Recommendations and management responses

**Access Method:**
- **Public reports:** Download directly from website
  - URL: https://www.tcontas.pt/pt-pt/ProdutosTC/Relatorios/RelatoriosAuditoria/
  - Search: "hospital" or "SNS" or specific institution names
  - Format: PDF reports (comprehensive)

**Value for Research:**
1. **Validation of Portal Data:**
   - Auditors verify financial statement accuracy
   - Flag data quality issues
   - Provide context on accounting policies

2. **Identification of Financial Distress Events:**
   - Audits often triggered by financial problems
   - Document arrears, irregular payments, budget overruns
   - Provide narrative of how problems developed

3. **Governance Quality Indicators:**
   - Internal control deficiencies
   - Management oversight issues
   - Board effectiveness assessments

4. **Case Study Material:**
   - Rich qualitative detail on specific hospitals
   - Can triangulate with quantitative PHFSI

**Data Extraction Strategy:**
- Download all hospital-related audit reports 2017-2024
- Create database: Hospital | Year | Audit Type | Key Findings | Recommendations
- Code findings: Financial distress severity (1-5 scale)
- Use as supplementary validation of PHFSI

**Timeline:** 
- Week 1: Search and download all relevant reports
- Week 2-3: Systematic review and coding
- Integrate findings into validation analysis

---

#### **TC-2: Sistema de Controlo Interno (Internal Control System Data)**

**What's Available:**
- Some audit reports reference underlying control systems
- Financial management quality indicators
- Procurement irregularities
- Payment discipline issues

**Access Method:**
- Mentioned in audit reports
- May be available through research request if aggregated/anonymized

**Value for Research:**
- Governance quality proxies
- Supplement survey data

---

### **CATEGORY C: GOVERNANCE SURVEY (PRIMARY DATA COLLECTION)**

**Target:** Hospital CEOs, CFOs, or Board Chairs  
**Sample Size:** 40-50 hospitals (stratified by size, region, ULS status)  
**Timeline:** Month 3 (after initial data analysis)  
**Expected Response Rate:** 40-60% (20-30 complete responses)

---

#### **SURVEY-1: Board Composition and Structure**

**Questions (5-7 items):**
1. Board size (number of members)
2. Number of independent members (not hospital employees or government officials)
3. Professional composition:
   - Number of physicians
   - Number of nurses
   - Number of financial/administrative professionals
   - Number of patient/community representatives
4. Board meeting frequency (times per year)
5. Existence of specialized committees:
   - Audit committee (Yes/No)
   - Quality committee (Yes/No)
   - Finance committee (Yes/No)
6. Average board tenure (years)

**Measurement:**
- Construct "Board Quality Index" from responses
- Compare to financial performance

---

#### **SURVEY-2: Executive Compensation and Incentives**

**Questions (4-5 items):**
1. CEO compensation structure:
   - % Fixed salary
   - % Performance-based bonus
2. Performance metrics used for bonus (if applicable):
   - Financial targets
   - Quality targets
   - Access targets
   - Patient satisfaction
3. Contract type:
   - Fixed-term (years)
   - Indefinite
   - Commission (political appointment)
4. Performance evaluation frequency

**Measurement:**
- Create incentive alignment score
- Test correlation with PHFSI components

---

#### **SURVEY-3: Decision-Making Autonomy**

**Questions (6-8 items):**
1. Level of autonomy in key decisions (5-point Likert scale: 1=No autonomy to 5=Full autonomy):
   - Hiring/firing staff
   - Procurement of supplies
   - Service expansion/reduction
   - Budget reallocation across departments
   - Capital investments
   - Setting clinical protocols
   - Contracting with external providers

**Measurement:**
- Average autonomy score
- Test if autonomy moderates ULS treatment effect

---

#### **SURVEY-4: Financial Management Practices**

**Questions (5-6 items):**
1. Frequency of financial reporting to board:
   - Monthly / Quarterly / Semi-annually / Annually
2. Use of financial forecasting:
   - Yes, regularly / Occasionally / No
3. Cash flow management tools:
   - Cash flow projections (Yes/No)
   - Treasury management system (Yes/No)
4. External financial advisor/consultant (Yes/No)
5. Participation in financial management training (Yes/No)

**Measurement:**
- Financial management sophistication index
- Control variable in regressions

---

#### **SURVEY-5: Perceived Financial Stress**

**Questions (4-5 items):**
1. Perceived adequacy of current budget (5-point scale)
2. Frequency of budget constraints affecting clinical decisions (5-point scale)
3. Major financial concerns (rank top 3):
   - Payment delays from insurers
   - Supplier payment pressures
   - Staffing costs
   - Pharmaceutical costs
   - Equipment maintenance
   - Infrastructure deterioration
4. Expectation of future financial position (Better/Same/Worse)

**Measurement:**
- Subjective financial stress score
- Validate against objective PHFSI

---

**Survey Administration:**
- Online platform (Qualtrics or similar)
- Email invitation with university letterhead
- Emphasis on confidentiality and anonymity in publication
- Offer to share aggregate findings
- Two reminder emails at 1-week intervals
- Follow-up phone calls to non-respondents
- Small incentive (e.g., summary report of benchmarking data)

---

### **CATEGORY D: DEMOGRAPHIC & REGIONAL DATA (INE)**

**Entity:** INE - Instituto Nacional de Estatística (National Statistics Institute)  
**Website:** https://www.ine.pt  
**Contact:** Public data portal; API available  
**Expected Response Time:** Immediate  
**Probability of Access:** 100% (public data)

---

#### **INE-1: Municipal/Regional Demographics**

**What's Available:**
- Population by municipality and age group (annual)
- Dependency ratio (% over 65)
- Birth and death rates
- Migration patterns

**Access Method:**
- INE Data Portal: https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_base_dados
- API: https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api
- Download format: CSV, Excel

**Value for Research:**
- Regional demand factors (control variables)
- Population aging = higher healthcare needs
- Match to hospital catchment areas

**Data Needed:**
- Annual, 2017-2024
- By NUTS II or NUTS III region (match to RHAs)
- Variables: Total population, % 0-14, % 15-64, % 65+, Dependency ratio

---

#### **INE-2: Regional Economic Indicators**

**What's Available:**
- GDP per capita by region
- Unemployment rates
- Poverty rates
- Educational attainment

**Value for Research:**
- Socioeconomic controls
- Poorer regions → higher uncompensated care burden
- Match to hospital locations

**Data Needed:**
- Annual, 2017-2024
- By NUTS II or NUTS III
- Variables: GDP/capita, Unemployment %, At-risk-of-poverty rate

---

#### **INE-3: Health Coverage Statistics**

**What's Available:**
- % population with supplementary health insurance
- Access to healthcare indicators

**Value for Research:**
- Payer mix variation (regional)
- Alternative care options

---

### **CATEGORY E: LEGISLATION & POLICY DOCUMENTS**

**Multiple Sources - Publicly Available**

---

#### **LEG-1: Diário da República (Official Gazette)**

**Entity:** Imprensa Nacional Casa da Moeda  
**Website:** https://diariodarepublica.pt  
**Access:** Free, searchable database

**What's Needed:**
- **Priority 1:** ULS creation decrees (2024)
  - Search: "Unidade Local de Saúde" + Date range 2024
  - Extract: ULS name, creation date, constituent hospitals

- Hospital organizational statutes
- Healthcare financing legislation changes
- Manager appointment decrees (for some positions)

**Timeline:** Week 1 - Critical for treatment variable

---

#### **LEG-2: Orçamento do Estado (State Budget) Documents**

**Entity:** Ministry of Finance  
**Website:** https://www.dgo.gov.pt (Direção-Geral do Orçamento)  
**Access:** Free PDF downloads

**What's Available:**
- Annual budget laws (2017-2024)
- Budget annexes sometimes include:
  - Hospital-level allocations
  - Healthcare financing framework
  - Subsidy formulas
- Special budget amendments (e.g., October 2024 €500M)

**Value for Research:**
- Understand financing framework evolution
- Identify policy changes that affect hospitals
- Context for financial analysis

**Specific Document:** CFE.pdf (already in project folder) mentions €500M injection

---

#### **LEG-3: ACSS Annual Reports & Methodology Documents**

**Entity:** ACSS  
**Website:** https://www.acss.min-saude.pt/category/publicacoes/relatorios/  
**Access:** Free PDF downloads

**What's Available:**
- Annual activity reports (2017-2024)
- Hospital financing methodology manuals
- Performance indicator definitions
- Benchmarking reports
- Payment system documentation

**Value for Research:**
- Understand how hospitals are paid (DRG, global budget, etc.)
- Performance targets and incentives
- System-wide trends and policy priorities
- Methodology for key indicators in portal datasets

**Timeline:** Week 2-3 - Background reading

---

### **CATEGORY F: COMPARISON DATA (GREECE)**

**For Validation and Discussion Section**

---

#### **GREECE-1: Greek Hospital Financial Statements**

**Entity:** Greek Ministry of Health  
**Source:** As cited in Karakolias (2025) paper  
**Website:** https://www.moh.gov.gr/articles/oikonomikes-katastaseis-nosokomeiwn/  
**Access:** Public financial statements portal (similar to Portugal)

**What's Needed:**
- 2022 financial statements (same as Karakolias study)
- For comparison: Calculate PHFSI for Greek sample
- Demonstrate PHFSI captures distress better than Z-scores in both countries

**Timeline:** Month 2-3 - After PHFSI validated in Portugal

**Use Case:**
- Discussion section: "Our PHFSI outperforms Z-scores in both Portugal (8 years) and Greece (1 year)"
- Generalizability argument
- Demonstrates theoretical framework applies across Beveridgean systems

---

#### **GREECE-2: Greek Hospital Characteristics**

**Source:** Karakolias (2025) paper
- n=90 hospitals
- Variables: Location (7 RHAs), Size (assets/revenue), Specialty (5 types), CEO gender
- Available from published paper

**Use Case:**
- Control variables for Greece comparison
- Institutional context description

---

### **CATEGORY G: LITERATURE & THEORY DATABASES**

**For Theoretical Development and Literature Review**

---

#### **LIT-1: Academic Databases**

**Already Accessible Through University:**
- Web of Science
- Scopus  
- PubMed/MEDLINE
- EconLit
- Business Source Complete

**Key Search Terms:**
- "Soft budget constraint" + healthcare
- "Financial distress" + public sector
- "Value-based healthcare" + financing
- "Hospital financial performance" + Portugal
- Beveridge health system + sustainability

---

#### **LIT-2: Working Paper Archives**

- SSRN (Social Science Research Network)
- NBER (National Bureau of Economic Research)
- CEPR (Centre for Economic Policy Research)

**Value:** Most recent theoretical and empirical work

---

#### **LIT-3: International Organization Reports**

**WHO (World Health Organization):**
- Health system profiles
- Financial sustainability assessments
- URL: https://www.who.int/countries/prt/

**OECD:**
- Health Statistics database
- Health Systems Characteristics
- URL: https://stats.oecd.org/

**European Observatory on Health Systems and Policies:**
- Country health system reviews
- Policy briefs on financing
- URL: https://eurohealthobservatory.who.int/

**Value:** 
- International comparison context
- Healthcare financing framework
- Benchmarking data

---

## PART III: DATA ACCESS STRATEGY SUMMARY

### **Immediate Actions (Week 1):**

**Can Start Today:**
1. ✅ **Download 30 SNS Portal datasets** (Python script)
2. ✅ **Manual collection: ULS creation dates** (Diário da República)
3. ✅ **Download TC audit reports** (all hospital-related, 2017-2024)
4. ✅ **Download INE demographic data** (regional, 2017-2024)
5. ✅ **Review ACSS annual reports** (financing methodology)
6. ✅ **Review budget documents** (CFE.pdf already have; get 2017-2023)

**Total Immediate Data Coverage:** ~60-70% of needs

---

### **Formal Requests (Week 1-2):**

**ACSS Data Request Letter:**
- Priority 1: Cash flow statements
- Priority 2: CMI data
- Priority 3: €500M allocation
- Priority 4: Manager characteristics
- Priority 5: Intervention events database

**Expected Timeline:** 2-3 month response

---

### **Survey Design (Month 2-3):**

**Governance Survey:**
- After preliminary data analysis complete
- Target n=40-50 hospitals
- Expected n=20-30 responses
- 2-month window (launch to close)

---

### **Contingency Plans:**

**If ACSS Denies Request:**
- ✅ Still have 60-70% of needed data from portal
- ✅ Can construct modified PHFSI with public data
- ✅ Can execute DiD with ULS dates (from DR)
- ⚠️ Lose perfect LRR and TLR components
- ⚠️ Lose IV strategy (€500M allocation)
- ✅ Still publishable in good journal (JHE alternative)

**If Survey Response Low (<20):**
- ✅ Use archival governance data (websites, LinkedIn)
- ✅ Subsample analysis with smaller n
- ✅ Qualitative interviews with 5-10 CFOs
- ✅ Still have rich financial data for main analysis

---

## PART IV: DATA SUFFICIENCY MATRIX

### Can We Answer Each Research Question?

| Research Question | Public Data | ACSS Data | Survey | Sufficient? |
|-------------------|-------------|-----------|---------|-------------|
| **RQ1: Develop PHFSI** | ✅ 80% | ⭐ 20% | ❌ | ✅ YES (modified version) |
| **RQ2: Validate PHFSI vs Z-scores** | ✅ 90% | ⭐ 10% | ❌ | ✅ YES |
| **RQ3: ULS reform effects (DiD)** | ✅ 95% | ❌ | ❌ | ✅ YES |
| **RQ4: Governance effects** | ⚠️ 30% | ⭐ 20% | ⭐⭐ 50% | ⚠️ PARTIAL |
| **RQ5: Predict intervention** | ✅ 70% | ⭐ 30% | ❌ | ✅ YES |

**Legend:**
- ✅ Available from public sources
- ⭐ Requires ACSS/external request (may not get)
- ⭐⭐ Requires primary data collection
- ❌ Not needed for this RQ

---

## PART V: FINAL DATA COLLECTION CHECKLIST

### **Week 1 (NOW):**
- [ ] Set up Python environment for SNS Portal downloads
- [ ] Download 13 essential portal datasets (Priority 1)
- [ ] Manual search Diário da República for ULS decrees
- [ ] Create ULS creation date spreadsheet
- [ ] Download 5-10 TC audit reports (start)
- [ ] Draft ACSS data request letter
- [ ] Download INE demographic data

### **Week 2:**
- [ ] Complete download of 27 portal datasets (Priority 1-2)
- [ ] Clean and merge financial datasets
- [ ] Complete ULS decree collection
- [ ] Download all remaining TC audit reports
- [ ] Review ACSS annual reports (2017-2024)
- [ ] Submit ACSS formal data request
- [ ] Start descriptive statistics

### **Week 3-4:**
- [ ] Download supplementary portal datasets (Priority 3)
- [ ] Code TC audit findings database
- [ ] Collect manager data from public sources (websites, LinkedIn)
- [ ] Preliminary PHFSI calculation
- [ ] Data quality assessment
- [ ] Missing data analysis

### **Month 2:**
- [ ] Follow up on ACSS request
- [ ] Design governance survey instrument
- [ ] IRB protocol preparation (if required)
- [ ] Start panel data construction
- [ ] Preliminary validation analysis

### **Month 3:**
- [ ] Launch governance survey
- [ ] Follow-up emails and phone calls
- [ ] Panel regression analysis
- [ ] DiD parallel trends tests
- [ ] Close survey and analyze

---

## CONCLUSION: DATA AVAILABILITY ASSESSMENT

**Overall Data Availability: EXCELLENT (75-85%)**

✅ **We can execute a high-quality study with public data alone**

The SNS Transparency Portal provides:
- ✅ 8 years of longitudinal financial data
- ✅ Hospital-level panel structure
- ✅ Activity and quality indicators
- ✅ Sufficient for modified PHFSI
- ✅ Sufficient for DiD analysis
- ✅ Sufficient for validation against interventions

**Additional data from ACSS and survey would:**
- ⭐ Elevate from "very good" to "excellent"
- ⭐ Enable perfect PHFSI calculation
- ⭐ Enable richer governance analysis
- ⭐ Provide IV strategy alternative

**But: Not make-or-break**

**Bottom Line:** START DOWNLOADING TODAY. Don't wait for ACSS response.

---

**End of Data Source Mapping Document**

*Next Steps: Generate Python download script and ACSS request letter template*
