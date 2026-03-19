#!/usr/bin/env python3
"""
Test script to verify the experiment setup
Checks all dependencies and system requirements
"""

import sys
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (需要 3.8+)")
        return False


def check_dependencies():
    """Check Python dependencies"""
    print("\nChecking Python dependencies...")
    
    dependencies = {
        'torch': 'PyTorch',
        'PIL': 'Pillow',
        'pdf2image': 'pdf2image',
        'qdrant_client': 'Qdrant Client',
        'numpy': 'NumPy'
    }
    
    optional_deps = {
        'colpali_engine': 'ColPali Engine (optional for full experiment)'
    }
    
    all_ok = True
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - Run: pip install {module.replace('_', '-')}")
            all_ok = False
    
    for module, name in optional_deps.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"⚠ {name} - Run: pip install {module.replace('_', '-')}")
    
    return all_ok


def check_poppler():
    """Check if poppler is installed"""
    print("\nChecking poppler...")
    import subprocess
    
    try:
        result = subprocess.run(
            ['pdftoppm', '-h'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0 or result.returncode == 1:  # -h returns 1
            print("✓ poppler installed")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("✗ poppler not found")
    print("  macOS: brew install poppler")
    print("  Linux: sudo apt-get install poppler-utils")
    return False


def check_pdfs():
    """Check if PDF files exist"""
    print("\nChecking PDF files...")
    
    pdf_folder = Path(__file__).parent.parent / "dataset" / "books-pdf"
    
    if not pdf_folder.exists():
        print(f"✗ PDF folder not found: {pdf_folder}")
        return False
    
    pdf_files = list(pdf_folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"✗ No PDF files found in {pdf_folder}")
        return False
    
    print(f"✓ Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files[:3]:
        size_mb = pdf.stat().st_size / 1024 / 1024
        print(f"  - {pdf.name} ({size_mb:.1f} MB)")
    
    if len(pdf_files) > 3:
        print(f"  ... and {len(pdf_files) - 3} more")
    
    return True


def check_device():
    """Check available compute devices"""
    print("\nChecking compute devices...")
    
    try:
        import torch
        
        # CPU is always available
        print("✓ CPU available")
        
        # Check CUDA
        if torch.cuda.is_available():
            print(f"✓ CUDA available - {torch.cuda.get_device_name(0)}")
        else:
            print("⚠ CUDA not available")
        
        # Check MPS (Apple Silicon)
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("✓ MPS (Apple Silicon) available")
        else:
            print("⚠ MPS not available")
        
    except ImportError:
        print("⚠ PyTorch not installed, cannot check devices")


def main():
    print("="*60)
    print("PDF Retrieval Experiment - Setup Test")
    print("="*60)
    print()
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_poppler(),
        check_pdfs()
    ]
    
    check_device()
    
    print()
    print("="*60)
    
    if all(checks):
        print("✓ All checks passed!")
        print()
        print("Ready to run experiments:")
        print("  Quick demo:  python simple_demo.py --max-pages 3")
        print("  Full experiment: ./run_experiment.sh colpali mps 5")
    else:
        print("✗ Some checks failed")
        print()
        print("Please install missing dependencies:")
        print("  pip install -r requirements.txt")
    
    print("="*60)


if __name__ == "__main__":
    main()
