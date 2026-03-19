#!/bin/bash

# PDF Retrieval Experiment Runner
# Quick start script for running the Qdrant PDF retrieval experiment

set -e

echo "================================================"
echo "PDF Retrieval at Scale Experiment"
echo "Based on Qdrant Methodology"
echo "================================================"
echo ""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the experiments directory
if [ ! -f "pdf_retrieval_experiment.py" ]; then
    cd "$(dirname "$0")"
fi

# Check Python
echo -e "${YELLOW}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is required but not installed.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

# Check poppler (for PDF conversion)
echo -e "${YELLOW}Checking poppler...${NC}"
if command -v pdftoppm &> /dev/null; then
    echo -e "${GREEN}✓ poppler found${NC}"
else
    echo -e "${RED}✗ poppler not found${NC}"
    echo ""
    echo "Please install poppler:"
    echo "  macOS:   brew install poppler"
    echo "  Linux:   sudo apt-get install poppler-utils"
    echo ""
    exit 1
fi

# Check dependencies
echo -e "${YELLOW}Checking Python dependencies...${NC}"
if python3 -c "import torch; from colpali_engine.models import ColPali; from qdrant_client import QdrantClient" 2>/dev/null; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

echo ""
echo "================================================"
echo "Starting Experiment"
echo "================================================"
echo ""

# Default parameters
MODEL="${1:-colpali}"
DEVICE="${2:-mps}"
MAX_PAGES="${3:-10}"

echo "Configuration:"
echo "  Model: $MODEL"
echo "  Device: $DEVICE"
echo "  Max pages per PDF: $MAX_PAGES"
echo ""

# Run experiment
python3 pdf_retrieval_experiment.py \
    --model "$MODEL" \
    --device "$DEVICE" \
    --pdf-folder ../dataset/books-pdf \
    --max-pages "$MAX_PAGES"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Experiment completed!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Results saved in: ../output/"
echo ""
echo "To run with different settings:"
echo "  ./run_experiment.sh colpali mps 20    # Process 20 pages"
echo "  ./run_experiment.sh colqwen cuda:0 50  # Use ColQwen on GPU"
