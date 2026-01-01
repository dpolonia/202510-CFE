#!/bin/bash
# Compile LaTeX manuscript to PDF using Docker
# Author: Daniel Polonia
# Date: January 2026

set -e

echo "================================================================================"
echo "COMPILING MANUSCRIPT TO PDF"
echo "================================================================================"
echo ""

PROJECT_ROOT="/home/dpolonia/202512-CFE"
PAPER_DIR="07_writing/paper"

cd "$PROJECT_ROOT/$PAPER_DIR"

echo "[Step 1/4] First XeLaTeX pass..."
docker run --rm \
    -v "$PROJECT_ROOT:/work" \
    -w "/work/$PAPER_DIR" \
    texlive/texlive:latest \
    xelatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "[Step 2/4] Processing bibliography with BibTeX..."
docker run --rm \
    -v "$PROJECT_ROOT:/work" \
    -w "/work/$PAPER_DIR" \
    texlive/texlive:latest \
    bibtex main > /dev/null 2>&1

echo "[Step 3/4] Second XeLaTeX pass (incorporating bibliography)..."
docker run --rm \
    -v "$PROJECT_ROOT:/work" \
    -w "/work/$PAPER_DIR" \
    texlive/texlive:latest \
    xelatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "[Step 4/4] Third XeLaTeX pass (resolving cross-references)..."
docker run --rm \
    -v "$PROJECT_ROOT:/work" \
    -w "/work/$PAPER_DIR" \
    texlive/texlive:latest \
    xelatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo ""
echo "================================================================================"
echo "PDF COMPILATION COMPLETE ✅"
echo "================================================================================"
echo ""
echo "Output: $PROJECT_ROOT/$PAPER_DIR/main.pdf"

# Display PDF info
if [ -f main.pdf ]; then
    SIZE=$(ls -lh main.pdf | awk '{print $5}')
    PAGES=$(pdfinfo main.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")
    echo "Size: $SIZE"
    echo "Pages: $PAGES"
    echo ""
    echo "To view: xdg-open main.pdf"
else
    echo "ERROR: PDF not created!"
    exit 1
fi

echo "================================================================================"
