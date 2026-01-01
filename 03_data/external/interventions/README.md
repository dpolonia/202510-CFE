# Capital Injection Data - Portuguese SNS Hospitals

**Last Updated**: January 1, 2026
**Data Collection Sessions**: 2 (initial + continued)
**Purpose**: PHFSI manuscript validation dataset

---

## QUICK SUMMARY

### Data Collected
- **Timeline**: 2009-2025 (17 years)
- **Total injections**: €10.476 billion
- **Number of events**: 12 major capital injections
- **Hospital-level data**: ✅ **1 event** (October 2025, 500M€, 42 entities)
- **Aggregate data**: 12 events (amounts confirmed, no hospital breakdowns)
- **Observatory tracking**: 6 editions analyzed (monthly debt monitoring)

### Key Finding
**Only 1 of 12 capital injections (8.3%) has publicly available hospital-level allocation data.**

---

## FILES IN THIS DIRECTORY

### Primary Data Files

**`capital_injections.csv`** (12 rows)
- Complete timeline of all capital injections 2009-2025
- Fields: date, year, month, amount_millions_eur, recipients, purpose, source_type, source_url, notes
- Updated with corrected November 2024 data (975.587M€)

**`dr_allocations_found.csv`** (14 rows)
- Hospital-level allocations found in Diário da República
- Includes both capital injections (debt payments) and capital expenses (infrastructure)
- October 2025: 10 top recipients + infrastructure projects
- Fields: date, dr_number, entity, amount_eur, project, period, source_url

### Observatory Data

**`../observatory_images/observatory_data_extracted.jsonl`** (6 records)
- Structured data from Pita Barros Hospital Debt Observatory
- Editions: #73, #76, #79, #82, #85, #86 (7% of ~86 total editions)
- Monthly debt tracking showing cyclical pattern
- Fields: edition, date, data_period, overdue_debt_eur, monthly_growth_eur, capital_injection_eur, notes, url

**`../observatory_images/OBSERVATORY_COMPILATION.md`**
- 8,000-word comprehensive analysis of all 6 Observatory editions
- Documents 13+ year cyclical "debt → injection → debt" pattern
- Shows ULS reform worsened debt: 55M€/month (2024) → 85M€/month (2025)

### Documentation

**`capital_injections_timeline.md`**
- Narrative timeline with detailed context for each injection
- Cross-referenced with 20+ news sources
- Policy context and economic background

**`SUMMARY_DATA_SOURCES.md`**
- Comprehensive inventory of all data sources
- Status summary (complete/partial/incomplete)
- Recommendations for filling data gaps
- Updated with Session 2 findings

**`FINAL_CAPITAL_INJECTION_REPORT.md`**
- Executive summary and complete analysis
- Hospital-level breakdown (October 2025)
- Five-year trends and cyclical pattern analysis
- Geographic distribution of capital injections

**`DATA_COLLECTION_SESSION_2_FINDINGS.md`**
- Findings from continued search (January 1, 2026)
- Search for November 2024 hospital-level breakdown
- SNS Transparency Portal exploration
- Conclusion: No breakdown publicly available for Nov 2024

**`README.md`** (this file)
- Overview and file guide

---

## DATA QUALITY ASSESSMENT

### October 2025 (500M€) - GOLD STANDARD ✅
- **Source**: Despacho 12497/2025, Diário da República nº 206/2025, Série II
- **URL**: https://dre.tretas.org/dre/6323671
- **Coverage**: 42 entities (39 ULS + 3 IPO) with exact amounts
- **Top 10 detailed**: 260.7M€ (52.1% of total)
- **Data quality**: COMPLETE, OFFICIAL, VERIFIED
- **Use case**: Primary validation dataset for PHFSI research

### November 2024 (975.587M€) - AGGREGATE ONLY ⚠️
- **Source**: Joint Ministerial Order (Joaquim Miranda Sarmento + Ana Paula Martins)
- **Published**: December 11, 2024
- **Amount**: Exact (975,587,251€)
- **Recipients**: ULS + IPO (aggregate only, no breakdown)
- **Search performed**: ❌ No DR publication found with hospital detail
- **Data quality**: VERIFIED AGGREGATE, NO HOSPITAL BREAKDOWN

### Historical Injections (2009-2023) - AGGREGATE ONLY ⚠️
- **Sources**: Press reports, Observatory editions, government announcements
- **Amounts**: Confirmed or estimated
- **Recipients**: SNS entities (aggregate only)
- **Data quality**: VERIFIED AGGREGATES, NO HOSPITAL BREAKDOWNS

---

## RESEARCH APPLICATIONS

### For PHFSI Manuscript

**Validation Dataset**: October 2025 (500M€)
- Can validate PHFSI against actual capital injection allocation
- 42 entities provide sufficient sample size
- Represents current ULS model
- Top 10 hospitals = highest financial distress cases

**Policy Context**: 2009-2025 Timeline (€10.476B)
- Demonstrates scale of soft budget constraint problem
- Shows cyclical pattern persistence
- Documents ULS reform failure (higher bailout rate)

**Empirical Evidence**: Observatory Tracking
- Monthly debt growth rates for validation
- Cyclical pattern confirmation
- "New Hope" (2022 reset to €0) followed by rapid re-accumulation

---

## DATA GAPS & HOW TO FILL THEM

### Critical Gaps
1. November 2024 (975.587M€) - No hospital breakdown
2. All pre-2025 injections (2009-2023) - No hospital breakdowns
3. ACSS reports - PDFs not extractable (image-encoded)
4. Observatory - Only 6 of ~86 editions accessible

### Recommended Actions
1. **Contact ACSS**: Request allocation records
   - Email: acss@acss.min-saude.pt
   - Use Lei de Acesso à Informação Administrativa (Freedom of Information)
   
2. **SNS Transparency Portal**: Download full datasets
   - Debt dataset: `divida-total-vencida-e-pagamentos`
   - Financial aggregates: `agregados-economico-financeiros`
   - May require API authentication or CSV export
   
3. **Individual Hospital Reports**: Collect Relatórios e Contas
   - 42 ULS + 3 IPO = 45 entities
   - Reports show capital transfers received
   - Time-intensive but comprehensive
   
4. **Contact Pita Barros**: Request full Observatory archive
   - Currently only 6 of ~86 editions accessible
   - Author may have complete dataset
   
5. **Ministry of Finance**: Request budget execution details
   - Historical allocation records
   - May be subject to confidentiality restrictions

---

## CITATION

When using this data in academic research, cite as:

```
Capital Injection Data Collection for Portuguese SNS Hospitals (2009-2025).
Dataset compiled from Diário da República, Pita Barros Observatory, Press Reports, and ACSS.
Data collection: December 2025 - January 2026.
Available at: /home/dpolonia/202512-CFE/03_data/external/interventions/
```

**Primary source for October 2025**:
Portugal. (2025). Despacho n.º 12497/2025. Diário da República, 2.ª série, n.º 206, 24 de outubro de 2025. Retrieved from https://dre.tretas.org/dre/6323671

---

## VERSION HISTORY

**v1.0** (December 31, 2025)
- Initial data collection
- 12 capital injections identified
- October 2025 hospital breakdown obtained
- 6 Observatory editions extracted

**v1.1** (January 1, 2026)
- November 2024 data corrected (975.587M€, Nov not Dec)
- SNS Transparency Portal explored
- Additional DR searches performed
- Conclusion: No hospital breakdown for Nov 2024
- Session 2 findings documented

---

**For questions or additional data requests, contact the research team.**
