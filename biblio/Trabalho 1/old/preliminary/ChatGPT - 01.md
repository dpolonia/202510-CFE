Daniel — below is a **full mini‑proposal** for **Topic 1**. I keep the tone managerial‑academic, use short phrases inside long paragraphs, and anchor each claim in the Advanced Corporate Finance syllabus (valuation, cost of capital, capital budgeting, disclosure, and asset measurement) to ensure fit with your module at Aveiro. ([ua.pt](https://www.ua.pt/en/uc/14215 "Advanced Corporate Finance -  Universidade de Aveiro"))

---

## **Topic 1 — Shadow capital for VBHC: valuing population‑health data as an intangible asset and tracing its effects on WACC and capital budgeting under EHDS/DGA**

**Motivation and gap.** Value‑based healthcare depends on longitudinal, high‑granularity data; yet most Beveridgean providers expense the generation and curation of datasets; intangible value is thus invisible in investment cases; the result is under‑investment in registries, PROMs/PREMs, and linkage infrastructure; accounting rules intensify the problem. IAS 38 permits recognition of **identifiable** intangibles, acquired or internally developed when strict criteria are met; however many internally generated information assets are expensed; IPSAS for the public sector mirrors this stance; disclosure is limited; investors, boards, and ministries underestimate the true stock of _data capital_. A regulatory shift now increases monetisable and mission‑critical use: the **Data Governance Act** creates trusted mechanisms and “data altruism” structures; the **European Health Data Space** establishes **data‑permit** regimes and secure processing for secondary use; expected cash‑flows from high‑quality datasets therefore rise, and real option value expands; yet no finance‑grounded method exists to price health datasets for capital budgeting in public providers. This paper closes that gap. ([IFRS](https://www.ifrs.org/issued-standards/list-of-standards/ias-38-intangible-assets/?utm_source=chatgpt.com "IAS 38 Intangible Assets - IFRS"))

**Research questions and hypotheses.** RQ1: can we construct a defensible **shadow asset register** for clinical, administrative, and PROM/PREM datasets using accepted valuation families (cost‑based, income‑based, market proxies); and does its publication improve capital allocation toward VBHC enablers; RQ2: does enhanced dataset disclosure and measurement reduce financing frictions observable in provider‑level investment behavior; RQ3: does the EHDS/DGA regime materially modify the **option value** and **income potential** of provider datasets. _H1:_ better disclosure of valued data assets lowers the provider’s effective cost of capital by reducing information risk and altering assessed cash‑flow covariances; _H2:_ providers that adopt the shadow register raise VBHC‑related capex share and display lower investment–cash‑flow sensitivity; _H3:_ effects are strongest where EHDS‑style secondary‑use demand is higher and where permit pricing is transparent. These hypotheses draw on established finance results linking disclosure quality to the cost of capital, and on the investment–cash‑flow sensitivity literature as a proxy for financing frictions, while acknowledging its identification debates. ([EconPapers](https://econpapers.repec.org/RePEc%3Abla%3Ajoares%3Av%3A45%3Ay%3A2007%3Ai%3A2%3Ap%3A385-420?utm_source=chatgpt.com "Accounting Information, Disclosure, and the Cost of Capital"))

**Design and identification.** A two‑part design. Part A builds **valuation blueprints** by dataset class; we map benefits under three regimes: pre‑EHDS baseline; _EHDS‑compliant secondary use_ with HDAB permits; and _altruism‑enabled_ sharing under DGA; we parameterise volumes and prices from **Findata** (Finland’s permit authority) and EHDS guidance; we then construct dataset‑level NPVs and **option trees** (defer/expand/abandon) to capture staged data curation and future linkage; we publish a register and a transparency note. Part B exploits _staggered adoption_ of the register across Portuguese **ULS** and comparable entities (e.g., IPOs), estimating difference‑in‑differences in VBHC capex share and in the slope of investment on internal cash‑flow; we supplement with event‑time plots around EHDS milestones and **Findata fee decrees** to anchor income‑based scenarios; we test for concurrent confounders with matched comparators. The identification strategy is pragmatic: we seek pre‑trends, use robust staggered DID estimators, and run placebo outcomes where data assets are irrelevant. ([Findata](https://findata.fi/en/pricing/?utm_source=chatgpt.com "Pricing - Findata"))

**Data and measures.** 
_Accounting and governance:_ 
IAS 38 and IPSAS 31 texts to define recognition and disclosure baselines; 
the **SNS** consolidated accounts series (SNC‑AP since 2018) and provider **Relatórios e Contas 2024** (e.g., Matosinhos, Leiria, Alto Minho) to extract intangible‑asset lines, digital capex, and working‑capital metrics; 
**Portal da Transparência** and ACSS releases to track quality and activity indicators relevant to VBHC; 
_Permits and prices:_ **Findata** permit/decision fees current in 2024–2025 to calibrate income models; 
_EHDS context:_ the Official Journal text and Commission pages to code secondary‑use pathways, HDAB powers, revocation penalties, and secure‑processing constraints. We define outcomes as: share of capex in digital/measurement; presence and coverage of PROM/PREM collection; arrears and DPO; and investment–cash‑flow sensitivity at provider‑year level; we define “treated” as providers that publicly adopt the register and accompanying disclosure. ([ifacweb.blob.core.windows.net](https://ifacweb.blob.core.windows.net/publicfiles/2024-12/B04-IPSAS-31.pdf?utm_source=chatgpt.com "INTERNATIONAL PUBLIC SECTOR ACCOUNTING STANDARDSTM"))

**Valuation methodology.** 
For each dataset class we triangulate **cost**, **income**, and **market** approaches. 
Cost: historical and replacement costs of collection, cleaning, curation, linkage, and governance, net of depreciation from schema drift; 
Income: cash‑flow proxies from secondary‑use permits, decision fees, data‑processing charges, and expected demand under EHDS; scenarios include public‑interest fee waivers; 
Market: comparable access terms from EU permit authorities (e.g., Findata) and NHS TRE/SDE models when public; we integrate **option value** by modeling staged curation and cross‑border use cases; sensitivity analysis covers fee elasticity, application failure rates, and revocation risks under EHDS. 
We then compute a **shadow WACC** for the data asset portfolio, combining budget funding with philanthropic or endowment elements where present; 
the finance logic is standard; 
better measurement and disclosure reduce information risk and may lower the composite capital charge for data‑intensive projects; 
we do not propose balance‑sheet recognition unless IAS/IPSAS tests are met; 
we propose **note‑level disclosure** to support investment decisions while remaining standards‑compliant. ([ONE MP](https://one.oecd.org/document/DSTI/CDEP/GD%282022%291/FINAL/en/pdf?utm_source=chatgpt.com "Measuring the value of data and data flows - OECD"))

**Econometric tests and robustness.** 
We estimate event‑time DID models for the VBHC‑capex share and for investment–cash‑flow sensitivity; 
we adopt **Sun–Abraham** style estimators for staggered treatment; 
we include EHDS interaction terms where national HDAB implementation advances faster; 
we test alternative cash‑flow proxies and exclude entities with atypical funding shocks; 
we benchmark disclosure effects to the **Lambert–Leuz–Verrecchia** predictions; 
we address the Kaplan–Zingales critique by using multiple constraint proxies and by testing whether sensitivity declines most where disclosure changes are largest; 
we run placebo tests on intangible categories unaffected by dataset valuation (e.g., legacy software amortisation). ([EconPapers](https://econpapers.repec.org/RePEc%3Abla%3Ajoares%3Av%3A45%3Ay%3A2007%3Ai%3A2%3Ap%3A385-420?utm_source=chatgpt.com "Accounting Information, Disclosure, and the Cost of Capital"))

**Expected contribution.** 
Conceptually, we transplant _corporate‑finance_ tools into a Beveridgean context to make _data for value_ **bankable**; 
we show how **asset measurement + disclosure** re‑shape hurdle rates and portfolio choice for VBHC infrastructure; 
practically, we deliver a reproducible **register template**, a **pricing playbook** aligned with EHDS permits and DGA altruism, and a **board‑level dashboard** linking dataset quality to option value and to the capital budget; 
policy‑wise, we inform standard‑setters on whether note‑level disclosure of data assets can improve allocative efficiency even without strict recognition. ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2025/327/oj/eng?utm_source=chatgpt.com "Regulation - EU - 2025/327 - EN - EUR-Lex"))

**Feasibility and risks.** 
Feasible because legal texts and fee schedules are public; provider accounts for 2024 are posted; 
EHDS provisions and Commission materials are stable and widely summarised; 
the **SNS transparency portal** is active again; 
main risks are measurement error in attributing income to datasets and concurrent reforms; 
we mitigate with conservative income scenarios based on official **Findata** fees, strict pre‑trend checks, IPO comparators, and sensitivity bounds on demand. ([ulsm.min-saude.pt](https://www.ulsm.min-saude.pt/wp-content/uploads/sites/16/2025/05/Relatorio-e-Contas_2024_compressed.pdf?utm_source=chatgpt.com "RELATÓRIO E CONTAS"))

