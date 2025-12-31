# BICSP (BI Cuidados de Saúde Primários) - Análise de Disponibilidade de Dados

**URL:** https://bicsp.min-saude.pt/
**Data:** 26 de outubro de 2025
**Propósito:** Averiguar indicadores disponíveis e possibilidade de download

---

## RESUMO EXECUTIVO

**Status:** ⚠️ **Dados NÃO diretamente descarregáveis via API ou exportação automática**

**Tipo de Portal:**
- Portal SharePoint com visualizações Power BI embebidas
- Focado em **Cuidados de Saúde Primários** (Primary Healthcare)
- Visualizações interativas (não downloads diretos de dados)

**Formatos de Download:**
- ❌ XLS/XLSX - Não disponível diretamente
- ❌ JSON - Não disponível
- ❌ Parquet - Não disponível
- ❌ CSV - Não disponível
- ⚠️ Possível exportação manual via Power BI (limitada)

---

## CONTEÚDO DISPONÍVEL

### Tipo de Dados:

**Foco:** Cuidados de Saúde Primários (CSP)

**Indicadores Identificados:**

1. **Unidades Funcionais (UF) por Tipo:**
   - UCC (Unidades de Cuidados na Comunidade)
   - UCSP (Unidades de Cuidados de Saúde Personalizados)
   - URAP (Unidades de Recursos Assistenciais Partilhados)
   - USP (Unidades de Saúde Pública)
   - USF-A (Unidades de Saúde Familiar - Modelo A)
   - USF-B (Unidades de Saúde Familiar - Modelo B)

2. **Distribuição Geográfica:**
   - Por Administração Regional de Saúde (ARS)
   - Por região
   - Por ULS (Unidades Locais de Saúde)

3. **Contratualização:**
   - IDE (Índice de Desempenho Económico)
   - IDG (Índice de Desempenho Global)
   - Relatórios de Atividade

4. **Estatísticas de Atividade:**
   - Número de unidades
   - Distribuição por tipo
   - Performance contratual

---

## ESTRUTURA TÉCNICA

### Plataforma:

**Base:** Microsoft SharePoint + Power BI

**Componentes:**
- Interface web SharePoint
- Dashboards Power BI embebidos
- Sistema de filtros interativos (ano, região, ULS, área CSP)

**Acesso:**
- Público (sem necessidade de login aparente)
- Visualizações interativas
- Sistema de pesquisa de relatórios

### Limitações Técnicas:

**Sem API Pública:**
- ❌ Não existe API REST documentada
- ❌ Não há endpoints para download de dados
- ❌ Sem formato de exportação automática

**Power BI Embeds:**
- Visualizações embebidas (iframes)
- Possível exportação manual para Excel via interface Power BI
- Limitado aos dados visíveis no relatório

---

## PÁGINAS PRINCIPAIS IDENTIFICADAS

### 1. **Página Principal**
   - URL: https://bicsp.min-saude.pt/
   - Conteúdo: Dashboards gerais, estatísticas de UF

### 2. **Relatórios de Atividade**
   - URL: https://bicsp.min-saude.pt/pt/contratualizacao/relatoriosatividade/Paginas/default.aspx
   - Conteúdo: Sistema de pesquisa de relatórios
   - Filtros: Ano, Região, ULS, Área CSP, UF
   - **Status:** Sem resultados visíveis sem filtros aplicados

### 3. **Secção de Contratualização**
   - Indicadores de desempenho (IDE, IDG)
   - Dados de performance

---

## POSSIBILIDADES DE EXTRAÇÃO DE DADOS

### ❌ **Método 1: Download Direto (NÃO disponível)**

**Status:** Não implementado

O site **NÃO oferece**:
- Botões de download direto
- Ficheiros XLS/CSV/JSON para download
- API de dados abertos
- Exportação em massa

### ⚠️ **Método 2: Exportação Manual via Power BI (Limitada)**

**Como funciona:**
1. Aceder aos dashboards Power BI
2. Clicar no menu de exportação do Power BI (se disponível)
3. Exportar para Excel (dados visíveis apenas)

**Limitações:**
- Apenas dados visíveis no dashboard atual
- Requer interação manual
- Limitação de linhas (geralmente 30.000 ou 150.000 dependendo da licença)
- Formato: XLSX apenas
- Não automatizável

**Exemplo:**
```
1. Aceder ao dashboard
2. Clicar "..." no visual
3. Selecionar "Export data" → "Excel"
4. Download de ficheiro .xlsx
```

### ⚠️ **Método 3: Contacto Direto (Recomendado)**

**Email:** servicedesk@spms.min-saude.pt

**Pedido sugerido:**
```
Assunto: Pedido de Acesso a Dados - BICSP

Exmo(a) Senhor(a),

Solicito informação sobre a possibilidade de aceder aos dados do portal
BICSP (https://bicsp.min-saude.pt/) para fins de investigação académica.

Especificamente, gostaria de saber:

1. Se existe API ou método automático para download de dados
2. Que indicadores estão disponíveis para exportação
3. Formatos disponíveis (XLS, CSV, JSON, Parquet)
4. Cobertura temporal dos dados (anos disponíveis)
5. Procedimento para obter acesso aos dados

Contexto: Investigação de doutoramento sobre [seu tema]

Agradeço a vossa colaboração,
[Nome]
```

### ❌ **Método 4: Web Scraping (NÃO recomendado)**

**Status:** Tecnicamente difícil e legalmente questionável

**Razões:**
- Dados dentro de iframes Power BI (difícil de extrair)
- Possível violação de termos de serviço
- Dados dinâmicos (JavaScript)
- Requer autenticação Power BI
- Não é uma fonte de dados abertos

---

## COMPARAÇÃO COM OUTRAS FONTES

### vs. SNS Transparência (transparencia.sns.gov.pt)

| Característica | BICSP | SNS Transparência |
|----------------|-------|-------------------|
| **API pública** | ❌ Não | ✅ Sim (CKAN API) |
| **Download direto** | ❌ Não | ✅ Sim (CSV, XLS, JSON) |
| **Foco** | Cuidados Primários | Hospitais |
| **Tipo de dados** | UF, IDE, IDG | Financeiro, Workforce |
| **Formato** | Power BI embeds | Dados estruturados |
| **Automatização** | ❌ Não | ✅ Sim |

**Conclusão:** SNS Transparência é muito superior para extração automatizada

### vs. INE (ine.pt)

| Característica | BICSP | INE |
|----------------|-------|-----|
| **API** | ❌ Não | ✅ Sim |
| **Dados históricos** | ⚠️ Limitado | ✅ Sim (2011-2025) |
| **Granularidade** | UF, Região | Municipal, NUTS |
| **Automatização** | ❌ Não | ✅ Sim |

### vs. Eurostat

| Característica | BICSP | Eurostat |
|----------------|-------|----------|
| **API** | ❌ Não | ✅ Sim |
| **Cobertura** | Portugal (CSP) | Europa |
| **Séries temporais** | ⚠️ Limitadas | ✅ Longas (1960+) |

---

## DADOS QUE PODEM SER ÚTEIS (Se acessíveis)

### Se conseguir obter dados do BICSP:

**Indicadores Potencialmente Úteis:**

1. **Número de Unidades de Saúde Primária por Município**
   - Distribuição geográfica
   - Tipo de unidade
   - Pode correlacionar com envelhecimento populacional

2. **IDE/IDG (Índices de Desempenho)**
   - Performance das unidades de saúde primária
   - Pode indicar qualidade dos cuidados preventivos
   - Potencial relação com pressão hospitalar

3. **Atividade dos CSP**
   - Volume de atendimentos
   - Capacidade instalada
   - Possível relação inversa com internamentos hospitalares

**Utilidade para sua Pesquisa:**

- **Variável de Controlo:** Acesso a cuidados primários vs. pressão hospitalar
- **Hipótese:** Melhor acesso a CSP → menor pressão sobre hospitais → menor endividamento
- **Análise Regional:** Regiões com mais/melhores CSP podem ter hospitais menos sobrecarregados

---

## ALTERNATIVAS PARA DADOS DE CUIDADOS PRIMÁRIOS

### Se BICSP não for acessível, considere:

### 1. **INE - Indicadores de Saúde**
- **Disponível:** ✅ Sim (via API)
- **Indicador:** Enfermeiros por 1000 habitantes (municipal)
- **Já extraído:** ✅ Sim (ind_0008277, 2011-2023)

### 2. **Eurostat - Primary Healthcare**
- **Dataset:** hlth_rs_*  (recursos de saúde)
- **Nível:** NUTS 2
- **Já extraído:** ✅ Parcial (hospital beds, physicians)

### 3. **PORDATA - Cuidados de Saúde**
- **URL:** https://www.pordata.pt
- **Cobertura:** Extensiva (saúde primária e hospitalar)
- **Download:** Manual (CSV)
- **Vantagem:** Séries longas, bem documentado

### 4. **ACSS (Administração Central do Sistema de Saúde)**
- **URL:** https://www.acss.min-saude.pt/
- **Dados:** Benchmarking, contratualização
- **Formato:** Relatórios PDF, possíveis Excel

### 5. **DGS (Direção-Geral da Saúde)**
- **URL:** https://www.dgs.pt/
- **Dados:** Estatísticas de saúde, boletins epidemiológicos
- **Formato:** PDF, Excel

---

## RECOMENDAÇÕES

### Para sua Investigação de Doutoramento:

#### ✅ **Opção 1: Contactar SPMS Diretamente (RECOMENDADO)**

**Ação:**
1. Enviar email para servicedesk@spms.min-saude.pt
2. Explicar contexto académico
3. Solicitar dados em formato estruturado (CSV/Excel)
4. Pedir cobertura temporal máxima

**Vantagens:**
- Acesso oficial
- Dados completos e validados
- Possível acesso a indicadores não públicos
- Suporte técnico

**Probabilidade de Sucesso:** 🔶 Média
- SPMS costuma colaborar com investigação académica
- Pode requerer autorização formal
- Tempo de resposta: 2-4 semanas

#### ⚠️ **Opção 2: Exportação Manual Power BI**

**Quando usar:**
- Para dados pontuais/específicos
- Complemento a outras fontes
- Visualização rápida de tendências

**Limitações:**
- Trabalhoso e lento
- Dados limitados
- Não replicável

#### ✅ **Opção 3: Usar Fontes Alternativas**

**Recomendação:**
- INE: Enfermeiros por município (já tem! ✓)
- Eurostat: Recursos de saúde NUTS 2 (já tem! ✓)
- PORDATA: Dados complementares (manual)

**Vantagem:**
- Dados já disponíveis
- Automatizável
- Validado

---

## CONCLUSÃO FINAL

### ❌ **BICSP NÃO é adequado para extração automatizada de dados**

**Razões:**
1. Sem API pública
2. Sem downloads estruturados
3. Baseado em Power BI (visualizações apenas)
4. Requer extração manual limitada

### ✅ **Alternativas SUPERIORES:**

**Para sua pesquisa já tem:**

| Fonte | Dados | Status |
|-------|-------|--------|
| **SNS Transparência** | Hospital financeiro/workforce | ✅ Extraído (305k records) |
| **INE** | Municipal aging, nurses | ✅ Extraído (34k records, 2011-2023) |
| **Eurostat** | Regional GDP, infrastructure | ✅ Extraído (206k records) |

**Total:** ~545,000 registos, 174 ficheiros

**Cobertura:**
- ✅ Nível institucional (426 hospitais)
- ✅ Nível municipal (344 municípios)
- ✅ Séries temporais (2011-2025)
- ✅ Contexto económico e demográfico

### Sobre Cuidados Primários:

**Já tem:**
- ✅ Enfermeiros por 1000 habitantes (municipal, 2011-2023) - INE
- ✅ Médicos por região (NUTS 2, 1993-2024) - Eurostat

**Pode adicionar (se necessário):**
- PORDATA: Dados CSP (download manual)
- Contacto SPMS: Dados BICSP oficiais

**Avaliação:**
- ⚠️ BICSP adiciona valor **marginal** à sua pesquisa
- ✅ Dados atuais (SNS + INE + Eurostat) **suficientes** para análise robusta
- 🎯 Foco deve ser na **análise** dos dados já obtidos

---

## CONTACTOS ÚTEIS

### BICSP / SPMS:
- **Email:** servicedesk@spms.min-saude.pt
- **Site:** https://bicsp.min-saude.pt
- **Organização:** Serviços Partilhados do Ministério da Saúde

### Fontes Alternativas:
- **PORDATA:** https://www.pordata.pt | Contacto: info@pordata.pt
- **ACSS:** https://www.acss.min-saude.pt/ | geral@acss.min-saude.pt
- **DGS:** https://www.dgs.pt/ | geral@dgs.min-saude.pt

---

**Gerado:** 26 de outubro de 2025
**Conclusão:** BICSP não oferece download direto de dados. Contactar SPMS ou usar fontes alternativas (INE, Eurostat, PORDATA).

**Recomendação:** Continuar com dados já extraídos (SNS + INE + Eurostat). Contactar SPMS apenas se necessitar especificamente de indicadores CSP não disponíveis noutras fontes.
