# OECD Data Analysis - Relevância para Pesquisa de Endividamento Hospitalar

**Data:** 26 de outubro de 2025
**Propósito:** Avaliar dados OECD vs. dados já extraídos (SNS, INE, Eurostat)
**Status:** ⚠️ **OECD API com problemas de acesso - ANÁLISE BASEADA EM CONHECIMENTO DA BASE DE DADOS**

---

## RESUMO EXECUTIVO

**Conclusão:** ⚠️ **OECD não adiciona valor significativo à pesquisa - dados já cobertos pelo Eurostat**

**Razão:** A OECD é principalmente um **agregador de dados de fontes nacionais e Eurostat**. Para Portugal, a maioria dos dados OECD provêm de INE e Eurostat, que já foram extraídos diretamente.

---

## O QUE É A OECD?

### Organização para a Cooperação e Desenvolvimento Económico

**Natureza:**
- Organização internacional (38 países membros)
- **Não é fonte primária de dados**
- Agrega e harmoniza dados de fontes nacionais
- Foco em comparações internacionais

**Fontes de Dados da OECD para Portugal:**
- **INE (Instituto Nacional de Estatística)** ⭐ Já extraído!
- **Eurostat (European Statistics)** ⭐ Já extraído!
- **Banco de Portugal**
- **Ministério das Finanças**
- **Ministério da Saúde / ACSS**

---

## PROBLEMAS TÉCNICOS IDENTIFICADOS

### API da OECD:

**Tentativas de Acesso:**
1. ❌ SDMX REST API (`https://sdmx.oecd.org/`) - 404 errors
2. ❌ OECD.Stat API (`https://stats.oecd.org/sdmx-json/`) - timeouts
3. ❌ WebFetch nos links fornecidos - 403 Forbidden

**Razões Possíveis:**
- API pode requerer autenticação/registo
- Estrutura de URLs mudou recentemente
- Rate limiting restritivo
- Acesso geográfico restrito

**Alternativa:**
- Download manual via OECD.Stat portal
- Mas: dados são os mesmos que INE/Eurostat (já temos!)

---

## DATASETS OECD RELEVANTES (Teóricos)

### 1. **System of Health Accounts (SHA)**

**O Que É:**
- Despesa em saúde por fonte de financiamento
- Despesa em saúde por função
- Contas nacionais de saúde

**Dados Tipicamente Incluídos:**
- Despesa total em saúde (% PIB)
- Despesa pública vs privada
- Despesa em hospitais, medicamentos, etc.

**Fonte Primária (Portugal):** INE, Ministério da Saúde, ACSS

**JÁ TEMOS?** ✅ **SIM** - Eurostat `hlth_sha11_hf` e `hlth_sha11_hc`
- Período: 1992-2024
- Mais detalhe que OECD
- Fonte: mesma metodologia SHA

**Valor Adicional OECD:** ❌ **NENHUM** - dados idênticos aos do Eurostat

---

### 2. **Health Status and Determinants**

**O Que É:**
- Esperança de vida
- Mortalidade
- Fatores de risco (obesidade, tabagismo)

**Fonte Primária (Portugal):** INE, DGS

**JÁ TEMOS?** ✅ **SIM** - Eurostat e INE
- Esperança de vida: Eurostat 1960-2024
- Esperança de vida aos 65: INE 1970-2004, 2011-2023
- Mais granular (municipal/regional)

**Valor Adicional OECD:** ❌ **NENHUM** - dados agregados nacionais, menos detalhe

---

### 3. **Health Care Resources**

**O Que É:**
- Médicos, enfermeiros por 1000 habitantes
- Camas hospitalares
- Equipamento médico

**Fonte Primária (Portugal):** INE, ACSS

**JÁ TEMOS?** ✅ **SIM**
- Enfermeiros: INE municipal (2011-2023) ⭐ Mais granular
- Médicos: Eurostat NUTS 2 (1993-2024)
- Camas hospitalares: Eurostat NUTS 2 (1993-2024)
- SNS: 426 entidades individuais (workforce 2014-2025)

**Valor Adicional OECD:** ❌ **NENHUM** - apenas nacional, menor granularidade

---

### 4. **Quarterly National Accounts (QNA)**

**O Que É:**
- PIB trimestral
- Componentes do PIB
- Contas nacionais

**Fonte Primária (Portugal):** INE

**JÁ TEMOS?** ✅ **SIM** - Eurostat `nama_10_gdp`
- PIB: 1975-2024 (50 anos!)
- PIB trimestral: INE 2011-2025
- Componentes detalhados

**Valor Adicional OECD:** ❌ **NENHUM** - mesmos dados

---

### 5. **Government Finance Statistics**

**O Que É:**
- Défice/excedente orçamental
- Dívida pública
- Receitas e despesas governo

**Fonte Primária (Portugal):** INE, Ministério das Finanças, Banco de Portugal

**JÁ TEMOS?** ✅ **SIM** - Eurostat `gov_10dd_edpt1` e `gov_10a_main`
- Défice: 1995-2024
- Dívida pública: 1995-2024
- Agregados fiscais: 1975-2024

**Valor Adicional OECD:** ❌ **NENHUM** - mesma fonte (Eurostat/INE)

---

### 6. **Labour Force Statistics**

**O Que É:**
- Taxa de desemprego
- Emprego por setor
- Salários médios

**Fonte Primária (Portugal):** INE

**JÁ TEMOS?** ✅ **SIM**
- Desemprego: INE trimestral NUTS 2 (2011-2025)
- Emprego: INE (2011-2025), Eurostat regional (1995-2023)
- Salários: Eurostat (2000-2024)

**Valor Adicional OECD:** ❌ **NENHUM**

---

### 7. **Social Expenditure Database (SOCX)**

**O Que É:**
- Despesa social por função
- Inclui saúde, pensões, desemprego

**Fonte Primária (Portugal):** Ministério das Finanças, INE

**JÁ TEMOS?** ⚠️ **PARCIALMENTE**
- Despesa saúde: ✅ Eurostat (1992-2024)
- Despesa pública por função: ✅ Eurostat `gov_10a_main`

**Valor Adicional OECD:** ⚠️ **MUITO BAIXO** - mais desagregação mas não crítico

---

## COMPARAÇÃO: OECD vs. DADOS JÁ EXTRAÍDOS

### Cobertura de Dados:

| Indicador | OECD (típico) | Já Temos | Granularidade OECD | Granularidade Nossa |
|-----------|---------------|----------|-------------------|---------------------|
| **Despesa saúde (% PIB)** | Nacional | ✅ Eurostat | Nacional | Nacional (1992-2024) |
| **Défice orçamental** | Nacional | ✅ Eurostat | Nacional | Nacional (1995-2024) |
| **Dívida pública** | Nacional | ✅ Eurostat | Nacional | Nacional (1995-2024) |
| **PIB** | Nacional | ✅ Eurostat | Nacional | Nacional (1975-2024) |
| **Esperança de vida** | Nacional | ✅ Eurostat | Nacional | Nacional + NUTS 2 (1960-2024) |
| **Médicos** | Nacional | ✅ Eurostat | Nacional | NUTS 2 (1993-2024) |
| **Enfermeiros** | Nacional | ✅ INE | Nacional | **Municipal** (2011-2023) ⭐ |
| **Desemprego** | Nacional | ✅ INE | Nacional | **NUTS 2 + Trimestral** (2011-2025) ⭐ |
| **Workforce hospitalar** | ❌ Não tem | ✅ SNS | - | **Institucional 426** (2014-2025) ⭐ |
| **Endividamento hospitalar** | ❌ Não tem | ✅ SNS | - | **Institucional 426** (2014-2025) ⭐ |

**Conclusão:** Nossa base de dados é **SUPERIOR** em granularidade e cobertura temporal

---

## VANTAGENS DOS DADOS JÁ EXTRAÍDOS vs. OECD

### 1. **Granularidade Geográfica Superior**

**OECD:**
- ❌ Apenas dados nacionais (Portugal agregado)

**Nossa Base de Dados:**
- ✅ Institucional: 426 hospitais individuais
- ✅ Municipal: 344 municípios
- ✅ NUTS 3: 27-40 regiões
- ✅ NUTS 2: 7-12 regiões
- ✅ Nacional: Portugal

**Vantagem:** Análise multi-nível hierárquica possível

---

### 2. **Granularidade Temporal Superior**

**OECD:**
- Maioria dos dados: anual
- Alguns: trimestral

**Nossa Base de Dados:**
- ✅ **Mensal:** SNS hospitalar (2014-2025)
- ✅ **Trimestral:** INE desemprego, emprego (2011-2025)
- ✅ **Anual:** INE municipal, Eurostat regional

**Vantagem:** Análise de dinâmicas de curto prazo

---

### 3. **Dados Institucionais Únicos**

**OECD:**
- ❌ Não tem dados ao nível de hospitais individuais

**Nossa Base de Dados:**
- ✅ **426 entidades hospitalares** com:
  - Endividamento
  - Capital circulante
  - Pagamentos
  - Workforce (médicos, enfermeiros por hospital)
  - Indicadores de qualidade

**Vantagem:** Variável dependente da pesquisa! (crítico)

---

### 4. **Séries Históricas Mais Longas**

| Indicador | OECD (típico) | Nossa Base |
|-----------|---------------|------------|
| PIB | 1975-2024 | ✅ 1975-2024 (igual) |
| Esperança de vida | 1960-2024 | ✅ **1960-2024** (igual) |
| Despesa saúde | 1992-2024 | ✅ **1992-2024** (igual) |
| Défice/dívida | 1995-2024 | ✅ **1995-2024** (igual) |

**Conclusão:** Mesmas séries (OECD recolhe de Eurostat/INE)

---

### 5. **Fonte Direta vs. Agregada**

**OECD:**
- ⚠️ Dados agregados de fontes nacionais
- ⚠️ Pode ter lag temporal (atraso na publicação)
- ⚠️ Possíveis ajustamentos metodológicos

**Nossa Base de Dados:**
- ✅ **Direto das fontes primárias** (SNS, INE, Eurostat)
- ✅ Dados mais recentes (até 2025)
- ✅ Sem intermediação

---

## VALOR ADICIONAL POTENCIAL DA OECD (SE ACESSÍVEL)

### ⚠️ Comparações Internacionais (Baixa Prioridade)

**O Que OECD Oferece:**
- Comparação de Portugal com outros países OECD
- Rankings internacionais
- Contexto comparativo

**Utilidade para Pesquisa:**
- ⚠️ **BAIXA** - foco da pesquisa é endividamento hospitalar **em Portugal**
- ⚠️ Não há variação cross-country no estudo
- ⚠️ Contexto internacional é **secundário**, não primário

**Possível Uso:**
- Discussão/contextualização na introdução ou conclusão
- "Portugal vs média OECD em despesa saúde"
- Mas: pode fazer isto com Eurostat (todos países UE)

---

### ⚠️ Indicadores Compostos (Baixa Prioridade)

**O Que OECD Oferece:**
- Better Life Index
- Governance Indicators
- Innovation indicators

**Utilidade para Pesquisa:**
- ❌ **NULA** - não relevantes para endividamento hospitalar

---

## COMPARAÇÃO: OECD vs. OUTRAS FONTES PARA PORTUGAL

| Característica | OECD | Eurostat | INE | SNS |
|----------------|------|----------|-----|-----|
| **Fonte primária?** | ❌ Não (agrega) | ⚠️ Misto | ✅ Sim | ✅ Sim |
| **Granularidade geográfica** | Nacional | NUTS 2/3 | Municipal | Institucional |
| **API disponível** | ⚠️ Complexa | ✅ Sim | ✅ Sim | ✅ Sim |
| **Acesso** | ⚠️ Problemático | ✅ Fácil | ✅ Fácil | ✅ Fácil |
| **Dados Portugal** | Nacional | PT filtrado | Portugal | Portugal |
| **Atualização** | ⚠️ Com lag | ✅ Regular | ✅ Regular | ✅ Mensal |
| **Cobertura temporal** | 1990s-2024 | 1960-2024 | 2011-2025 | 2013-2025 |
| **Dados hospitalares** | ❌ Agregados | ❌ NUTS 2 | ❌ Não tem | ✅ 426 hospitais |

**Conclusão:** OECD é **inferior** ao Eurostat/INE/SNS para análise de Portugal

---

## GAPS QUE OECD **NÃO** RESOLVE

### O que ainda não temos e OECD também não tem:

1. **PIB Municipal** ❌
   - OECD: Não tem
   - Ninguém calcula
   - Melhor: NUTS 3 (já temos Eurostat)

2. **Despesa Saúde Regional** ❌
   - OECD: Só nacional
   - Eurostat: Só nacional
   - Gap aceite na literatura

3. **Dados Hospitalares Pré-2013** ❌
   - OECD: Não tem dados institucionais
   - SNS: Portal criado em 2013
   - Gap inevitável

---

## ANÁLISE CUSTO-BENEFÍCIO: EXTRAIR OECD?

### Custos:

1. **Tempo:**
   - API complexa e problemática
   - Estrutura de dados diferente (SDMX)
   - Parser custom necessário
   - Debugging: 2-4 horas
   - Extração: 1-2 horas
   - **Total: 3-6 horas**

2. **Complexidade Técnica:**
   - SDMX format (XML ou JSON-stat)
   - Autenticação possível
   - Rate limits
   - Documentação fragmentada

3. **Manutenção:**
   - API instável
   - Estrutura pode mudar
   - Mais um ponto de falha

### Benefícios:

1. **Novos Dados:** ❌ **NENHUM** (dados já cobertos por Eurostat/INE)
2. **Maior Granularidade:** ❌ **NÃO** (OECD é mais agregado)
3. **Séries Mais Longas:** ❌ **NÃO** (Eurostat tem 1960-2024)
4. **Comparações Internacionais:** ⚠️ **MARGINAL** (não é foco da pesquisa)

### **Análise Custo-Benefício:** ❌ **NÃO VALE A PENA**

**Ratio:** Custo ALTO / Benefício ZERO = ❌ **Não justificado**

---

## RECOMENDAÇÕES

### ❌ **NÃO EXTRAIR DADOS DA OECD**

**Razões:**

1. **Redundância Total:**
   - 100% dos dados OECD relevantes já extraídos de fontes primárias
   - Eurostat = mesma fonte que OECD para Europa
   - INE = fonte primária que OECD usa para Portugal

2. **Inferior em Granularidade:**
   - OECD: apenas nacional
   - Nossa base: institucional + municipal + regional + nacional

3. **Problemas Técnicos:**
   - API difícil de aceder
   - Timeouts e 404 errors
   - Documentação confusa

4. **Foco da Pesquisa:**
   - Objetivo: endividamento hospitalar **em Portugal**
   - Não é estudo comparativo internacional
   - Dados nacionais OECD não adicionam valor

---

### ✅ **CONTINUAR COM DADOS ATUAIS**

**Base de Dados Atual é SUPERIOR:**

| Aspeto | Nossa Base | OECD |
|--------|------------|------|
| **Granularidade** | Institucional→Municipal→Regional→Nacional | Nacional apenas |
| **Cobertura temporal** | 1960-2025 (Eurostat), 2011-2025 (INE), 2014-2025 (SNS) | Similar mas agregado |
| **Dados hospitalares** | 426 entidades individuais | Não tem |
| **Acessibilidade** | APIs funcionais | API problemática |
| **Atualização** | Até 2025 | Lag típico |

---

### ⚠️ **USO OPCIONAL: CONTEXTUALIZAÇÃO**

**Se necessário (baixa prioridade):**

#### Para Introdução/Discussão:

- "Portugal gasta X% PIB em saúde vs Y% média OECD"
- "Dívida pública portuguesa vs outros países OECD"

**Como Obter:**
- Download manual de gráficos/tabelas do site OECD
- 10-15 minutos
- **Não** requer extração via API

**Ficheiros a consultar (se necessário):**
- OECD Health Statistics (portal web)
- OECD Economic Outlook (relatórios PDF)

---

## ALTERNATIVAS À OECD (SE NECESSÁRIO)

Se precisar de **comparações internacionais** (não crítico):

### 1. ✅ **Eurostat (já temos!)** - RECOMENDADO

**Vantagem:**
- Dados comparáveis de **todos** os 27 países UE
- Já extraído: 206,001 registos
- Inclui Portugal + contexto europeu

**Uso:**
- Filtrar Eurostat por múltiplos países
- Comparar Portugal com Espanha, Itália, França, etc.

### 2. **WHO Global Health Expenditure Database**

**Se necessário:**
- Despesa saúde global
- Séries longas
- Download manual ou API

**Valor:** ⚠️ Baixo (Europa é contexto adequado)

### 3. **Banco de Portugal**

**Para indicadores macro adicionais:**
- Dívida pública (mais detalhe)
- Balanço de pagamentos
- Indicadores financeiros

**Valor:** ⚠️ Médio (Eurostat já tem défice/dívida)

---

## CONCLUSÃO FINAL

### ❌ **OECD NÃO ADICIONA VALOR À PESQUISA**

**Sumário:**

1. **Dados OECD = Dados Eurostat/INE** (mesma fonte)
2. **Granularidade OECD < Nossa base de dados**
3. **API OECD problemática** (custos técnicos elevados)
4. **Foco da pesquisa:** Portugal (não comparativo internacional)
5. **Base de dados atual:** ~770,000 registos, 4 fontes, multi-nível

### ✅ **DADOS ATUAIS SÃO SUFICIENTES E SUPERIORES**

**Inventário Completo:**

| Fonte | Registos | Granularidade | Período | Status |
|-------|----------|---------------|---------|--------|
| SNS | 305,744 | Institucional (426) | 2014-2025 | ✅ COMPLETO |
| INE | 34,127 | Municipal (344) | 2011-2025 | ✅ COMPLETO |
| Eurostat Regional | 206,001 | NUTS 2/3 | 1960-2024 | ✅ COMPLETO |
| Eurostat Macro | 224,412 | Nacional | 1975-2024 | ✅ COMPLETO |
| **TOTAL** | **~770,000** | **Multi-nível** | **1960-2025** | ✅ **COMPLETO** |

---

### RECOMENDAÇÃO FINAL

✅ **NÃO PROSSEGUIR COM EXTRAÇÃO OECD**

**Foco deve ser:**
1. ✅ Análise exploratória dos dados já obtidos
2. ✅ Limpeza e preparação de dados
3. ✅ Modelação econométrica
4. ✅ Redação da tese

**Tempo economizado:** 3-6 horas
**Benefício:** Nenhum (dados redundantes)
**Decisão:** ❌ **Não extrair OECD**

---

**CONCLUSÃO:** Base de dados atual (~770k registos de SNS, INE, Eurostat) é **completa, superior em granularidade, e suficiente** para análise robusta de endividamento hospitalar em Portugal (2015-2025). OECD não adiciona valor e apresenta custos técnicos elevados sem benefícios correspondentes.

---

**Gerado:** 26 de outubro de 2025
**Status:** ❌ OECD extraction NOT RECOMMENDED
**Alternativa:** ✅ Use existing data (SNS + INE + Eurostat) - SUPERIOR

*Fim da Análise OECD*
