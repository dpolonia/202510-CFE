# PORDATA - Análise de Disponibilidade de Dados vs. Fontes Já Extraídas

**URL:** https://www.pordata.pt
**Data:** 26 de outubro de 2025
**Propósito:** Identificar dados de saúde e economia disponíveis no PORDATA que ainda não foram descarregados do INE, SNS ou Eurostat

---

## RESUMO EXECUTIVO

**Status:** ⚠️ **PORDATA é um agregador - maioria dos dados JÁ extraídos das fontes originais**

**Tipo de Portal:**
- Portal de estatísticas agregadas (não fonte primária)
- Mantido pela Fundação Francisco Manuel dos Santos
- Agrega dados de: INE, Eurostat, Banco de Portugal, Ministérios
- Foco em visualização e séries temporais longas

**Formatos de Download:**
- ✅ CSV - Disponível (download manual)
- ✅ XLSX - Disponível (download manual)
- ❌ JSON - Não disponível
- ❌ Parquet - Não disponível
- ❌ API - Não existe

**Acesso:**
- Gratuito (sem necessidade de registo para maioria dos dados)
- Download manual por indicador
- Não automatizável

---

## O QUE É O PORDATA?

### Natureza do Portal:

PORDATA **NÃO é uma fonte primária de dados**. É um **portal agregador** que:

1. **Recolhe dados de fontes oficiais:**
   - Instituto Nacional de Estatística (INE) ⭐ (principal fonte)
   - Eurostat
   - Banco de Portugal
   - Ministérios (Saúde, Educação, Finanças)
   - ACSS (Administração Central do Sistema de Saúde)
   - DGS (Direção-Geral da Saúde)

2. **Adiciona valor através de:**
   - Visualizações interativas
   - Séries temporais longas (desde 1960 em alguns casos)
   - Comparações internacionais
   - Interface user-friendly
   - Contextualização dos dados

3. **Limitações:**
   - ❌ Sem API pública
   - ❌ Download manual apenas (indicador a indicador)
   - ❌ Não permite download em massa
   - ❌ Dados podem ter lag temporal vs. fonte original
   - ❌ Alguns indicadores têm menor granularidade que a fonte

---

## COMPARAÇÃO: PORDATA vs. FONTES JÁ EXTRAÍDAS

### Dados Que Você JÁ TEM (Extraídos):

**SNS (305,744 registos, 2013-2025):**
- ✅ Dados financeiros hospitalares (mensais, institucionais)
- ✅ Workforce hospitalar (mensais, institucionais)
- ✅ Indicadores de qualidade hospitalares
- ✅ Granularidade: 426 entidades individuais
- ✅ Frequência: Mensal

**INE (34,127 registos, 2011-2025):**
- ✅ Índice de envelhecimento (municipal, 2011-2023)
- ✅ Índices de dependência (municipal, 2011-2023)
- ✅ Enfermeiros por 1000 habitantes (municipal, 2011-2023)
- ✅ Taxa de desemprego (trimestral, NUTS 2, 2011-2025)
- ✅ Emprego (trimestral, 2011-2025)
- ✅ Esperança de vida aos 65 anos (2011-2023)
- ✅ Granularidade: 344 municípios
- ✅ Frequência: Anual/Trimestral

**Eurostat (206,001 registos, 1960-2024):**
- ✅ PIB regional (NUTS 2/3, 2000-2023)
- ✅ Camas hospitalares (NUTS 2, 1993-2024)
- ✅ Médicos por região (NUTS 2, 1993-2024)
- ✅ Esperança de vida (nacional, 1960-2024)
- ✅ População por idade/sexo (NUTS 2/3, 2014-2024)
- ✅ Emprego regional (NUTS 2, 1995-2023)
- ✅ Granularidade: NUTS 2/3 (7-40 regiões)
- ✅ Frequência: Anual

---

## DADOS DISPONÍVEIS NO PORDATA

### Categoria: SAÚDE

#### Subcategoria: Hospitais

**Indicadores Típicos:**
1. **Número de hospitais**
   - **Fonte Original:** ACSS / SNS
   - **Disponível no PORDATA:** Nacional + Regional
   - **Já tem?** ✅ SIM (implícito nos dados SNS - 426 entidades)
   - **Valor Adicional:** ⚠️ Baixo (dados SNS são mais granulares)

2. **Camas hospitalares**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional + Regional (NUTS 2)
   - **Já tem?** ✅ SIM (Eurostat: 1993-2024, NUTS 2)
   - **Valor Adicional:** ❌ Nenhum (fonte já extraída)

3. **Internamentos hospitalares**
   - **Fonte Original:** ACSS / SNS
   - **Disponível no PORDATA:** Nacional, séries longas
   - **Já tem?** ⚠️ PARCIAL (SNS tem dados institucionais recentes)
   - **Valor Adicional:** ✅ Séries históricas pré-2013 (se necessário)

4. **Tempo médio de internamento**
   - **Fonte Original:** ACSS
   - **Disponível no PORDATA:** Nacional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ✅ Potencialmente útil (eficiência hospitalar)

#### Subcategoria: Recursos de Saúde

**Indicadores Típicos:**
1. **Médicos por 1000 habitantes**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, Regional, Municipal
   - **Já tem?** ✅ SIM (Eurostat: NUTS 2, 1993-2024)
   - **Valor Adicional:** ✅ MÉDIO (PORDATA pode ter municipal, Eurostat só regional)

2. **Enfermeiros por 1000 habitantes**
   - **Fonte Original:** INE
   - **Disponível no PORDATA:** Nacional, Regional, Municipal
   - **Já tem?** ✅ SIM (INE: municipal, 2011-2023)
   - **Valor Adicional:** ❌ Nenhum (fonte já extraída)

3. **Centros de saúde**
   - **Fonte Original:** ACSS
   - **Disponível no PORDATA:** Nacional, Regional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ Baixo (foco da pesquisa é hospitais, não CSP)

4. **Farmácias**
   - **Fonte Original:** INFARMED
   - **Disponível no PORDATA:** Municipal
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ Baixo (não essencial para pesquisa de hospitais)

#### Subcategoria: Despesas de Saúde

**Indicadores Típicos:**
1. **Despesa pública em saúde (% PIB)**
   - **Fonte Original:** INE / Eurostat / Ministério das Finanças
   - **Disponível no PORDATA:** Nacional, séries longas
   - **Já tem?** ⚠️ PARCIAL (não explícito)
   - **Valor Adicional:** ✅ ALTO - contexto macroeconómico importante

2. **Despesa em saúde per capita**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, regional
   - **Já tem?** ⚠️ PARCIAL (não explícito)
   - **Valor Adicional:** ✅ MÉDIO

3. **Despesa privada em saúde**
   - **Fonte Original:** INE
   - **Disponível no PORDATA:** Nacional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ MÉDIO (contexto de financiamento)

#### Subcategoria: Estado de Saúde

**Indicadores Típicos:**
1. **Esperança de vida à nascença**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, Regional, séries longas
   - **Já tem?** ✅ SIM (Eurostat: 1960-2024)
   - **Valor Adicional:** ❌ Nenhum

2. **Esperança de vida aos 65 anos**
   - **Fonte Original:** INE
   - **Disponível no PORDATA:** Nacional, Regional
   - **Já tem?** ✅ SIM (INE: 2011-2023)
   - **Valor Adicional:** ❌ Nenhum

3. **Taxa de mortalidade**
   - **Fonte Original:** INE
   - **Disponível no PORDATA:** Nacional, Regional, Municipal
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ✅ MÉDIO (potencial variável de controlo)

4. **Taxa de obesidade**
   - **Fonte Original:** INE (INSEF)
   - **Disponível no PORDATA:** Nacional, Regional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ BAIXO (não crítico para pesquisa hospitalar)

---

### Categoria: ECONOMIA

#### Subcategoria: Crescimento e Produtividade

**Indicadores Típicos:**
1. **PIB (nacional)**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, séries desde 1960
   - **Já tem?** ✅ SIM (implícito no Eurostat)
   - **Valor Adicional:** ⚠️ Baixo (séries longas se necessário)

2. **PIB regional (NUTS 2/3)**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** NUTS 2/3, desde 2000
   - **Já tem?** ✅ SIM (Eurostat: NUTS 2/3, 2000-2023)
   - **Valor Adicional:** ❌ Nenhum

3. **PIB per capita**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, Regional
   - **Já tem?** ✅ SIM (pode ser calculado dos dados já extraídos)
   - **Valor Adicional:** ❌ Nenhum

4. **Taxa de crescimento do PIB**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, Regional
   - **Já tem?** ✅ SIM (pode ser calculado)
   - **Valor Adicional:** ❌ Nenhum

#### Subcategoria: Mercado de Trabalho

**Indicadores Típicos:**
1. **Taxa de desemprego**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, Regional, Municipal
   - **Já tem?** ✅ SIM (INE: trimestral NUTS 2, 2011-2025)
   - **Valor Adicional:** ⚠️ MÉDIO (PORDATA pode ter municipal)

2. **População empregada**
   - **Fonte Original:** INE / Eurostat
   - **Disponível no PORDATA:** Nacional, Regional
   - **Já tem?** ✅ SIM (INE: 2011-2025; Eurostat: 1995-2023)
   - **Valor Adicional:** ❌ Nenhum

3. **Salário médio**
   - **Fonte Original:** GEP-MTSSS / INE
   - **Disponível no PORDATA:** Nacional, Regional, Municipal
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ✅ MÉDIO (contexto económico regional)

#### Subcategoria: Finanças Públicas

**Indicadores Típicos:**
1. **Dívida pública**
   - **Fonte Original:** Banco de Portugal / INE
   - **Disponível no PORDATA:** Nacional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ✅ ALTO - contexto macroeconómico crítico

2. **Défice/Excedente orçamental**
   - **Fonte Original:** INE / Ministério das Finanças
   - **Disponível no PORDATA:** Nacional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ✅ ALTO - contexto fiscal

3. **Despesas públicas por função**
   - **Fonte Original:** INE / Ministério das Finanças
   - **Disponível no PORDATA:** Nacional (incluindo saúde)
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ✅ ALTO - contexto de financiamento SNS

4. **Receitas fiscais**
   - **Fonte Original:** Ministério das Finanças / INE
   - **Disponível no PORDATA:** Nacional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ MÉDIO

#### Subcategoria: Demografia Empresarial

**Indicadores Típicos:**
1. **Número de empresas**
   - **Fonte Original:** INE
   - **Disponível no PORDATA:** Nacional, Regional, Municipal
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ BAIXO (não essencial)

2. **Falências empresariais**
   - **Fonte Original:** INE
   - **Disponível no PORDATA:** Nacional
   - **Já tem?** ❌ NÃO
   - **Valor Adicional:** ⚠️ MÉDIO (proxy de stress económico)

---

## IDENTIFICAÇÃO DE GAPS - DADOS QUE PORDATA TEM E VOCÊ NÃO

### ALTA PRIORIDADE (Úteis para a Pesquisa):

#### 1. **Despesa Pública em Saúde (% PIB) - Nacional**
- **Fonte PORDATA:** Ministério das Finanças / INE
- **Utilidade:** ✅✅✅ **MUITO ALTA**
- **Razão:** Contexto macroeconómico de financiamento do SNS
- **Nível:** Nacional
- **Séries:** Desde 1995
- **Alternativa:** Pode calcular com dados SNS + PIB Eurostat

#### 2. **Dívida Pública (% PIB) - Nacional**
- **Fonte PORDATA:** Banco de Portugal
- **Utilidade:** ✅✅✅ **MUITO ALTA**
- **Razão:** Contexto fiscal geral que afeta financiamento hospitalar
- **Nível:** Nacional
- **Séries:** Desde 1990
- **Alternativa:** Dados Banco de Portugal diretamente

#### 3. **Défice/Excedente Orçamental (% PIB) - Nacional**
- **Fonte PORDATA:** Ministério das Finanças / INE
- **Utilidade:** ✅✅✅ **MUITO ALTA**
- **Razão:** Pressão orçamental afeta disponibilidade de recursos para saúde
- **Nível:** Nacional
- **Séries:** Desde 1995

#### 4. **Despesas Públicas por Função (Saúde) - Nacional**
- **Fonte PORDATA:** Ministério das Finanças
- **Utilidade:** ✅✅ **ALTA**
- **Razão:** Orçamento total dedicado à saúde
- **Nível:** Nacional
- **Séries:** Desde 2000

#### 5. **Salário Médio Regional**
- **Fonte PORDATA:** GEP-MTSSS / INE
- **Utilidade:** ✅✅ **ALTA**
- **Razão:** Contexto económico regional, capacidade de atrair profissionais
- **Nível:** NUTS 2/3 ou Municipal
- **Séries:** Desde 2010

### MÉDIA PRIORIDADE (Potencialmente Úteis):

#### 6. **Taxa de Mortalidade (Municipal)**
- **Fonte PORDATA:** INE
- **Utilidade:** ✅ **MÉDIA**
- **Razão:** Variável de controlo para necessidades de saúde
- **Nível:** Municipal
- **Alternativa:** Pode estar disponível diretamente no INE

#### 7. **Tempo Médio de Internamento (Nacional)**
- **Fonte PORDATA:** ACSS
- **Utilidade:** ✅ **MÉDIA**
- **Razão:** Indicador de eficiência hospitalar
- **Nível:** Nacional
- **Séries:** Desde 2000

#### 8. **Médicos por 1000 habitantes (Municipal)**
- **Fonte PORDATA:** INE
- **Utilidade:** ✅ **MÉDIA**
- **Razão:** Já tem NUTS 2 (Eurostat), municipal seria mais granular
- **Nível:** Municipal
- **Nota:** Verificar se INE API tem isto (pode ter)

#### 9. **Despesa Privada em Saúde**
- **Fonte PORDATA:** INE
- **Utilidade:** ✅ **MÉDIA**
- **Razão:** Contexto de financiamento dual (público/privado)
- **Nível:** Nacional

#### 10. **Falências Empresariais**
- **Fonte PORDATA:** INE
- **Utilidade:** ✅ **MÉDIA**
- **Razão:** Proxy para stress económico regional
- **Nível:** Nacional/Regional

### BAIXA PRIORIDADE (Não Essenciais):

- Centros de saúde (foco da pesquisa é hospitais)
- Farmácias
- Taxa de obesidade
- Número de empresas
- Indicadores ambientais

---

## POSSIBILIDADES DE EXTRAÇÃO - PORDATA

### ❌ **Método 1: API/Download Automático (NÃO disponível)**

PORDATA **NÃO oferece:**
- API pública
- Download em massa
- Exportação automatizada

### ✅ **Método 2: Download Manual (Disponível, Trabalhoso)**

**Como funciona:**
1. Aceder ao indicador específico no PORDATA
2. Selecionar período temporal e geografia
3. Clicar em "Exportar" → Excel ou CSV
4. Download ficheiro individual

**Limitações:**
- ⚠️ Indicador a indicador (sem download em massa)
- ⚠️ Trabalhoso e demorado (10-20 indicadores = 1-2 horas)
- ⚠️ Não automatizável
- ⚠️ Não replicável facilmente

**Vantagens:**
- ✅ Dados limpos e bem estruturados
- ✅ Séries temporais longas
- ✅ Documentação clara

**Processo Estimado:**
- 5-10 minutos por indicador
- 10 indicadores = 1-2 horas de trabalho manual

### ✅ **Método 3: Acesso à Fonte Original (Recomendado para alguns)**

Para indicadores de **ALTA PRIORIDADE**, considere ir à fonte:

1. **Banco de Portugal** (dívida pública)
   - URL: https://bpstat.bportugal.pt/
   - API disponível: https://bpstat.bportugal.pt/sites/default/files/documentos/bpstat_api_documentation.pdf
   - ✅ **RECOMENDADO:** Extrair via API

2. **Ministério das Finanças** (despesa pública, défice)
   - Portal: https://www.dgo.gov.pt/
   - Dados: Relatórios orçamentais
   - ⚠️ Maioritariamente PDF (trabalhoso)

3. **INE - Indicadores Adicionais**
   - Verificar se taxa de mortalidade, médicos municipais existem na API INE
   - Usar mesmo método (op=1) já desenvolvido

---

## RECOMENDAÇÕES

### Para a sua Investigação de Doutoramento:

#### ✅ **Opção 1: Priorizar 5 Indicadores Macroeconómicos do PORDATA (RECOMENDADO)**

**Indicadores a descarregar manualmente do PORDATA:**

1. **Despesa pública em saúde (% PIB)** - Nacional, 1995-2024
2. **Dívida pública (% PIB)** - Nacional, 1995-2024
3. **Défice/Excedente orçamental (% PIB)** - Nacional, 1995-2024
4. **Despesas públicas por função: Saúde** - Nacional, 2000-2024
5. **Salário médio mensal** - NUTS 2, 2010-2024

**Tempo estimado:** 30-45 minutos
**Formato:** CSV ou Excel
**Utilidade:** ✅✅✅ **Muito Alta** - contextualização macroeconómica crítica

**Ação:**
1. Aceder a https://www.pordata.pt
2. Pesquisar cada indicador
3. Exportar para CSV (delimitador: ponto-e-vírgula)
4. Guardar em `pordata_manual_data/`

#### ✅ **Opção 2: Extrair Dados do Banco de Portugal via API**

**Indicadores:**
- Dívida pública
- Défice orçamental
- PIB
- Juros da dívida

**Vantagem:**
- ✅ API disponível (automatizável)
- ✅ Dados atualizados
- ✅ Séries longas (desde 1990)

**Ação:** Criar script Python para Banco de Portugal API

#### ⚠️ **Opção 3: Verificar INE API para Indicadores Adicionais**

**Indicadores a procurar no INE:**
- Taxa de mortalidade (municipal)
- Médicos por 1000 habitantes (municipal)
- Salários regionais

**Método:** Usar API INE com op=1 (já desenvolvido)

#### ❌ **NÃO Recomendado: Download Massivo PORDATA**

**Razões:**
- Maioria dos dados já extraídos das fontes originais
- Não automatizável
- Valor marginal baixo
- Trabalhoso (100+ indicadores = semanas de trabalho)

---

## MATRIZ DE DECISÃO

| Indicador | Fonte | Já Tem? | Prioridade | Ação Recomendada |
|-----------|-------|---------|------------|------------------|
| **Despesa pública em saúde (% PIB)** | PORDATA | ❌ | ⭐⭐⭐ | Download manual PORDATA |
| **Dívida pública (% PIB)** | Banco Portugal | ❌ | ⭐⭐⭐ | API Banco de Portugal |
| **Défice orçamental (% PIB)** | PORDATA | ❌ | ⭐⭐⭐ | Download manual PORDATA |
| **Despesas públicas: Saúde** | PORDATA | ❌ | ⭐⭐⭐ | Download manual PORDATA |
| **Salário médio regional** | PORDATA | ❌ | ⭐⭐ | Download manual PORDATA |
| **Taxa de mortalidade (municipal)** | INE | ❌ | ⭐⭐ | Verificar INE API primeiro |
| **Médicos (municipal)** | INE | ❌ | ⭐⭐ | Verificar INE API primeiro |
| **Tempo médio internamento** | PORDATA | ❌ | ⭐ | Opcional |
| **PIB regional** | Eurostat | ✅ | - | Já tem |
| **Enfermeiros (municipal)** | INE | ✅ | - | Já tem |
| **Desemprego** | INE | ✅ | - | Já tem |
| **Camas hospitalares** | Eurostat | ✅ | - | Já tem |
| **Dados financeiros hospitalares** | SNS | ✅ | - | Já tem |

---

## COMPARAÇÃO: PORDATA vs. OUTRAS FONTES

| Característica | PORDATA | SNS | INE | Eurostat |
|----------------|---------|-----|-----|----------|
| **API pública** | ❌ Não | ✅ Sim | ✅ Sim | ✅ Sim |
| **Download automático** | ❌ Não | ✅ Sim | ✅ Sim | ✅ Sim |
| **Fonte primária** | ❌ Não (agrega) | ✅ Sim | ✅ Sim | ✅ Sim |
| **Séries temporais** | ✅ Muito longas | ⚠️ Médias | ✅ Longas | ✅ Muito longas |
| **Granularidade geográfica** | ✅ Até municipal | ✅ Institucional | ✅ Municipal | ⚠️ NUTS 2/3 |
| **Formatos** | CSV, XLSX | JSON, CSV, XLSX, Parquet | JSON, CSV, XLSX, Parquet | JSON, CSV, XLSX, Parquet |
| **Cobertura temática** | ✅ Ampla | ⚠️ Saúde apenas | ✅ Ampla | ✅ Muito ampla |
| **Actualização** | ⚠️ Com lag | ✅ Mensal | ✅ Frequente | ✅ Frequente |
| **Documentação** | ✅ Excelente | ⚠️ Limitada | ✅ Boa | ✅ Excelente |

**Conclusão:** PORDATA é inferior para extração automatizada, mas útil para visualização e alguns indicadores específicos não disponíveis noutras fontes.

---

## DADOS QUE VOCÊ JÁ TEM - RESUMO

### ✅ **Cobertura Atual Excelente:**

**Nível Institucional (426 hospitais):**
- ✅ Financeiro (2014-2025, mensal)
- ✅ Workforce (2014-2025, mensal)
- ✅ Qualidade (2013-2025)

**Nível Municipal (344 municípios):**
- ✅ Demografia (aging, dependency, 2011-2023)
- ✅ Saúde (enfermeiros per capita, 2011-2023)
- ✅ Económico (desemprego NUTS 2, 2011-2025)

**Nível Regional (NUTS 2/3):**
- ✅ PIB (2000-2023)
- ✅ Infraestrutura de saúde (1993-2024)
- ✅ População (2014-2024)
- ✅ Emprego (1995-2023)

**Total:** ~545,000 registos, 174 ficheiros

### ⚠️ **Gaps Identificados:**

**Contexto Macroeconómico (Nacional):**
- ❌ Despesa pública em saúde (% PIB)
- ❌ Dívida pública
- ❌ Défice orçamental
- ❌ Orçamento da saúde

**Contexto Socioeconómico (Regional/Municipal):**
- ❌ Salários regionais
- ⚠️ Taxa de mortalidade (pode estar no INE)
- ⚠️ Médicos municipais (pode estar no INE)

---

## PLANO DE AÇÃO RECOMENDADO

### Fase 1: PORDATA Download Manual (30-45 minutos) ⭐

**Indicadores a descarregar:**
1. Despesa pública em saúde, em % do PIB (nacional, 1995-2024)
2. Dívida pública, em % do PIB (nacional, 1995-2024)
3. Saldo orçamental, em % do PIB (nacional, 1995-2024)
4. Despesas públicas por função: Saúde (nacional, 2000-2024)
5. Remuneração média mensal dos trabalhadores por conta de outrem (NUTS 2, 2010-2024)

**Output:** 5 ficheiros CSV em `pordata_manual_data/`

### Fase 2: Verificar INE API para Indicadores Adicionais (30 minutos)

**Indicadores a procurar:**
- `varcd=0008281` - Taxa de mortalidade
- `varcd=0008276` - Médicos por 1000 habitantes (se existir municipal)
- Outros indicadores de saúde municipal

**Método:** Script Python existente com op=1

### Fase 3: API Banco de Portugal (Opcional, 1-2 horas)

**Se tempo disponível:**
- Criar script para API Banco de Portugal
- Extrair dívida pública, défice, juros
- Formato: multiformat (CSV, XLSX, Parquet)

### Fase 4: NÃO FAZER

❌ Download massivo PORDATA (não vale o tempo)
❌ Web scraping PORDATA (não necessário)
❌ Indicadores de baixa prioridade

---

## CONCLUSÃO FINAL

### ❌ **PORDATA - Download Massivo NÃO É NECESSÁRIO**

**Razões:**
1. Maioria dos dados PORDATA vêm de INE/Eurostat (já extraídos)
2. Sem API (download manual trabalhoso)
3. Valor adicional marginal para maioria dos indicadores
4. Pesquisa já tem ~545,000 registos de fontes primárias

### ✅ **PORDATA - Download Seletivo RECOMENDADO**

**5 indicadores macroeconómicos prioritários:**
- Despesa pública saúde (% PIB)
- Dívida pública (% PIB)
- Défice orçamental (% PIB)
- Orçamento saúde
- Salários regionais

**Tempo:** 30-45 minutos
**Valor:** ✅✅✅ **Alto** - contextualização fiscal crítica

### ✅ **Dados Atuais SÃO SUFICIENTES para Análise Robusta**

**Cobertura:**
- ✅ Nível institucional (426 hospitais)
- ✅ Nível municipal (344 municípios)
- ✅ Nível regional (NUTS 2/3)
- ✅ Séries temporais (2011-2025, alguns desde 1960)
- ✅ Multi-dimensional (financeiro, operacional, demográfico, económico)

**Recomendação Final:**
1. ✅ **Fazer:** Download manual 5 indicadores PORDATA (30 min)
2. ✅ **Fazer:** Verificar INE API para indicadores adicionais (30 min)
3. ⚠️ **Opcional:** API Banco de Portugal (1-2 horas)
4. ❌ **NÃO fazer:** Download massivo PORDATA
5. ✅ **Priorizar:** Análise dos dados já obtidos (~545k registos)

---

## CONTACTOS

**PORDATA:**
- Email: info@pordata.pt
- URL: https://www.pordata.pt
- Organização: Fundação Francisco Manuel dos Santos

**Banco de Portugal:**
- BPstat: https://bpstat.bportugal.pt/
- API: https://bpstat.bportugal.pt/sites/default/files/documentos/bpstat_api_documentation.pdf

**INE (verificação indicadores adicionais):**
- API: https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api_v2
- Email: difusao@ine.pt

---

**Gerado:** 26 de outubro de 2025

**Conclusão:** PORDATA é um agregador útil mas NÃO é necessário fazer download massivo. Download seletivo de 5 indicadores macroeconómicos (30 minutos) adiciona contexto fiscal crítico. Dados atuais (SNS + INE + Eurostat) são suficientes para análise robusta de endividamento hospitalar (2015-2025).

**Prioridade:** ⭐⭐ Download manual seletivo (5 indicadores)
**Tempo estimado:** 30-45 minutos
**Valor adicional:** ✅ MÉDIO-ALTO (contexto macroeconómico)
