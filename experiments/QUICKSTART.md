# Quick Start Guide - PDF Retrieval Experiment

## 快速开始指南

这个实验演示了如何使用 Qdrant 的方法进行大规模 PDF 检索。

## Step 1: Install System Dependencies

### macOS (推荐用于此项目)

```bash
# Install poppler for PDF processing
brew install poppler
```

### Linux

```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

## Step 2: Install Python Dependencies

```bash
cd experiments

# Install dependencies
pip install -r requirements.txt
```

**注意**: 
- 首次运行会下载 ColPali/ColQwen 模型 (~2GB)
- 需要足够的磁盘空间和内存

## Step 3: Run Quick Demo (无需大模型)

先运行简化版本测试环境:

```bash
python simple_demo.py --pdf-folder ../dataset/books-pdf --max-pages 3
```

这个演示:
- ✅ 不需要下载大模型
- ✅ 快速验证环境配置
- ✅ 展示两阶段检索概念
- ⚠️ 使用简单特征而非 VLLM

## Step 4: Run Full Experiment (使用 ColPali/ColQwen)

### Option A: Quick Test (推荐首次运行)

只处理每个 PDF 的前 5 页:

```bash
# Make script executable
chmod +x run_experiment.sh

# Run with ColPali
./run_experiment.sh colpali mps 5

# Or with ColQwen
./run_experiment.sh colqwen mps 5
```

### Option B: Full Processing

处理所有页面:

```bash
python pdf_retrieval_experiment.py \
    --model colpali \
    --device mps \
    --pdf-folder ../dataset/books-pdf \
    --max-pages 999
```

### Device Options

- `mps` - Apple Silicon GPU (M1/M2/M3) ⚡ 最快
- `cuda:0` - NVIDIA GPU ⚡ 最快 (Linux/Windows)
- `cpu` - CPU only 🐌 慢

## Expected Output

```
==============================================================
PDF RETRIEVAL EXPERIMENT - COLPALI
==============================================================

Creating collection: pdf_retrieval_colpali
Found 7 PDF files

Processing: 普通高中教科书 数学  必修 第一册.pdf
Converted 5 pages
Generating embeddings for 5 images...
Indexed 5 pages in 23.45 seconds

==============================================================
RUNNING TEST QUERIES
==============================================================

Searching for: '集合的定义和性质'
Top results:
  1. Page 5 from 普通高中教科书 数学  必修 第一册.pdf (Score: 0.8745)
  2. Page 3 from 普通高中教科书 数学  必修 第一册.pdf (Score: 0.8234)
  3. Page 6 from 普通高中教科书 数学  必修 第一册.pdf (Score: 0.7891)
```

## Understanding the Results

实验会生成结果文件:

```
output/
├── pdf_retrieval_results_colpali_20231206_143022.json
└── demo_results_20231206_142015.json
```

### Metrics to Watch

1. **Indexing Speed**
   - 优化前: ~10-15 秒/页
   - 优化后: ~2-3 秒/页 (使用 mean pooling)
   - 🎯 目标: 10x 加速

2. **Retrieval Quality**
   - 第一阶段 (mean-pooled): 快速筛选
   - 第二阶段 (original): 精确重排
   - 🎯 目标: 接近原始模型质量

3. **Memory Usage**
   - Original vectors: ~1000 vectors/page
   - Pooled vectors: ~32 vectors/page
   - 🎯 节省: ~30x 压缩

## Troubleshooting

### Error: "Model download failed"

```bash
# Set HuggingFace mirror (China users)
export HF_ENDPOINT=https://hf-mirror.com
python pdf_retrieval_experiment.py ...
```

### Error: "CUDA out of memory"

减小 batch size:

```python
experiment.index_pdf(pdf_path, max_pages=10, batch_size=1)
```

### Error: "poppler not found"

```bash
# macOS
brew install poppler

# Verify installation
pdftoppm -h
```

### Error: "MPS backend not available"

使用 CPU:

```bash
./run_experiment.sh colpali cpu 5
```

## Next Steps

### 1. Customize Search Queries

编辑 `pdf_retrieval_experiment.py` 的测试查询:

```python
test_queries = [
    "你的搜索查询 1",
    "你的搜索查询 2",
    # 添加更多...
]
```

### 2. Use Your Own PDFs

```bash
python pdf_retrieval_experiment.py \
    --model colpali \
    --device mps \
    --pdf-folder /path/to/your/pdfs \
    --max-pages 50
```

### 3. Deploy to Production

使用 Qdrant Cloud:

```python
experiment = PDFRetrievalExperiment(
    model_name="colpali",
    qdrant_url="https://your-cluster.qdrant.io",
    qdrant_api_key="your-api-key",
    use_local_qdrant=False
)
```

### 4. Compare Models

运行两个模型并比较:

```bash
# ColPali
./run_experiment.sh colpali mps 10

# ColQwen
./run_experiment.sh colqwen mps 10

# Compare results in output/ folder
```

## Key Concepts from Qdrant Tutorial

### Why Mean Pooling?

**Problem**: 
- ColPali: 1,024 vectors/page × 100 (ef_construct) = 102M comparisons
- Too slow for large-scale indexing!

**Solution**:
- Mean pool by rows: 1,024 → 32 vectors
- 32 vectors × 100 = 3.2M comparisons
- 🚀 **30x faster** indexing

### Two-Stage Retrieval

```
Query
  ↓
[Stage 1] Fast search with mean-pooled vectors (HNSW index)
  ↓
Top 100 candidates
  ↓
[Stage 2] Rerank with original multivectors
  ↓
Top 5 results
```

## Performance Comparison

| Method | Vectors/Page | Index Speed | Retrieval Quality |
|--------|--------------|-------------|-------------------|
| Original | 1,024 | 1x (slow) | 100% |
| Mean-pooled rows | 32 | 10x | ~98% |
| Mean-pooled cols | 32 | 10x | ~98% |
| Two-stage | Both | 10x + rerank | ~99.5% |

## References

- [Qdrant Tutorial](https://qdrant.tech/documentation/advanced-tutorials/pdf-retrieval-at-scale/)
- [ColPali Paper](https://arxiv.org/abs/2407.01449)
- [Project README](README.md)

## Questions?

Check the [main README](README.md) for detailed documentation.

Happy experimenting! 🚀
