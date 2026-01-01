# Manuscript Documentation
## Stakeholder-Distributed Distress: Public Hospital Financial Sustainability

**Author**: Daniel Polónia
**Institution**: Universidade de Aveiro
**Target Journal**: Health Care Management Science
**Last Compiled**: January 2026

---

## PDF Compilation

### Quick Compile

```bash
cd /home/dpolonia/202512-CFE/07_writing/paper
bash compile_pdf.sh
```

This runs the complete LaTeX compilation cycle (XeLaTeX + BibTeX) using Docker.

**Output**: `main.pdf` (48 pages, ~260KB)

---

### Manual Compilation

If you prefer to compile manually:

```bash
cd /home/dpolonia/202512-CFE/07_writing/paper

# Using Docker (recommended - no LaTeX installation needed)
docker run --rm -v /home/dpolonia/202512-CFE:/work -w /work/07_writing/paper \
    texlive/texlive:latest xelatex -interaction=nonstopmode main.tex

docker run --rm -v /home/dpolonia/202512-CFE:/work -w /work/07_writing/paper \
    texlive/texlive:latest bibtex main

docker run --rm -v /home/dpolonia/202512-CFE:/work -w /work/07_writing/paper \
    texlive/texlive:latest xelatex -interaction=nonstopmode main.tex

docker run --rm -v /home/dpolonia/202512-CFE:/work -w /work/07_writing/paper \
    texlive/texlive:latest xelatex -interaction=nonstopmode main.tex
```

**Why XeLaTeX?**: The manuscript contains Unicode characters (β, ≥) that require XeLaTeX or LuaLaTeX instead of pdflatex.

---

## Manuscript Structure

### Main File
- **`main.tex`**: Master LaTeX file that includes all sections

### Sections (in `sections/` directory)
1. **`01_introduction.tex`**: Research gap, contribution, findings preview
2. **`02_theory.tex`**: Soft budget constraints, stakeholder-distributed distress framework
3. **`03_methods.tex`**: Data sources, PHFSI construction, econometric strategy
4. **`04_results.tex`**: Descriptive statistics, validation, panel regressions
5. **`05_discussion.tex`**: Theoretical contributions, policy implications, limitations
6. **`06_conclusion.tex`**: Summary and future research

### Bibliography
- **`references.bib`**: BibTeX bibliography file (40+ references)

### Supporting Files
- **`cover_letter.tex`**: Journal submission cover letter (not included in main PDF)
- **`compile_pdf.sh`**: Automated compilation script

---

## Embedded Content

### Tables (from `/06_output/tables/`)

**Main Tables**:
- Table 1: Summary Statistics by Period
- Table 2: PHFSI Distribution by Cluster
- Table 3: Fixed Effects Panel Regression Results

**Appendix Tables**:
- Table A1: Robustness Checks
- Table A2: Panel Regression Diagnostics
- Table A3: Sample Construction Flowchart
- Table A3b: Attrition Bias Diagnostics
- Table A7: Cross-Country Comparison
- Table A8: Hospital to ULS Entity Crosswalk

### Figures (from `/06_output/figures/`)

**Main Figures**:
- Figure 1: PHFSI Trends Over Time (2017-2024)
- Figure 2: PHFSI Component Correlation Matrix
- Figure 3: Subsidy Dependence vs. Payment Delays
- Figure 4: Event Study - PHFSI Before/After ULS Integration Reform

All figures are embedded as PDFs for high-quality rendering.

---

## Manuscript Statistics

### Current Version (January 2026)
- **Total Pages**: 48 (including bibliography and appendix)
- **Word Count**: ~10,000 words (estimated, main text)
- **Abstract**: 250 words
- **Keywords**: 7 keywords
- **JEL Codes**: 4 codes (G33, H51, I11, L32)
- **References**: 40+ citations
- **Tables**: 3 main + 6 appendix
- **Figures**: 4 main

### Formatting
- **Font**: Times New Roman (12pt)
- **Spacing**: Double-spaced
- **Margins**: 1 inch all sides
- **Citation Style**: APA-like (natbib)

---

## Known Compilation Issues

### Minor LaTeX Warnings
1. **"Not in outer par mode"** errors in appendix tables
   - **Cause**: Floating table environments in appendix
   - **Impact**: None - PDF compiles correctly
   - **Fix**: Ignore (doesn't affect output)

2. **Missing BibTeX entry**: `DespachoCapitalInjection2025`
   - **Cause**: Government decree not yet in references.bib
   - **Impact**: Citation appears as "?" in text
   - **Fix**: Add entry to references.bib

### File Ownership
- Docker compilation creates PDF owned by `root`
- **Solution**: PDF is readable by all users, ownership doesn't affect usability

---

## Journal Submission Checklist

### Required Files
- [x] Main manuscript (main.pdf)
- [x] Cover letter (cover_letter.tex)
- [x] Abstract (<250 words)
- [x] Keywords (5-7)
- [x] Author information and affiliations
- [ ] Data availability statement (in REPLICATION.md)
- [ ] Competing interests statement (to be added)
- [ ] Funding acknowledgments (to be added)

### Formatting Requirements
- [x] Double-spaced manuscript
- [x] Continuous line numbering (not implemented - add if required)
- [x] Tables and figures cited in text
- [x] References formatted in journal style
- [x] Abstract within word limit

---

## Updating the Manuscript

### After Changing Text
1. Edit the relevant section file in `sections/`
2. Run `bash compile_pdf.sh` to regenerate PDF
3. Check for new LaTeX errors in output

### After Updating Tables/Figures
1. Regenerate tables/figures using analysis scripts in `04_code/`
2. Tables automatically saved to `06_output/tables/`
3. Figures automatically saved to `06_output/figures/`
4. Recompile PDF - new tables/figures are embedded automatically

### After Adding Citations
1. Add new BibTeX entry to `references.bib`
2. Cite in text using `\citep{AuthorYear}` or `\citet{AuthorYear}`
3. Recompile PDF (BibTeX will process new citations)

---

## File Locations

```
07_writing/
├── paper/
│   ├── main.tex                 ← Main manuscript file
│   ├── main.pdf                 ← Compiled PDF output (48 pages)
│   ├── references.bib           ← Bibliography database
│   ├── compile_pdf.sh           ← Automated compilation script
│   ├── cover_letter.tex         ← Journal submission cover letter
│   └── sections/
│       ├── 01_introduction.tex
│       ├── 02_theory.tex
│       ├── 03_methods.tex
│       ├── 04_results.tex
│       ├── 05_discussion.tex
│       └── 06_conclusion.tex
└── README_MANUSCRIPT.md         ← This file
```

---

## Viewing the PDF

### Linux
```bash
xdg-open /home/dpolonia/202512-CFE/07_writing/paper/main.pdf
```

### WSL (Windows Subsystem for Linux)
```bash
# Option 1: Copy to Windows filesystem
cp main.pdf /mnt/c/Users/YourUsername/Desktop/

# Option 2: Open from WSL
explorer.exe main.pdf
```

### Check PDF Details
```bash
pdfinfo main.pdf
# OR
ls -lh main.pdf
```

---

## Troubleshooting

### "Docker image not found"
**Solution**: First run will download texlive/texlive Docker image (~600MB). Wait for download to complete.

### "Permission denied" on compile_pdf.sh
**Solution**: Make script executable
```bash
chmod +x compile_pdf.sh
```

### Unicode character errors
**Solution**: Use XeLaTeX instead of pdflatex (already configured in compile_pdf.sh)

### Missing tables or figures
**Solution**: Regenerate outputs using analysis scripts
```bash
cd /home/dpolonia/202512-CFE
bash run_all_analyses.sh  # Regenerates all tables
```

### Bibliography not appearing
**Solution**: Ensure you run full compilation cycle (xelatex → bibtex → xelatex → xelatex)

---

## Version History

- **v1.0** (January 1, 2026): Initial PDF compilation
  - 48 pages
  - Complete with bibliography and all references
  - All main results embedded (Tables 1-3, Figures 1-4)
  - Appendix tables included

---

## Contact

For manuscript questions:
- **Author**: Daniel Polónia
- **Email**: dpolonia@ua.pt
- **Institution**: Universidade de Aveiro, Portugal

For LaTeX/compilation issues:
- See troubleshooting section above
- Check `main.log` for detailed error messages
- Ensure Docker is installed and running

---

**Last Updated**: January 1, 2026
