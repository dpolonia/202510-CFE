# Directory Reorganization Plan
## Corporate Finance Research on Portuguese SNS

**Date**: 2025-12-31
**Purpose**: Optimize folder structure for scientific paper development in corporate finance

---

## Recommended Structure

```
202512-CFE/
│
├── 01_admin/                    # Administrative documents
│   ├── proposal/
│   │   └── research_proposal.md
│   ├── correspondence/
│   │   └── ACSS_request_letter.md
│   └── project_info/
│       └── README.md
│
├── 02_literature/               # Bibliography and references
│   ├── key_papers/              # Core references for the study
│   ├── background/              # General background reading
│   ├── methodology/             # Methods references
│   ├── portuguese_context/      # Portugal/SNS specific papers
│   └── course_materials/        # CFE course materials
│
├── 03_data/                     # All data files
│   ├── raw/                     # Original, unmodified data
│   │   ├── eurostat/
│   │   │   ├── macro/           # Eurostat macro indicators
│   │   │   └── regional/        # Eurostat regional data
│   │   ├── ine/                 # Portuguese Statistical Institute
│   │   │   ├── current/
│   │   │   └── historical/
│   │   ├── sns/                 # SNS Transparency Portal
│   │   │   ├── financial/
│   │   │   ├── operational/
│   │   │   └── quality/
│   │   ├── acss/                # ACSS data
│   │   └── other/               # Other sources (OECD, Banco Portugal, etc.)
│   │
│   ├── processed/               # Cleaned and processed data
│   │   ├── consolidated/        # Merged datasets
│   │   ├── panel/               # Panel data (hospital-year)
│   │   └── variables/           # Constructed variables
│   │
│   ├── external/                # External validation data
│   │   ├── governance/          # Board composition, audits
│   │   └── interventions/       # Government interventions, capital injections
│   │
│   └── metadata/                # Data documentation
│       ├── data_dictionary.xlsx
│       ├── source_documentation.md
│       └── variable_definitions.md
│
├── 04_code/                     # All analysis code
│   ├── 01_data_collection/      # Scripts to download/extract data
│   │   ├── eurostat_extractor.py
│   │   ├── ine_extractor.py
│   │   ├── sns_scraper.py
│   │   └── README.md
│   │
│   ├── 02_data_processing/      # Data cleaning and merging
│   │   ├── clean_financial_data.py
│   │   ├── merge_datasets.py
│   │   ├── create_panel.py
│   │   └── README.md
│   │
│   ├── 03_variable_construction/ # Building analysis variables
│   │   ├── phfsi_components.py
│   │   ├── governance_index.py
│   │   ├── control_variables.py
│   │   └── README.md
│   │
│   ├── 04_analysis/             # Statistical analysis
│   │   ├── descriptive_stats.py
│   │   ├── panel_regression.py
│   │   ├── diff_in_diff.py
│   │   ├── validation.py
│   │   └── README.md
│   │
│   ├── 05_visualization/        # Plots and figures
│   │   ├── figure1_phfsi_distribution.py
│   │   ├── figure2_trends.py
│   │   ├── figure3_did_plots.py
│   │   └── README.md
│   │
│   └── utils/                   # Helper functions
│       ├── data_utils.py
│       ├── analysis_utils.py
│       └── plot_utils.py
│
├── 05_notebooks/                # Jupyter notebooks for exploration
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_phfsi_development.ipynb
│   ├── 03_preliminary_results.ipynb
│   └── README.md
│
├── 06_output/                   # Analysis outputs
│   ├── figures/                 # Publication-quality figures
│   │   ├── main/                # Main text figures
│   │   └── appendix/            # Supplementary figures
│   │
│   ├── tables/                  # Publication-quality tables
│   │   ├── main/                # Main text tables
│   │   └── appendix/            # Supplementary tables
│   │
│   ├── results/                 # Regression outputs, statistics
│   │   ├── descriptive/
│   │   ├── regressions/
│   │   └── robustness/
│   │
│   └── data_summaries/          # Data documentation outputs
│
├── 07_writing/                  # Manuscript and presentations
│   ├── paper/
│   │   ├── main.tex             # Main LaTeX file (or .docx)
│   │   ├── sections/            # Paper sections
│   │   │   ├── 01_introduction.tex
│   │   │   ├── 02_theory.tex
│   │   │   ├── 03_methods.tex
│   │   │   ├── 04_data.tex
│   │   │   ├── 05_results.tex
│   │   │   ├── 06_discussion.tex
│   │   │   └── 07_conclusion.tex
│   │   ├── references.bib
│   │   └── appendix.tex
│   │
│   ├── presentations/
│   │   ├── conference_2025/
│   │   └── seminar_slides/
│   │
│   └── drafts/                  # Earlier versions
│
├── 08_documentation/            # Project documentation
│   ├── methodology_notes.md
│   ├── data_sources.md
│   ├── analysis_plan.md
│   └── changelog.md
│
├── venv/                        # Python virtual environment (keep)
│
├── .git/                        # Git repository (keep)
├── .gitignore                   # Git ignore file
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
└── README.md                    # Project README

```

---

## Reorganization Actions

### Phase 1: Create New Structure
1. Create all new directories as specified above
2. Copy (don't move yet) critical files to test structure

### Phase 2: Migrate Administrative Files
**From root → To 01_admin/**
- `99 Proposal.md` → `01_admin/proposal/research_proposal.md`
- `ACSS_request_letter_template.md` → `01_admin/correspondence/`
- `CFE DanielPolonia 20251107 2359.pdf` → `01_admin/proposal/` (submitted version)
- `README.md` → Update and keep at root + version in `01_admin/project_info/`

### Phase 3: Migrate Literature
**From biblio/ → To 02_literature/**
- `biblio/Trabalho 1/` → `02_literature/key_papers/`
- `biblio/Trabalho 2/` → `02_literature/background/`
- `biblio/Aulas/` → `02_literature/course_materials/`
- `biblio/Trabalho 1/old/Portuguese/` → `02_literature/portuguese_context/`

### Phase 4: Consolidate Data
**Raw Data Organization:**

**Eurostat Data:**
- `eurostat_macro_data/` → `03_data/raw/eurostat/macro/`
- `eurostat_data_multiformat/` → `03_data/raw/eurostat/regional/`
- ARCHIVE: `eurostat_data_OLD_NATIONAL/` → Keep for reference or delete if duplicated

**INE Data:**
- `ine_data_multiformat/` → `03_data/raw/ine/current/`
- `ine_historical_data/` → `03_data/raw/ine/historical/`
- ARCHIVE: `ine_data/` and `ine_data_OLD_BACKUP/` → Delete if duplicates exist in multiformat

**SNS Data:**
- `sns_data_multiformat/` → `03_data/raw/sns/`
- Subdivide by type (financial, operational, quality) if needed
- `sns_data/` → Evaluate if duplicate, then archive or integrate

**Other Sources:**
- `source/` → `03_data/raw/acss/` (recent ACSS downloads)
- `macro_indicators_consolidated/` → `03_data/processed/consolidated/` (already processed)

**Metadata:**
- `metadata/` → `03_data/metadata/`
- `docs/FINAL_DATA_SUMMARY.md` → `03_data/metadata/`
- All other .md files in docs/ → `03_data/metadata/`

### Phase 5: Organize Code
**From scripts/ → To 04_code/**
- `scripts/eurostat_macro_extractor.py` → `04_code/01_data_collection/`
- `scripts/consolidate_macro_indicators.py` → `04_code/02_data_processing/`

**Nested Project:**
- Investigate `202512-CFE/202512-CFE/` contents
- If contains analysis code → move to `04_code/04_analysis/`
- If duplicates → delete

### Phase 6: Setup Output Structure
- Create empty directories in `06_output/`
- Add README files with instructions for each subdirectory

### Phase 7: Writing Setup
- Create `07_writing/paper/` structure
- Add LaTeX template or Word template
- Create bibliography file from references

### Phase 8: Documentation
**Create new documentation files:**
1. `08_documentation/data_sources.md` - Compile from existing docs
2. `08_documentation/methodology_notes.md` - Extract from proposal
3. `08_documentation/analysis_plan.md` - From proposal Section 3
4. `README.md` - New comprehensive project README

### Phase 9: Cleanup
**Archive or Delete:**
- `99 old/` → Review and either delete or move to `01_admin/archive/`
- `__pycache__/` → Delete (will regenerate)
- `.env:Zone.Identifier` → Delete (Windows metadata)
- `firebase-debug.log` → Delete
- `_ul` → Delete (empty file)
- Duplicate data folders after verification
- `TC NUTS 2013_ NUTS 2024 a município.xlsx` → Move to `03_data/external/` or metadata

### Phase 10: Git Housekeeping
- Update `.gitignore` to reflect new structure
- Ensure large data files are excluded
- Ensure .env is excluded
- Add venv/ to .gitignore if not already

---

## File Mapping Summary

| Current Location | New Location | Action |
|-----------------|--------------|--------|
| `99 Proposal.md` | `01_admin/proposal/research_proposal.md` | Move |
| `CFE DanielPolonia 20251107 2359.pdf` | `01_admin/proposal/submitted_version.pdf` | Move |
| `ACSS_request_letter_template.md` | `01_admin/correspondence/` | Move |
| `0003300035.pdf` | `02_literature/portuguese_context/` | Move |
| `biblio/` | `02_literature/` | Restructure |
| `eurostat_macro_data/` | `03_data/raw/eurostat/macro/` | Move |
| `eurostat_data_multiformat/` | `03_data/raw/eurostat/regional/` | Move |
| `eurostat_data_OLD_NATIONAL/` | Archive or delete | Evaluate |
| `ine_data_multiformat/` | `03_data/raw/ine/current/` | Move |
| `ine_historical_data/` | `03_data/raw/ine/historical/` | Move |
| `ine_data/`, `ine_data_OLD_BACKUP/` | Archive or delete | Evaluate |
| `sns_data_multiformat/` | `03_data/raw/sns/` | Move |
| `sns_data/` | Evaluate | Compare with multiformat |
| `source/` | `03_data/raw/acss/` | Move |
| `macro_indicators_consolidated/` | `03_data/processed/consolidated/` | Move |
| `metadata/` | `03_data/metadata/` | Move |
| `docs/*.md` | `03_data/metadata/` | Move |
| `scripts/` | `04_code/01_data_collection/` and `04_code/02_data_processing/` | Distribute |
| `202512-CFE/202512-CFE/` | Evaluate and distribute | Investigate |
| `notebooks/` | `05_notebooks/` | Move (currently empty) |
| `99 old/` | `01_admin/archive/` or delete | Evaluate |
| `__pycache__/` | Delete | Remove |
| `.env` | Keep at root | Keep |
| `requirements.txt` | Keep at root | Keep |
| `README.md` | Update at root | Rewrite |
| `.gitignore` | Update at root | Update |
| `venv/` | Keep at root | Keep |

---

## Benefits of New Structure

### 1. **Reproducibility**
- Clear separation of raw vs. processed data
- Code organized by workflow stage
- All outputs traceable to source code

### 2. **Collaboration**
- Standard academic structure (easy for advisors/co-authors)
- Clear documentation
- Version control friendly

### 3. **Paper Writing**
- Direct path from analysis → outputs → manuscript
- Figures and tables organized for publication
- Literature easily accessible

### 4. **Efficiency**
- No duplicate data folders
- Clear naming conventions
- Easy to find any component

### 5. **Professional Presentation**
- Follows best practices for computational research
- Ready for GitHub/OSF publication
- Meets reproducibility standards for journals

---

## Implementation Priority

**High Priority (Do First):**
1. Create new directory structure
2. Migrate administrative files (Phase 2)
3. Organize literature (Phase 3)
4. Create documentation (Phase 8)
5. Update README and .gitignore

**Medium Priority (Do Second):**
6. Consolidate data (Phase 4) - verify no duplicates
7. Organize code (Phase 5)
8. Setup writing structure (Phase 7)

**Low Priority (Do Last):**
9. Setup output directories (Phase 6)
10. Cleanup archives (Phase 9)
11. Git housekeeping (Phase 10)

---

## Notes

- **Backup**: Before any major reorganization, create a full backup
- **Git**: Commit current state before reorganization
- **Verify**: After moving data, verify files with checksums or file counts
- **Document**: Update README.md with new structure explanation
- **Iterate**: This structure can be refined as the project progresses

---

## Next Steps

1. Review this plan
2. Make any adjustments based on your preferences
3. Create a git commit of current state
4. Execute reorganization in phases
5. Test that all critical files are accessible
6. Update documentation
7. Resume research work in new structure
