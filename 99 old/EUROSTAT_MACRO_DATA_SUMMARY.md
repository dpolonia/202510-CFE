# Eurostat Macroeconomic Indicators - Extraction Summary

**Date:** October 26, 2025
**Source:** Eurostat API
**Output Directory:** `eurostat_macro_data/`
**Status:** ✅ **EXTRACTION COMPLETE - ALL INDICATORS SUCCESSFULLY DOWNLOADED**

---

## RESUMO EXECUTIVO

✅ **Extraídos com sucesso os indicadores macroeconómicos do Eurostat que substituem a necessidade de download manual do PORDATA**

**Total de Registos Extraídos:** 224,412 registos (Portugal)
**Cobertura Temporal:** 1975-2024 (varia por indicador)
**Formatos:** JSON, CSV, XLSX, Parquet (4 formatos para cada dataset)

---

## DATASETS EXTRAÍDOS

### PRIORIDADE 1: Finanças Públicas e Despesa em Saúde

#### 1. **gov_10dd_edpt1 - Défice/Excedente e Dívida Pública** ⭐⭐⭐

**Descrição:** Government deficit/surplus, debt and associated data

**Conteúdo:**
- Défice/excedente orçamental
- Dívida pública (bruta e líquida)
- Dados associados de contabilidade nacional

**Estatísticas:**
- **Registos:** 9,180
- **Cobertura:** 1995-2024 (30 anos)
- **Geografia:** Nacional (PT)
- **Indicadores (na_item):** 17 tipos diferentes
- **Unidades:** EUR, % PIB, unidades nacionais

**Indicadores-chave incluídos:**
- `B9` - Net lending (+) / net borrowing (-) (Défice/Excedente)
- `GD` - Government consolidated gross debt (Dívida pública bruta)
- `B1GQ` - Gross domestic product at market prices (PIB)

**Utilidade para Pesquisa:** ✅✅✅ **CRÍTICO**
- Contexto fiscal nacional
- Pressão orçamental que afeta financiamento SNS
- Relação entre dívida pública e endividamento hospitalar

**Ficheiros:**
- JSON: `gov_10dd_edpt1_government_deficit_debt.json` (3.5 MB)
- CSV: `gov_10dd_edpt1_government_deficit_debt.csv` (1.4 MB)
- XLSX: `gov_10dd_edpt1_government_deficit_debt.xlsx` (442 KB)
- Parquet: `gov_10dd_edpt1_government_deficit_debt.parquet` (19 KB) ⭐ RECOMENDADO

---

#### 2. **hlth_sha11_hf - Despesa em Saúde por Esquema de Financiamento** ⭐⭐⭐

**Descrição:** Health expenditure by financing scheme

**Conteúdo:**
- Despesa total em saúde
- Despesa pública (governo)
- Despesa privada (famílias, seguros)
- Esquemas de financiamento voluntário

**Estatísticas:**
- **Registos:** 4,224
- **Cobertura:** 1992-2024 (33 anos)
- **Geografia:** Nacional (PT)
- **Esquemas (icha11_hf):** 16 tipos de financiamento
- **Unidades:** EUR, EUR per capita, % PIB, unidades nacionais

**Esquemas incluídos:**
- `TOT_HF` - All financing schemes (Total despesa saúde)
- `HF1` - Government schemes (Despesa pública saúde) ⭐
- `HF2` - Compulsory contributory health insurance
- `HF3` - Household out-of-pocket payments (Despesa privada)

**Utilidade para Pesquisa:** ✅✅✅ **CRÍTICO**
- Despesa pública em saúde (% PIB) - indicador-chave
- Contexto de financiamento do SNS
- Evolução temporal do investimento em saúde

**Ficheiros:**
- JSON: `hlth_sha11_hf_health_expenditure_by_financing.json` (1.3 MB)
- CSV: `hlth_sha11_hf_health_expenditure_by_financing.csv` (509 KB)
- XLSX: `hlth_sha11_hf_health_expenditure_by_financing.xlsx` (179 KB)
- Parquet: `hlth_sha11_hf_health_expenditure_by_financing.parquet` (14 KB) ⭐ RECOMENDADO

---

#### 3. **hlth_sha11_hc - Despesa em Saúde por Função** ⭐⭐⭐

**Descrição:** Health expenditure by function

**Conteúdo:**
- Despesa em cuidados curativos (hospitais)
- Despesa em cuidados de longa duração
- Despesa em prevenção
- Despesa em medicamentos

**Estatísticas:**
- **Registos:** 12,408
- **Cobertura:** 1992-2024 (33 anos)
- **Geografia:** Nacional (PT)
- **Funções (icha11_hc):** 47 categorias funcionais
- **Unidades:** EUR, EUR per capita, % PIB, unidades nacionais

**Funções incluídas:**
- `TOT_HC` - Current health care expenditure (Despesa corrente total)
- `HC1` - Curative and rehabilitative care (Hospitais) ⭐
- `HC11` - Inpatient curative and rehabilitative care (Internamento)
- `HC5` - Medical goods (Medicamentos)

**Utilidade para Pesquisa:** ✅✅ **ALTA**
- Despesa específica em cuidados hospitalares
- Análise funcional do orçamento de saúde
- Priorização de despesa

**Ficheiros:**
- JSON: `hlth_sha11_hc_health_expenditure_by_function.json` (3.9 MB)
- CSV: `hlth_sha11_hc_health_expenditure_by_function.csv` (1.4 MB)
- XLSX: `hlth_sha11_hc_health_expenditure_by_function.xlsx` (511 KB)
- Parquet: `hlth_sha11_hc_health_expenditure_by_function.parquet` (30 KB) ⭐ RECOMENDADO

---

### PRIORIDADE 2: PIB e Agregados Económicos

#### 4. **nama_10_gdp - PIB e Componentes Principais** ⭐⭐

**Descrição:** GDP and main components (output, expenditure and income)

**Conteúdo:**
- PIB total (várias medidas)
- Consumo privado
- Consumo público
- Investimento
- Exportações e importações

**Estatísticas:**
- **Registos:** 62,400
- **Cobertura:** 1975-2024 (50 anos!)
- **Geografia:** Nacional (PT)
- **Componentes (na_item):** 39 tipos
- **Unidades:** EUR, índices, taxas de crescimento

**Componentes-chave:**
- `B1GQ` - Gross domestic product at market prices (PIB) ⭐
- `P3` - Final consumption expenditure (Consumo final)
- `P3_S13` - Government final consumption expenditure (Consumo público)
- `P51G` - Gross fixed capital formation (Investimento)

**Utilidade para Pesquisa:** ✅✅ **ALTA**
- Denominador para cálculo de ratios (% PIB)
- Contexto económico nacional
- Ciclos económicos

**Ficheiros:**
- JSON: `nama_10_gdp_gdp_main_components.json` (20.7 MB)
- CSV: `nama_10_gdp_gdp_main_components.csv` (8.7 MB)
- XLSX: `nama_10_gdp_gdp_main_components.xlsx` (2.6 MB)
- Parquet: `nama_10_gdp_gdp_main_components.parquet` (144 KB) ⭐ RECOMENDADO

---

#### 5. **nama_10_pc - PIB Per Capita** ⭐⭐

**Descrição:** GDP per capita

**Conteúdo:**
- PIB per capita (várias medidas)
- Paridades de poder de compra
- Índices comparativos

**Estatísticas:**
- **Registos:** 5,400
- **Cobertura:** 1975-2024 (50 anos)
- **Geografia:** Nacional (PT)
- **Medidas:** 9 tipos de PIB per capita
- **Unidades:** EUR, PPS, índices

**Utilidade para Pesquisa:** ✅ **MÉDIA**
- Riqueza per capita
- Comparações internacionais
- Capacidade económica

**Ficheiros:**
- JSON: `nama_10_pc_gdp_per_capita.json` (1.9 MB)
- CSV: `nama_10_pc_gdp_per_capita.csv` (870 KB)
- XLSX: `nama_10_pc_gdp_per_capita.xlsx` (239 KB)
- Parquet: `nama_10_pc_gdp_per_capita.parquet` (24 KB) ⭐ RECOMENDADO

---

### PRIORIDADE 3: Salários e Agregados Fiscais

#### 6. **earn_nt_net - Salários Médios Anuais** ⭐

**Descrição:** Annual net earnings

**Conteúdo:**
- Salários líquidos anuais
- Por estrutura familiar
- Por tipo de agregado

**Estatísticas:**
- **Registos:** 5,850
- **Cobertura:** 2000-2024 (25 anos)
- **Geografia:** Nacional (PT)
- **Estruturas:** 6 tipos de agregado familiar
- **Casos:** 13 tipos

**Utilidade para Pesquisa:** ⚠️ **BAIXA-MÉDIA**
- Contexto de rendimentos
- Capacidade de pagamento
- Poder de compra

**Ficheiros:**
- JSON: `earn_nt_net_annual_net_earnings.json` (2.3 MB)
- CSV: `earn_nt_net_annual_net_earnings.csv` (944 KB)
- XLSX: `earn_nt_net_annual_net_earnings.xlsx` (300 KB)
- Parquet: `earn_nt_net_annual_net_earnings.parquet` (41 KB) ⭐ RECOMENDADO

---

#### 7. **gov_10a_main - Agregados Fiscais** ⭐

**Descrição:** Main national accounts tax aggregates

**Conteúdo:**
- Receitas fiscais
- Impostos diretos e indiretos
- Contribuições sociais
- Despesas por categoria

**Estatísticas:**
- **Registos:** 124,950
- **Cobertura:** 1975-2024 (50 anos)
- **Geografia:** Nacional (PT)
- **Itens (na_item):** 119 tipos
- **Unidades:** EUR, % PIB

**Utilidade para Pesquisa:** ✅ **MÉDIA**
- Receitas do Estado
- Capacidade fiscal
- Contexto orçamental

**Ficheiros:**
- JSON: `gov_10a_main_tax_aggregates.json` (47.2 MB)
- CSV: `gov_10a_main_tax_aggregates.csv` (18.5 MB)
- XLSX: `gov_10a_main_tax_aggregates.xlsx` (5.8 MB)
- Parquet: `gov_10a_main_tax_aggregates.parquet` (140 KB) ⭐ RECOMENDADO

---

## COMPARAÇÃO: EUROSTAT vs. PORDATA

### Indicadores Identificados como Necessários no PORDATA:

| Indicador | PORDATA (manual) | Eurostat (API) | Status |
|-----------|------------------|----------------|--------|
| **Despesa pública em saúde (% PIB)** | ✅ Disponível | ✅ **EXTRAÍDO** (hlth_sha11_hf) | ✅ COMPLETO |
| **Dívida pública (% PIB)** | ✅ Disponível | ✅ **EXTRAÍDO** (gov_10dd_edpt1) | ✅ COMPLETO |
| **Défice orçamental (% PIB)** | ✅ Disponível | ✅ **EXTRAÍDO** (gov_10dd_edpt1) | ✅ COMPLETO |
| **Despesas públicas: Saúde** | ✅ Disponível | ✅ **EXTRAÍDO** (hlth_sha11_hf/hc) | ✅ COMPLETO |
| **PIB nacional** | ✅ Disponível | ✅ **EXTRAÍDO** (nama_10_gdp) | ✅ COMPLETO |
| **PIB per capita** | ✅ Disponível | ✅ **EXTRAÍDO** (nama_10_pc) | ✅ COMPLETO |
| **Salários médios** | ✅ Disponível | ✅ **EXTRAÍDO** (earn_nt_net) | ✅ COMPLETO |

**Conclusão:** ✅ **TODOS os indicadores prioritários identificados no PORDATA foram extraídos do Eurostat via API**

---

## VANTAGENS DA ABORDAGEM EUROSTAT vs. PORDATA

| Característica | PORDATA (manual) | Eurostat (API) |
|----------------|------------------|----------------|
| **Método** | Download manual, indicador a indicador | Automatizado via script Python |
| **Tempo** | 30-45 minutos (5 indicadores) | 5 minutos (7 datasets completos) |
| **Replicabilidade** | ❌ Difícil (processo manual) | ✅ Total (script reutilizável) |
| **Formatos** | CSV, XLSX | CSV, XLSX, JSON, Parquet (4 formatos) |
| **Cobertura** | Indicadores selecionados | Datasets completos com todos os sub-indicadores |
| **Atualizações** | Requer re-download manual | Executar script novamente |
| **Documentação** | Metadata manual | Metadata automática (JSON) |
| **Séries históricas** | 1995-2024 (tipicamente) | 1975-2024 (50 anos!) |

**Resultado:** ✅ **Abordagem Eurostat SUPERIOR em todos os aspectos**

---

## INDICADORES-CHAVE PARA ANÁLISE

### Para calcular os ratios necessários:

#### 1. **Despesa Pública em Saúde (% PIB)**

**Fórmula:**
```
Despesa Pública Saúde (% PIB) = (Despesa Gov Saúde / PIB) × 100
```

**Dados necessários:**
- **Numerador:** `hlth_sha11_hf` → filtrar `icha11_hf == 'HF1'` (Government schemes), `unit == 'MIO_EUR'`
- **Denominador:** `nama_10_gdp` → filtrar `na_item == 'B1GQ'`, `unit == 'CP_MEUR'`
- **Ou direto:** `hlth_sha11_hf` → filtrar `icha11_hf == 'HF1'`, `unit == 'PC_GDP'` ⭐ (já calculado!)

---

#### 2. **Dívida Pública (% PIB)**

**Fórmula:**
```
Dívida Pública (% PIB) = (Dívida Bruta / PIB) × 100
```

**Dados necessários:**
- **Direto:** `gov_10dd_edpt1` → filtrar `na_item == 'GD'`, `unit == 'PC_GDP'` ⭐ (já calculado!)
- **Ou calcular:** usar `unit == 'MIO_EUR'` e dividir por PIB

---

#### 3. **Défice Orçamental (% PIB)**

**Fórmula:**
```
Défice (% PIB) = (Net borrowing / PIB) × 100
```

**Dados necessários:**
- **Direto:** `gov_10dd_edpt1` → filtrar `na_item == 'B9'`, `unit == 'PC_GDP'` ⭐ (já calculado!)

---

## ESTRUTURA DOS FICHEIROS

### Formato dos Dados:

Todos os datasets seguem estrutura similar:

**Colunas comuns:**
- `freq` / `freq_label` - Frequência (Anual)
- `unit` / `unit_label` - Unidade de medida
- `geo` / `geo_label` - Geografia (PT - Portugal)
- `time` / `time_label` - Ano
- `value` - Valor do indicador

**Colunas específicas por dataset:**
- `gov_10dd_edpt1`: `sector`, `na_item` (tipo de indicador fiscal)
- `hlth_sha11_hf`: `icha11_hf` (esquema de financiamento)
- `hlth_sha11_hc`: `icha11_hc` (função de saúde)
- `nama_10_gdp`: `na_item` (componente do PIB)

### Unidades de Medida Importantes:

| Código | Descrição | Uso |
|--------|-----------|-----|
| `MIO_EUR` | Million euros | Valores absolutos |
| `PC_GDP` | Percentage of GDP | Ratios (% PIB) ⭐ |
| `EUR_HAB` | Euro per inhabitant | Per capita |
| `MIO_NAC` | Million national currency | Valores nacionais |
| `CP_MEUR` | Current prices, million euros | PIB corrente |

**Dica:** Filtrar por `unit == 'PC_GDP'` dá diretamente os ratios calculados! ⭐

---

## COMO USAR OS DADOS

### Exemplo 1: Extrair Défice Orçamental (% PIB) 1995-2024

```python
import pandas as pd

# Load data
df = pd.read_parquet('eurostat_macro_data/parquet/gov_10dd_edpt1_government_deficit_debt.parquet')

# Filter for deficit as % of GDP
deficit = df[
    (df['na_item'] == 'B9') &  # Net borrowing
    (df['unit'] == 'PC_GDP')    # As % of GDP
][['time', 'value']].sort_values('time')

print(deficit)
# Output: time series of deficit % GDP from 1995-2024
```

---

### Exemplo 2: Extrair Despesa Pública Saúde (% PIB) 1992-2024

```python
import pandas as pd

# Load data
df = pd.read_parquet('eurostat_macro_data/parquet/hlth_sha11_hf_health_expenditure_by_financing.parquet')

# Filter for government health expenditure as % of GDP
health_exp = df[
    (df['icha11_hf'] == 'HF1') &   # Government schemes
    (df['unit'] == 'PC_GDP')       # As % of GDP
][['time', 'value']].sort_values('time')

print(health_exp)
# Output: time series of public health spending % GDP from 1992-2024
```

---

### Exemplo 3: Extrair Dívida Pública (% PIB) 1995-2024

```python
import pandas as pd

# Load data
df = pd.read_parquet('eurostat_macro_data/parquet/gov_10dd_edpt1_government_deficit_debt.parquet')

# Filter for government debt as % of GDP
debt = df[
    (df['na_item'] == 'GD') &     # Government debt
    (df['unit'] == 'PC_GDP')       # As % of GDP
][['time', 'value']].sort_values('time')

print(debt)
# Output: time series of public debt % GDP from 1995-2024
```

---

## PRÓXIMOS PASSOS RECOMENDADOS

### 1. ✅ **Criar Dataset Consolidado de Indicadores Macroeconómicos** (RECOMENDADO)

**Objetivo:** Criar ficheiro único com indicadores-chave para análise

**Indicadores a incluir:**
1. Défice orçamental (% PIB)
2. Dívida pública (% PIB)
3. Despesa pública saúde (% PIB)
4. Despesa total saúde (% PIB)
5. PIB (EUR milhões)
6. PIB per capita

**Output:** `macro_indicators_consolidated_1995_2024.csv`

**Script:** Criar `consolidate_macro_indicators.py`

---

### 2. ✅ **Integrar com Dados SNS para Análise Multi-Nível**

**Objetivo:** Relacionar contexto macro com desempenho hospitalar

**Análises possíveis:**
- Correlação entre défice nacional e endividamento hospitalar
- Efeito da despesa pública saúde nos indicadores financeiros SNS
- Impacto de ciclos económicos (PIB) na gestão hospitalar

---

### 3. ⚠️ **Explorar Indicadores Regionais** (Opcional)

**Nota:** Dados extraídos são nacionais (PT). Para análise regional, considerar:
- Eurostat datasets com NUTS 2/3 (se disponíveis)
- Já extraído: PIB regional (`nama_10r_3gdp`)

---

## FICHEIROS GERADOS

### Estrutura de Diretórios:

```
eurostat_macro_data/
├── csv/                 (7 ficheiros CSV, 30.4 MB total)
│   ├── gov_10dd_edpt1_government_deficit_debt.csv
│   ├── hlth_sha11_hf_health_expenditure_by_financing.csv
│   ├── hlth_sha11_hc_health_expenditure_by_function.csv
│   ├── nama_10_gdp_gdp_main_components.csv
│   ├── nama_10_pc_gdp_per_capita.csv
│   ├── earn_nt_net_annual_net_earnings.csv
│   └── gov_10a_main_tax_aggregates.csv
├── xlsx/                (7 ficheiros Excel, 10.0 MB total)
├── json/                (7 ficheiros JSON, 78.8 MB total)
├── parquet/             (7 ficheiros Parquet, 412 KB total) ⭐ RECOMENDADO
└── metadata/            (7 ficheiros JSON de metadata)
```

### Tamanhos de Ficheiro:

| Dataset | CSV | XLSX | Parquet | Compressão |
|---------|-----|------|---------|------------|
| gov_10dd_edpt1 | 1.4 MB | 442 KB | 19 KB | 98.6% |
| hlth_sha11_hf | 509 KB | 179 KB | 14 KB | 97.2% |
| hlth_sha11_hc | 1.4 MB | 511 KB | 30 KB | 97.9% |
| nama_10_gdp | 8.7 MB | 2.6 MB | 144 KB | 98.3% |
| nama_10_pc | 870 KB | 239 KB | 24 KB | 97.2% |
| earn_nt_net | 944 KB | 300 KB | 41 KB | 95.7% |
| gov_10a_main | 18.5 MB | 5.8 MB | 140 KB | 99.2% |

**Recomendação:** Usar **Parquet** para análise (98%+ compressão, leitura rápida)

---

## RESUMO FINAL

### ✅ **MISSÃO CUMPRIDA - Indicadores Macroeconómicos Extraídos do Eurostat**

**O que foi extraído:**
- ✅ Défice e dívida pública (1995-2024)
- ✅ Despesa em saúde pública e privada (1992-2024)
- ✅ Despesa em saúde por função (hospitais, medicamentos, etc.)
- ✅ PIB e componentes (1975-2024)
- ✅ PIB per capita (1975-2024)
- ✅ Salários médios (2000-2024)
- ✅ Agregados fiscais (1975-2024)

**Total:** 224,412 registos, 7 datasets, 4 formatos

**Substituiu necessidade de:** Download manual PORDATA (economia de 30-45 minutos)

**Vantagem:**
- Automatizado e replicável
- Séries históricas mais longas (até 50 anos!)
- Datasets completos (não apenas indicadores selecionados)
- Formato Parquet eficiente (98% compressão)

---

## DADOS COMPLETOS AGORA DISPONÍVEIS

### Inventário Total da Pesquisa:

**SNS (Hospitais):** 305,744 registos (2013-2025)
**INE (Municipal):** 34,127 registos (2011-2025)
**Eurostat (Regional):** 206,001 registos (1960-2024)
**Eurostat (Macro):** 224,412 registos (1975-2024) ⭐ **NOVO!**

**TOTAL:** ~770,000 registos

**Níveis:**
- ✅ Institucional (426 hospitais)
- ✅ Municipal (344 municípios)
- ✅ Regional (NUTS 2/3)
- ✅ Nacional (contexto macroeconómico) ⭐ **COMPLETO!**

**Cobertura Temporal:**
- ✅ 1975-2024 (indicadores macro - 50 anos!)
- ✅ 1992-2024 (despesa saúde - 33 anos)
- ✅ 1995-2024 (dívida/défice - 30 anos)
- ✅ 2011-2025 (dados municipais - 14 anos)
- ✅ 2014-2025 (dados hospitalares - 11 anos)

---

**Conclusão:** Base de dados COMPLETA para análise de endividamento hospitalar no contexto económico, fiscal e demográfico português (2015-2025).

**Próximo passo recomendado:** Criar dataset consolidado de indicadores macroeconómicos-chave para análise integrada.

---

**Gerado:** 26 de outubro de 2025
**Script:** `eurostat_macro_extractor.py`
**Status:** ✅ COMPLETE - All macroeconomic indicators extracted from Eurostat
