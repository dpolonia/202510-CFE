# Capital Injection Data Collection - Session 2 Findings
**Date**: January 1, 2026
**Purpose**: Search for hospital-level breakdown of November 2024 (975.5M€) capital injection

---

## SUMMARY

**Objective**: Find Diário da República publication with hospital-level allocation details for the November 2024 capital injection (similar to October 2025 Despacho 12497/2025)

**Result**: ❌ **NO hospital-level breakdown found** in publicly accessible sources

---

## DETAILED FINDINGS

### November 2024 Capital Injection - Corrected Information

**Previous understanding** (from Session 1):
- Amount: 976M€
- Date: December 2024
- Source: Observatory #82 + Press

**Corrected information** (Session 2):
- **Exact amount**: 975,587,251€ (975.587M€)
- **Transfer date**: November 2024
- **Publication date**: December 11, 2024
- **Authorization**: Joint ministerial order (Despacho Conjunto)
- **Ministers**: Joaquim Miranda Sarmento (Finance) + Ana Paula Martins (Health)
- **Purpose**: Settle debts to external suppliers with payment deadlines overdue >90 days
- **Recipients**: ULS (Local Health Units) + IPO (Portuguese Oncology Institutes)
- **Context**: August 2024 overdue debt was 902M€

**Source**: Jornal de Negócios - https://www.jornaldenegocios.pt/economia/saude/detalhe/governo-injeta-quase-mil-milhoes-no-sns-para-pagar-dividas-a-fornecedores

---

## SEARCHES PERFORMED

### 1. SNS Transparency Portal Exploration

**Datasets checked**:
- Dívida Total, Vencida e Pagamentos em Atraso (Total Debt, Overdue, and Payment Arrears)
- Agregados Económico Financeiros (Economic and Financial Aggregates)
- Conta do Serviço Nacional de Saúde (National Health Service Accounts)

**Finding**:
- Datasets track monthly debt evolution by entity (ULS/hospital)
- Contains budget execution data and financial aggregates
- **BUT**: Web interface doesn't show allocation breakdowns
- API access attempted but failed (400 errors)
- Would require downloading full datasets or direct API authentication

**Conclusion**: Portal may contain hospital-level data but not easily accessible through web interface

---

### 2. Diário da República Search

**Searches conducted**:
- DR website (dre.pt) and alternative mirror (dre.tretas.org)
- Date ranges: November-December 2024
- Search terms: "despacho conjunto", "975", "976", "milhões", "ULS", "hospitais"
- Specific searches for joint ministerial orders from Nov-Dec 2024

**Despachos found and checked**:
- Despacho 14560/2024 (Dec 10) - Pre-hospital emergency teams (Red Cross) ❌
- Despacho 14705/2024 (Dec 12) - Hospital Central do Alentejo construction ❌
- Despacho 14764/2024 (Dec 13) - Military health administrative powers ❌
- Multiple other December 2024 orders - None related to capital injection ❌

**Conclusion**: No Diário da República publication found with hospital-level allocation for November 2024 transfer

---

### 3. Press and News Sources

**Sources searched**:
- PÚBLICO, Observador, RTP, Jornal de Negócios, Notícias ao Minuto, DN
- Search period: November-December 2024
- Keywords: capital injection, 975/976 milhões, ULS, hospitais, distribuição

**Finding**:
- All sources confirm the 975.5M€ transfer
- Purpose confirmed: Overdue debt payment (>90 days)
- Recipients confirmed: ULS + IPO
- **BUT**: No source provides hospital-by-hospital breakdown
- Only aggregate amount reported

**Conclusion**: Capital injection confirmed but allocation detail not published in press

---

## KEY INSIGHT: Publication Pattern Difference

### October 2025 (500M€) - PUBLISHED WITH DETAIL
- **Despacho 12497/2025** (October 24, 2025)
- Diário da República nº 206/2025, Série II
- **Complete breakdown**: 42 entities with exact amounts
- URL: https://dre.tretas.org/dre/6323671

### November 2024 (975.5M€) - NO PUBLIC BREAKDOWN
- Joint ministerial order mentioned in press
- No Diário da República publication found
- Allocation detail not published
- **Hypothesis**: Internal budget allocation not requiring detailed public publication

---

## IMPLICATIONS FOR PHFSI RESEARCH

### Data Available
✅ **October 2025**: Complete hospital-level data (500M€ to 42 entities)
❌ **November 2024**: Aggregate only (975.5M€ total, no breakdown)
❌ **All other injections** (2009-2023): Aggregate only

### Research Impact
1. **Validation dataset**: October 2025 provides sufficient hospital-level data
2. **Sample size**: 42 entities (39 ULS + 3 IPO) with exact allocations
3. **Representativeness**: Covers most SNS entities, including top debt accumulation hospitals
4. **Temporal coverage**: Recent data (2025) under current ULS model

### Remaining Data Gaps
To obtain hospital-level allocations for November 2024 and prior years:
1. **Contact ACSS directly**: Request allocation records (acss@acss.min-saude.pt)
2. **Access SNS Transparency Portal datasets**: Download full data via API
3. **Individual hospital reports**: Review each ULS Relatório e Contas
4. **Ministry of Finance**: Request budget execution details
5. **Freedom of Information request**: Lei de Acesso à Informação Administrativa

---

## UPDATED CAPITAL INJECTION SUMMARY

| Year | Month | Amount (M€) | Hospital Breakdown Available? |
|------|-------|-------------|------------------------------|
| 2009 | Dec | 70 | ❌ No |
| 2019 | Dec | 800 | ❌ No |
| 2020 | Dec | 560 | ❌ No |
| 2021 | Dec | 1,064 | ❌ No |
| 2022 | Jan | 84 | ❌ No |
| 2022 | Dec | 1,022 | ❌ No |
| 2023 | Dec | 1,200 | ❌ No |
| 2024 | Nov | **975.587** | ❌ No (Session 2 finding) |
| 2025 | Jul | 200 | ❌ No |
| 2025 | Oct | **500** | ✅ **YES - Complete** (42 entities) |
| 2025 | Nov | 678 | ❌ No |
| 2025 | Dec | 600 | ❌ No |
| **Total** | - | **10,475.587** | **1 of 12** (8.3%) |

---

## CONCLUSION

The November 2024 capital injection (975.587M€) does not have a publicly available hospital-level breakdown in the Diário da República or press sources. This contrasts with the October 2025 injection (500M€) which has complete detail published in Despacho 12497/2025.

The October 2025 data remains the **only comprehensive hospital-level allocation** publicly available and provides sufficient validation data for PHFSI research.

**Recommendation**: Proceed with manuscript revision using October 2025 as primary validation dataset, supplemented by aggregate timeline (2009-2025) and cyclical pattern evidence from Pita Barros Observatory.

---

**Files Updated**:
- `capital_injections.csv` - Corrected November 2024 entry (date, amount, notes)
- This report created: `DATA_COLLECTION_SESSION_2_FINDINGS.md`
