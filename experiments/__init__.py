"""
PDF Retrieval at Scale Experiments
Based on Qdrant's methodology using ColPali/ColQwen with mean pooling optimization

Quick Start:
    cd experiments
    python test_setup.py              # Check environment
    python simple_demo.py             # Quick demo (no large models)
    ./run_experiment.sh colpali mps 5 # Full experiment

For detailed documentation, see:
    - QUICKSTART.md - Getting started guide
    - README.md - Comprehensive documentation
    - EXPERIMENT_SUMMARY.md - Technical details and methodology
"""

__version__ = "1.0.0"
__author__ = "Agno Project"
__all__ = ["PDFRetrievalExperiment", "SimplePDFRetrieval"]
