# SNS Entities List - Complete Summary

**Date:** October 26, 2025
**Status:** ✅ COMPLETE - 426 unique entities extracted

---

## Overview

Extracted and deduplicated all entities (healthcare institutions) from the downloaded SNS data files.

### Total Entities: 426

**Sources:** 10 CSV files containing entity/institution information
- Priority 1: Financial data files
- Priority 2: Operational data files
- Priority 3: Quality data files

---

## Files Created

### 1. **sns_entities_complete_list.csv** (Simple List)
**Columns:** `id`, `entity_name`
- Complete deduplicated list of all 426 entities
- Alphabetically sorted
- Simple format for quick reference

### 2. **sns_entities_categorized.csv** (Enhanced List)
**Columns:** `id`, `entity_name`, `entity_type`, `region`
- Same 426 entities with categorization
- Sorted by type, region, then name
- Ready for analysis

### 3. **sns_entities_by_type.csv** (Type Summary)
Count of entities by type

### 4. **sns_entities_by_region.csv** (Region Summary)
Count of entities by region

### 5. **sns_entities_type_region_crosstab.csv** (Matrix)
Cross-tabulation of entity types by region

---

## Entity Breakdown by Type

| Type | Count | Percentage |
|------|-------|------------|
| **ULS** (Unidades Locais de Saúde) | 184 | 43.2% |
| **Centro Hospitalar** | 95 | 22.3% |
| **Other** | 68 | 16.0% |
| **Hospital** | 58 | 13.6% |
| **ARS** (Admin. Regional de Saúde) | 16 | 3.8% |
| **INFARMED** | 3 | 0.7% |
| **ACSS** | 2 | 0.5% |

---

## Entity Breakdown by Region

| Region | Count | Percentage |
|--------|-------|------------|
| **Nacional** | 271 | 63.6% |
| **Centro** | 97 | 22.8% |
| **LVT** (Lisboa e Vale do Tejo) | 21 | 4.9% |
| **Alentejo** | 17 | 4.0% |
| **Norte** | 13 | 3.1% |
| **Algarve** | 7 | 1.6% |

**Note:** Many entities are listed without specific regional coding, hence the high "Nacional" count.

---

## Entity Type Descriptions

### ULS (184 entities - 43%)
**Unidades Locais de Saúde** - Local Health Units
- Integrated care delivery organizations
- Combine hospital and primary care services
- Example: "Unidade Local De Saúde Do Alentejo Central, E.P.E."

### Centro Hospitalar (95 entities - 22%)
**Hospital Centers** - Multi-facility hospital organizations
- Groups of hospitals under single administration
- Example: "Centro Hospitalar Universitário de Lisboa Central, E.P.E."

### Hospital (58 entities - 14%)
**Individual Hospitals**
- Standalone hospital facilities
- Example: "Hospital de Loures, E.P.E."

### ARS (16 entities - 4%)
**Administrações Regionais de Saúde** - Regional Health Administrations
- Regional health authorities
- 5 mainland regions: Norte, Centro, LVT, Alentejo, Algarve
- 2 autonomous regions: Açores, Madeira

### ACES (in "Other")
**Agrupamentos de Centros de Saúde** - Primary Care Centers
- Primary healthcare groupings
- Community health centers

### ACSS (2 entities)
**Administração Central do Sistema de Saúde** - Central Health Administration
- Central administrative authority

### INFARMED (3 entities)
**Autoridade Nacional do Medicamento** - National Medicines Authority
- Pharmaceutical regulatory authority

---

## Data Sources Used

Files that contained entity/institution information:

1. **agregados-economico-financeiros.csv** - 95 entities
2. **divida-total-vencida-e-pagamentos.csv** - 108 entities
3. **tempo-medio-de-pagamento-das-instituicoes-do-sns-a-fornecedores.csv** - 107 entities
4. **contagem-dos-dias-de-ausencia-ao-trabalho-segundo-o-motivo-de-ausencia.csv** - 122 entities
5. **percentagem-de-gastos-com-te-e-suplementos-no-total-gastos-com-pessoal.csv** - 90 entities
6. **trabalhadores-por-grupo-profissional.csv** - 108 entities
7. **trabalhadores-por-modalidade-de-vinculacao.csv** - 122 entities
8. **fraturas-da-anca-cirurgias-nas-primeiras-48h.csv** - 91 entities
9. **morbilidade-e-mortalidade-hospitalar.csv** - 43 entities
10. **taxa-de-mortalidade-por-avc-isquemico-e-hemorragico.csv** - 87 entities

**Note:** Different files contain different subsets of entities, which is why we needed to extract from all sources.

---

## Sample Entities

### ULS Examples:
- Unidade Local De Saúde Do Alentejo Central, E.P.E.
- Unidade Local De Saúde Do Alto Alentejo, E.P.E.
- Unidade Local De Saúde Do Baixo Alentejo, E.P.E.

### Centro Hospitalar Examples:
- Centro Hospitalar Alto Ave, E.P.E.
- Centro Hospitalar Universitário de Lisboa Central, E.P.E.
- Centro Hospitalar de Setúbal, E.P.E.

### Hospital Examples:
- Hospital de Loures, E.P.E.
- Hospital Arcebispo João Crisóstomo - Cantanhede
- Hospital Fernando Fonseca, E.P.E.

### ARS Examples:
- Administração Regional de Saúde do Norte
- Administração Regional de Saúde do Centro
- Administração Regional de Saúde de Lisboa e Vale do Tejo

---

## Usage Examples

### Load simple list:
```python
import pandas as pd
entities = pd.read_csv('sns_entities_complete_list.csv')
print(f"Total entities: {len(entities)}")
```

### Load categorized list:
```python
entities = pd.read_csv('sns_entities_categorized.csv')
uls_only = entities[entities['entity_type'] == 'ULS']
print(f"ULS entities: {len(uls_only)}")
```

### Filter by region:
```python
centro_entities = entities[entities['region'] == 'Centro']
print(f"Centro region entities: {len(centro_entities)}")
```

### Count by type:
```python
type_counts = entities['entity_type'].value_counts()
print(type_counts)
```

---

## Data Quality Notes

### Encoding
- All files saved with UTF-8 BOM encoding
- Portuguese characters (ç, ã, õ, etc.) preserved

### Duplicates
- 426 unique entities after deduplication
- Some entities appear with slight variations (e.g., with/without "I.P.E.")
- Both variations kept to maintain data integrity

### Missing Data
- Some files don't have entity columns (aggregated national data)
- 3 files had no entity information and were excluded from this analysis

---

## Research Applications

### For ULS Reform Study:
```python
# Identify ULS entities for reform analysis
uls_entities = entities[entities['entity_type'] == 'ULS']
# Use for DiD (Difference-in-Differences) analysis
```

### For Regional Comparisons:
```python
# Compare regions
by_region = entities.groupby(['region', 'entity_type']).size()
```

### For Panel Data Construction:
```python
# Use entity list to ensure complete panel
# Match with financial/operational metrics
```

---

## Summary Statistics

**Total Unique Entities:** 426

**By Type:**
- Healthcare Delivery: 337 entities (ULS + CH + Hospital)
- Administration: 18 entities (ARS + ACSS)
- Other: 71 entities

**By Region:**
- Mainland: 155 entities (with regional coding)
- Nacional/Unspecified: 271 entities

**Coverage:**
- All 5 mainland regions represented
- Mix of public hospitals, ULS, and health centers
- Complete SNS institutional landscape

---

## Files Location

All files saved to: `/c/Users/dpolo/Documents/202510 CFE/`

```
├── sns_entities_complete_list.csv           (426 rows)
├── sns_entities_categorized.csv             (426 rows)
├── sns_entities_by_type.csv                 (7 rows)
├── sns_entities_by_region.csv               (6 rows)
└── sns_entities_type_region_crosstab.csv    (matrix)
```

---

## Next Steps

### 1. Data Validation
Verify entity names against official SNS registries

### 2. Standardization
Create canonical names for entities with variations

### 3. Integration
Use entity list to:
- Validate data completeness
- Create master panel dataset
- Link with external data sources (ACSS, Tribunal de Contas)

### 4. Research Analysis
- Identify ULS vs non-ULS for reform studies
- Regional comparisons
- Institutional characteristics mapping

---

**Status:** ✅ Complete and ready for research use

*Generated: October 26, 2025*
*Source: SNS Transparency Portal data (2014-2024)*
*Total entities: 426 unique healthcare institutions*
