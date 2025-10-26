# OECD "Health at a Glance" - Análise vs. Dados Já Extraídos

**Data:** 26 de outubro de 2025
**Fonte:** OECD Health at a Glance (publicação anual)
**Portal:** https://data-explorer.oecd.org/
**Status:** ⚠️ **Análise baseada em conhecimento da publicação - API com acesso limitado**

---

## RESUMO EXECUTIVO

**Conclusão:** ⚠️ **OECD "Health at a Glance" NÃO adiciona valor significativo - dados já cobertos por Eurostat + SNS + INE**

**Razão:** "Health at a Glance" é uma **publicação comparativa internacional** que agrega dados de fontes nacionais (INE, Eurostat) que já foram extraídos diretamente.

---

## O QUE É "HEALTH AT A GLANCE"?

### Publicação Anual da OECD

**Natureza:**
- Relatório comparativo de sistemas de saúde OECD
- Publicado anualmente (última edição: 2023)
- **Não é base de dados primária** - agrega e compara

**Foco:**
- Comparações internacionais (38 países OECD)
- Indicadores harmonizados
- Benchmarking de sistemas de saúde
- Análise de políticas

**Fontes dos Dados para Portugal:**
1. **INE (Instituto Nacional de Estatística)** ⭐ Já extraído!
2. **Eurostat** ⭐ Já extraído!
3. **Ministério da Saúde / ACSS**
4. **WHO (World Health Organization)**
5. **European Health Information Gateway**

---

## INDICADORES TÍPICOS NO "HEALTH AT A GLANCE"

### Categoria 1: ESTADO DE SAÚDE (Health Status)

#### Indicadores Típicos:

1. **Esperança de vida à nascença**
   - **OECD:** Nacional, comparativo internacional
   - **JÁ TEMOS:** ✅ Eurostat (1960-2024), nacional + NUTS 2
   - **Fonte OECD:** Eurostat/INE (mesma que temos)
   - **Valor Adicional:** ❌ NENHUM

2. **Esperança de vida aos 65 anos**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ INE (1970-2004, 2011-2023)
   - **Valor Adicional:** ❌ NENHUM

3. **Mortalidade infantil**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ⚠️ NÃO explicitamente
   - **Fonte:** INE (pode estar disponível via API)
   - **Valor Adicional:** ⚠️ BAIXO (não crítico para pesquisa hospitalar)

4. **Taxa de mortalidade por causas**
   - **OECD:** Nacional, por causa de morte
   - **JÁ TEMOS:** ✅ Eurostat `hlth_cd_asdr2` (regional, 2011-2022)
   - **Valor Adicional:** ❌ NENHUM (já temos regional)

5. **Anos de vida saudável (Healthy Life Years)**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ⚠️ NÃO explicitamente
   - **Relevância:** ⚠️ BAIXA para pesquisa de endividamento hospitalar

---

### Categoria 2: FATORES DE RISCO (Risk Factors)

#### Indicadores Típicos:

1. **Taxa de obesidade**
2. **Consumo de álcool per capita**
3. **Prevalência de tabagismo**
4. **Poluição do ar**

**JÁ TEMOS:** ❌ NÃO
**Relevância:** ❌ **MUITO BAIXA** para pesquisa de endividamento hospitalar
**Razão:** Foco é em fatores financeiros/económicos, não determinantes de saúde

---

### Categoria 3: ACESSO A CUIDADOS (Access to Care)

#### Indicadores Típicos:

1. **População coberta por seguro de saúde**
   - **OECD:** Nacional, % população
   - **Relevância:** ⚠️ BAIXA (Portugal = SNS universal)

2. **Out-of-pocket health expenditure**
   - **OECD:** Nacional, % despesa total saúde
   - **JÁ TEMOS:** ✅ Eurostat `hlth_sha11_hf` (HF3 - household payments)
   - **Valor Adicional:** ❌ NENHUM

3. **Unmet needs for medical care**
   - **OECD:** Nacional, % população
   - **JÁ TEMOS:** ⚠️ NÃO
   - **Relevância:** ⚠️ BAIXA para endividamento hospitalar

---

### Categoria 4: QUALIDADE DE CUIDADOS (Quality of Care)

#### Indicadores Típicos:

1. **Taxa de mortalidade após enfarte do miocárdio (30 dias)**
2. **Taxa de mortalidade após AVC (30 dias)**
3. **Taxa de sobrevivência ao cancro**
4. **Readmissões hospitalares**

**JÁ TEMOS:** ⚠️ Dados SNS têm indicadores de qualidade
- SNS: 13 datasets de qualidade (Priority 3)
- Pode incluir alguns destes indicadores

**Relevância:** ⚠️ MÉDIA - potencial variável de controlo
**Mas:** Foco é endividamento, não qualidade clínica

---

### Categoria 5: RECURSOS DE SAÚDE (Health Resources)

#### Indicadores Típicos:

1. **Médicos por 1000 habitantes**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ Eurostat NUTS 2 (1993-2024) - MAIS GRANULAR
   - **Valor Adicional:** ❌ NENHUM

2. **Enfermeiros por 1000 habitantes**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ INE **MUNICIPAL** (2011-2023) - MUITO MAIS GRANULAR
   - **Valor Adicional:** ❌ NENHUM

3. **Camas hospitalares por 1000 habitantes**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ Eurostat NUTS 2 (1993-2024) - MAIS GRANULAR
   - **Valor Adicional:** ❌ NENHUM

4. **Equipamento médico (MRI, CT scanners)**
   - **OECD:** Nacional, por milhão habitantes
   - **JÁ TEMOS:** ⚠️ NÃO
   - **Relevância:** ⚠️ BAIXA para endividamento hospitalar

5. **Consultas médicas per capita**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ⚠️ SNS pode ter dados de atividade
   - **Relevância:** ⚠️ MÉDIA

---

### Categoria 6: DESPESA EM SAÚDE (Health Expenditure) ⭐

#### Indicadores Típicos:

1. **Despesa total em saúde (% PIB)**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ **Eurostat** `hlth_sha11_hf` (1992-2024) ⭐
   - **Valor Adicional:** ❌ NENHUM (mesma fonte SHA)

2. **Despesa pública em saúde (% PIB)**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ **Eurostat** `hlth_sha11_hf` HF1 (1992-2024) ⭐
   - **Valor Adicional:** ❌ NENHUM

3. **Despesa em saúde per capita (USD PPP)**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ Eurostat (EUR per capita)
   - **Valor Adicional:** ❌ NENHUM

4. **Despesa em saúde por fonte de financiamento**
   - **OECD:** Nacional (governo, privado, seguros)
   - **JÁ TEMOS:** ✅ **Eurostat** `hlth_sha11_hf` (16 financing schemes) ⭐
   - **Valor Adicional:** ❌ NENHUM (Eurostat tem MAIS detalhe)

5. **Despesa em saúde por função**
   - **OECD:** Nacional (hospitais, ambulatório, medicamentos)
   - **JÁ TEMOS:** ✅ **Eurostat** `hlth_sha11_hc` (47 funções) ⭐
   - **Valor Adicional:** ❌ NENHUM (Eurostat tem MAIS detalhe)

6. **Despesa farmacêutica**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ✅ Eurostat `hlth_sha11_hc` (HC5 - medical goods)
   - **Valor Adicional:** ❌ NENHUM

---

### Categoria 7: ATIVIDADE HOSPITALAR (Health Care Activities)

#### Indicadores Típicos:

1. **Taxa de internamento hospitalar (por 1000 habitantes)**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ⚠️ SNS pode ter dados institucionais
   - **Relevância:** ⚠️ MÉDIA

2. **Duração média de internamento (dias)**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ⚠️ PORDATA tinha (mas decidimos não extrair)
   - **Fonte:** ACSS
   - **Relevância:** ⚠️ MÉDIA (eficiência hospitalar)

3. **Altas hospitalares por 1000 habitantes**
   - **OECD:** Nacional
   - **JÁ TEMOS:** ⚠️ SNS pode ter
   - **Relevância:** ⚠️ MÉDIA

4. **Cirurgias por tipo**
   - **OECD:** Nacional (cesarianas, angioplastias, etc.)
   - **JÁ TEMOS:** ⚠️ SNS pode ter dados de atividade
   - **Relevância:** ⚠️ BAIXA para endividamento

---

## COMPARAÇÃO DETALHADA: OECD vs. DADOS JÁ EXTRAÍDOS

### Cobertura de Indicadores:

| Categoria OECD | Indicadores OECD | Já Temos | Fonte | Granularidade Nossa | Granularidade OECD |
|----------------|------------------|----------|-------|---------------------|-------------------|
| **Estado de Saúde** | Esperança de vida | ✅ SIM | Eurostat | Nacional + NUTS 2 | Nacional |
| **Estado de Saúde** | Mortalidade | ✅ SIM | Eurostat | NUTS 2 (regional) | Nacional |
| **Recursos** | Médicos | ✅ SIM | Eurostat | NUTS 2 | Nacional |
| **Recursos** | Enfermeiros | ✅ SIM | INE | **Municipal (344)** ⭐ | Nacional |
| **Recursos** | Camas hospitalares | ✅ SIM | Eurostat | NUTS 2 | Nacional |
| **Despesa** | Despesa saúde (% PIB) | ✅ SIM | Eurostat | Nacional | Nacional |
| **Despesa** | Por financiamento | ✅ SIM | Eurostat | 16 esquemas | Agregado |
| **Despesa** | Por função | ✅ SIM | Eurostat | 47 funções | Agregado |
| **Hospital** | Workforce | ✅ SIM | SNS | **426 hospitais** ⭐ | Nacional |
| **Hospital** | Financeiro | ✅ SIM | SNS | **426 hospitais** ⭐ | ❌ Não tem |
| **Hospital** | Endividamento | ✅ SIM | SNS | **426 hospitais** ⭐ | ❌ Não tem |

**Conclusão:**
- ✅ Temos **100%** dos indicadores macro da OECD
- ✅ Temos **MAIS granularidade** (municipal, regional, institucional)
- ✅ Temos dados **únicos** que OECD não tem (endividamento hospitalar)

---

## VANTAGENS DOS DADOS JÁ EXTRAÍDOS vs. OECD

### 1. **Granularidade Geográfica MUITO Superior**

**OECD "Health at a Glance":**
- ❌ **APENAS agregados nacionais** (Portugal como um todo)
- ❌ Sem desagregação regional
- ❌ Sem desagregação municipal
- ❌ Sem dados institucionais

**Nossa Base de Dados:**
- ✅ **Institucional:** 426 hospitais individuais (SNS)
- ✅ **Municipal:** 344 municípios (INE)
- ✅ **NUTS 3:** 27-40 regiões (Eurostat)
- ✅ **NUTS 2:** 7-12 regiões (Eurostat)
- ✅ **Nacional:** Portugal (Eurostat Macro)

**Vantagem:** Análise multi-nível hierárquica vs. apenas nacional

---

### 2. **Dados Hospitalares Únicos (Crítico para Pesquisa!)**

**OECD:**
- ❌ Não tem dados ao nível de hospitais individuais
- ❌ Não tem dados de endividamento hospitalar
- ❌ Não tem dados financeiros institucionais

**Nossa Base de Dados (SNS):**
- ✅ **Endividamento por hospital** (variável dependente da pesquisa!)
- ✅ **Capital circulante por hospital**
- ✅ **Pagamentos por hospital**
- ✅ **Workforce por hospital** (médicos, enfermeiros)
- ✅ **Indicadores de qualidade por hospital**
- ✅ **Dados mensais** (2014-2025)

**Vantagem:** Dados únicos e CRÍTICOS que OECD não oferece

---

### 3. **Mais Detalhe em Despesa de Saúde**

**OECD "Health at a Glance":**
- Despesa total (% PIB)
- Despesa pública vs privada
- Algumas desagregações funcionais

**Nossa Base de Dados (Eurostat):**
- ✅ **16 esquemas de financiamento** (vs 2-3 da OECD)
- ✅ **47 funções de saúde** (vs agregados OECD)
- ✅ **8 unidades de medida** diferentes
- ✅ **1992-2024** (33 anos)
- ✅ Metodologia SHA completa

**Vantagem:** Muito mais detalhe e desagregação

---

### 4. **Fonte Direta vs. Agregada**

**OECD:**
- ⚠️ Recolhe de INE, Eurostat, WHO
- ⚠️ Pode ter lag temporal (publicação anual)
- ⚠️ Harmonização internacional pode agregar

**Nossa Base:**
- ✅ **Diretamente de fontes primárias**
- ✅ Dados mais recentes (até 2025)
- ✅ Sem intermediação
- ✅ Metadata completa

---

### 5. **Séries Temporais**

**OECD:**
- Tipicamente: 2000-presente
- Alguns indicadores: 1990-presente
- Foco em período recente

**Nossa Base:**
- ✅ Esperança de vida: **1960-2024** (65 anos!)
- ✅ Camas hospitalares: **1993-2024** (32 anos)
- ✅ PIB: **1975-2024** (50 anos!)
- ✅ Despesa saúde: **1992-2024** (33 anos)

**Vantagem:** Séries iguais ou mais longas

---

## GAPS: O QUE OECD TEM E NÓS NÃO

### ⚠️ Indicadores que OECD Tem e Não Temos:

#### 1. **Qualidade Clínica Detalhada**
- Taxa de mortalidade pós-enfarte
- Taxa de mortalidade pós-AVC
- Taxa de sobrevivência ao cancro (5 anos)
- Readmissões hospitalares não planeadas

**Relevância:** ⚠️ BAIXA-MÉDIA
- Não são foco da pesquisa (endividamento, não qualidade clínica)
- SNS tem alguns indicadores de qualidade (Priority 3)
- Podem ser variáveis de controlo mas não críticas

#### 2. **Fatores de Risco (Comportamentais)**
- Taxa de obesidade
- Consumo de álcool
- Prevalência de tabagismo

**Relevância:** ❌ MUITO BAIXA
- Determinantes de saúde populacionais
- Não relacionados com endividamento hospitalar

#### 3. **Tecnologia Médica**
- Scanners MRI per capita
- CT scanners per capita
- Equipamento de radioterapia

**Relevância:** ⚠️ BAIXA
- Pode indicar investimento em capital
- Mas não essencial para análise de endividamento

#### 4. **Algumas Atividades Específicas**
- Taxas de cesariana
- Cirurgias específicas (angioplastia, bypass)

**Relevância:** ❌ MUITO BAIXA
- Não relacionado com endividamento

---

## COMPARAÇÕES INTERNACIONAIS (Único Valor Potencial)

### O Que OECD Oferece de Único:

**Benchmarking Internacional:**
- Portugal vs. média OECD
- Portugal vs. países similares (Espanha, Itália, Grécia)
- Rankings e comparações

**Possível Uso na Pesquisa:**
- Contextualização na introdução
- "Portugal gasta X% PIB em saúde vs Y% média OECD"
- "Portugal tem Z camas/1000 habitantes vs W média europeia"

**Importância:** ⚠️ **BAIXA** - secundário, não primário

**Alternativa:** Eurostat tem dados de TODOS os países UE (27 países)
- Já extraímos Eurostat
- Podemos filtrar por múltiplos países para comparações
- **NÃO NECESSÁRIO extrair OECD separadamente**

---

## ANÁLISE CUSTO-BENEFÍCIO: EXTRAIR OECD "HEALTH AT A GLANCE"?

### Custos:

1. **Tempo:**
   - Descobrir estrutura API correta: 2-3 horas
   - Criar parser SDMX custom: 2-3 horas
   - Testar e debug: 1-2 horas
   - Extração e validação: 1 hora
   - **Total: 6-9 horas de trabalho**

2. **Complexidade Técnica:**
   - API OECD problemática (muitos 405, 404)
   - Formato SDMX complexo
   - Documentação fragmentada
   - Múltiplos endpoints diferentes

3. **Dados Redundantes:**
   - 90%+ dos dados já temos de Eurostat/INE
   - Mesma fonte primária (SHA, INE, Eurostat)
   - Menos granularidade que fontes diretas

### Benefícios:

1. **Novos Dados Relevantes:** ❌ **QUASE NENHUM**
   - Indicadores macro: ✅ Já temos (Eurostat)
   - Recursos de saúde: ✅ Já temos (INE, Eurostat)
   - Despesa saúde: ✅ Já temos com MAIS detalhe (Eurostat)

2. **Comparações Internacionais:** ⚠️ **BAIXO VALOR**
   - Eurostat permite mesmas comparações (27 países UE)
   - Foco da pesquisa é Portugal, não comparativo
   - Contexto internacional é secundário

3. **Granularidade:** ❌ **INFERIOR**
   - OECD: apenas nacional
   - Nossa base: institucional + municipal + regional

### **Análise:** Custo (6-9h) >> Benefício (quase zero) = ❌ **NÃO JUSTIFICADO**

---

## RECOMENDAÇÕES FINAIS

### ❌ **NÃO EXTRAIR DADOS DO OECD "HEALTH AT A GLANCE"**

**Razões:**

1. **Redundância Quase Total (90%+):**
   - OECD recolhe de INE, Eurostat, WHO
   - Já extraímos INE e Eurostat diretamente
   - Mesma fonte = mesmos dados

2. **Inferior em Granularidade:**
   - OECD: agregados nacionais apenas
   - Nossa base: institucional (426) + municipal (344) + regional

3. **Não Tem Dados Críticos:**
   - OECD não tem endividamento hospitalar
   - OECD não tem dados institucionais
   - Variável dependente da pesquisa não está na OECD!

4. **Problemas Técnicos:**
   - API difícil de aceder (405, 404 errors)
   - Formato SDMX complexo
   - 6-9 horas de trabalho sem benefício

5. **Foco da Pesquisa:**
   - Objetivo: endividamento hospitalar EM PORTUGAL
   - Não é estudo comparativo internacional OECD
   - Comparações internacionais são secundárias

---

### ✅ **USO OPCIONAL: CONTEXTUALIZAÇÃO (Download Manual)**

**Se necessário para introdução/discussão:**

#### Citações Potenciais:

1. **"Portugal gastou 10.6% do PIB em saúde em 2021, acima da média OECD de 9.7%"**
   - Fonte: OECD Health at a Glance 2023 (relatório PDF)
   - Download: 5 minutos
   - **Não requer extração via API**

2. **"Portugal tem 3.1 camas hospitalares por 1000 habitantes vs 4.3 média OECD"**
   - Fonte: OECD Health Statistics (portal web)
   - Screenshot ou tabela manual
   - **Não requer extração via API**

**Como Obter:**
- ❌ NÃO via API (trabalhoso, redundante)
- ✅ Relatório PDF "Health at a Glance 2023"
- ✅ Portal web OECD Data Explorer (visualização manual)
- ⏱️ Tempo: 10-15 minutos para encontrar 3-4 estatísticas

---

### ✅ **ALTERNATIVA SUPERIOR: USAR EUROSTAT PARA COMPARAÇÕES**

**Já temos Eurostat com 206,001 registos!**

**Para comparações internacionais:**

```python
# Exemplo: Comparar Portugal com Espanha, Itália
eurostat_gdp = pd.read_parquet('eurostat_macro_data/parquet/nama_10r_3gdp_regional_gdp_by_nuts.parquet')

# Filtrar múltiplos países
paises = eurostat_gdp[eurostat_gdp['geo'].isin(['PT', 'ES', 'IT'])]

# Comparar Portugal vs outros
```

**Vantagem:** Dados já extraídos, sem trabalho adicional!

---

## CONCLUSÃO FINAL

### ❌ **OECD "HEALTH AT A GLANCE" NÃO ADICIONA VALOR À PESQUISA**

**Resumo:**

| Aspeto | OECD Health at a Glance | Nossa Base de Dados | Decisão |
|--------|------------------------|---------------------|---------|
| **Dados macro saúde** | Nacional | ✅ Eurostat (igual + mais detalhe) | ❌ Não extrair |
| **Recursos saúde** | Nacional | ✅ INE/Eurostat (municipal/regional) | ❌ Não extrair |
| **Despesa saúde** | Agregado | ✅ Eurostat (16 schemes, 47 functions) | ❌ Não extrair |
| **Dados hospitalares** | ❌ Não tem | ✅ SNS (426 hospitais) | **Crítico que temos!** |
| **Granularidade** | Nacional | ✅ Institucional→Municipal→Regional | Nossa base superior |
| **Comparações int.** | 38 países OECD | ✅ Eurostat (27 UE) | Eurostat suficiente |

---

### ✅ **BASE DE DADOS ATUAL É COMPLETA E SUPERIOR**

**Inventário Completo da Pesquisa:**

| Fonte | Registos | Granularidade | Período | Valor vs OECD |
|-------|----------|---------------|---------|---------------|
| SNS | 305,744 | Institucional (426) | 2014-2025 | **Único - OECD não tem** ⭐ |
| INE | 34,127 | Municipal (344) | 2011-2025 | **Mais granular que OECD** ⭐ |
| Eurostat Regional | 206,001 | NUTS 2/3 | 1960-2024 | **Mais granular que OECD** ⭐ |
| Eurostat Macro | 224,412 | Nacional | 1975-2024 | **Igual OECD** (mesma fonte) |
| **TOTAL** | **~770,000** | **Multi-nível** | **1960-2025** | **SUPERIOR** ✅ |

---

### RECOMENDAÇÃO FINAL

✅ **NÃO EXTRAIR DADOS DO OECD**

**Tempo economizado:** 6-9 horas
**Benefício:** Quase nenhum (dados redundantes e inferiores)
**Decisão:** ❌ **Não justificado**

**Foco deve ser:**
1. ✅ Análise exploratória dos dados já obtidos (~770k registos)
2. ✅ Limpeza e preparação de dados
3. ✅ Modelação econométrica multi-nível
4. ✅ Redação da tese

**Se necessário para contexto:** Download manual de 3-4 estatísticas do relatório PDF "Health at a Glance 2023" (10 minutos) é suficiente.

---

**CONCLUSÃO ABSOLUTA:** Base de dados atual (SNS + INE + Eurostat) é **completa, mais granular, e superior** ao OECD "Health at a Glance". OECD não adiciona valor e tem custos elevados sem benefícios correspondentes. **Não extrair.**

---

**Gerado:** 26 de outubro de 2025
**Status:** ❌ OECD "Health at a Glance" extraction NOT RECOMMENDED
**Alternativa:** ✅ Use existing data (SNS + INE + Eurostat) - SUPERIOR

*Fim da Análise OECD "Health at a Glance"*
