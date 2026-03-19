# PDF Retrieval at Scale Experiment

This experiment implements the PDF retrieval methodology from Qdrant's documentation using Vision LLMs (ColPali/ColQwen) with mean pooling optimization.

## Overview

The experiment demonstrates:
1. **First-stage retrieval**: Fast search using mean-pooled vectors (rows/columns)
2. **Second-stage reranking**: Precision refinement using original multivectors
3. **Performance comparison**: Indexing speed and retrieval quality

## Methodology

Based on: https://qdrant.tech/documentation/advanced-tutorials/pdf-retrieval-at-scale/

### Key Optimizations

**Problem**: VLLMs generate 700-1000+ vectors per PDF page, making indexing extremely slow.

**Solution**: 
- Apply mean pooling by rows/columns to reduce vectors (e.g., 1024 → 32)
- Use pooled vectors for fast first-stage retrieval via HNSW index
- Rerank top results using original multivectors for precision

### Benefits
- **10x faster** indexing time
- **Comparable** retrieval quality to original model
- **Scalable** to large document collections

## Installation

### 1. System Dependencies

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

### 2. Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Experiment

Run on the Chinese math textbooks:

```bash
python pdf_retrieval_experiment.py \
    --model colpali \
    --device mps \
    --pdf-folder dataset/books-pdf \
    --max-pages 10
```

### Parameters

- `--model`: Choose `colpali` or `colqwen` (default: colpali)
- `--device`: Device for model inference
  - `mps` - Apple Silicon GPU
  - `cuda:0` - NVIDIA GPU
  - `cpu` - CPU (slowest)
- `--pdf-folder`: Path to folder containing PDFs
- `--max-pages`: Max pages to process per PDF (for testing)

### Full Experiment

Process all pages from all PDFs:

```bash
python pdf_retrieval_experiment.py \
    --model colpali \
    --device mps \
    --pdf-folder dataset/books-pdf \
    --max-pages 999
```

## Example Output

```
==============================================================
PDF RETRIEVAL EXPERIMENT - COLPALI
==============================================================

Creating collection: pdf_retrieval_colpali
Collection created successfully!

Found 7 PDF files

Processing: 普通高中教科书 数学  必修 第一册.pdf
Converting PDF to images: dataset/books-pdf/普通高中教科书 数学  必修 第一册.pdf
Converted 10 pages
Generating embeddings for 10 images...
Processing batch 1/5
Processing batch 2/5
...
Indexed 10 pages in 45.32 seconds
Average time per page: 4.53s

==============================================================
RUNNING TEST QUERIES
==============================================================

Searching for: '集合的定义和性质'
Search completed in 0.15 seconds

Top results for '集合的定义和性质':
  1. Page 5 from 普通高中教科书 数学  必修 第一册.pdf
     Score: 0.8745
  2. Page 3 from 普通高中教科书 数学  必修 第一册.pdf
     Score: 0.8234
  3. Page 6 from 普通高中教科书 数学  必修 第一册.pdf
     Score: 0.7891
```

## Architecture

### PDFRetrievalExperiment Class

Main components:

1. **Model Loading**: Initialize ColPali or ColQwen2
2. **Collection Creation**: Setup Qdrant with multivector configuration
3. **PDF Processing**: Convert pages to images
4. **Embedding Generation**: Create original + mean-pooled vectors
5. **Indexing**: Upload to Qdrant with metadata
6. **Search**: Two-stage retrieval with optional reranking

### Vector Storage

Each PDF page is stored with 3 vector representations:

- `original`: Full multivector embedding (HNSW disabled)
- `mean_pooling_rows`: Mean pooled by row patches
- `mean_pooling_columns`: Mean pooled by column patches

## Performance Metrics

The experiment tracks:

- **Indexing time**: Total and per-page
- **Vector counts**: Original vs pooled
- **Search latency**: First-stage retrieval speed
- **Memory usage**: Collection size

Results are saved to `output/pdf_retrieval_results_<model>_<timestamp>.json`

## Test Queries

Default queries for Chinese math textbooks:

1. 集合的定义和性质 (Sets definition and properties)
2. 一元二次不等式的解法 (Solving quadratic inequalities)
3. 指数函数的性质 (Properties of exponential functions)
4. 对数函数的图像 (Logarithmic function graphs)
5. 函数的单调性 (Function monotonicity)

## Advanced Usage

### Custom Search

```python
from pdf_retrieval_experiment import PDFRetrievalExperiment

experiment = PDFRetrievalExperiment(
    model_name="colpali",
    device="mps",
    use_local_qdrant=True
)

# Index PDFs
experiment.create_collection()
experiment.index_pdf("path/to/document.pdf", max_pages=50)

# Search
results = experiment.search(
    query="your search query",
    top_k=5,
    pooling_method="rows",  # or "columns"
    use_reranking=True
)

for result in results:
    print(f"Page {result['page_number']}: {result['score']}")
```

### Production Deployment

For production use with Qdrant Cloud:

```python
experiment = PDFRetrievalExperiment(
    model_name="colpali",
    device="cuda:0",
    qdrant_url="https://your-cluster.qdrant.io",
    qdrant_api_key="your-api-key",
    use_local_qdrant=False
)
```

## Troubleshooting

### Out of Memory

Reduce batch size:
```python
experiment.index_pdf(pdf_path, max_pages=10, batch_size=1)
```

### Slow on CPU

Use Apple Silicon GPU or NVIDIA GPU:
```bash
--device mps  # Apple Silicon
--device cuda:0  # NVIDIA GPU
```

### PDF Conversion Errors

Ensure poppler is installed:
```bash
# macOS
brew install poppler

# Linux
sudo apt-get install poppler-utils
```

## References

- [Qdrant PDF Retrieval Tutorial](https://qdrant.tech/documentation/advanced-tutorials/pdf-retrieval-at-scale/)
- [ColPali Paper](https://arxiv.org/abs/2407.01449)
- [ColQwen Model](https://huggingface.co/vidore/colqwen2-v0.1)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

## License

This experiment code follows the Agno project license.
