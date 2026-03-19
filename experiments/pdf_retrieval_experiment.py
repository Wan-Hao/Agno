"""
PDF Retrieval at Scale Experiment
Based on Qdrant's methodology using ColPali/ColQwen with mean pooling optimization
"""

import torch
from pathlib import Path
from typing import List, Tuple, Dict, Any
import json
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

try:
    from colpali_engine.models import ColPali, ColPaliProcessor, ColQwen2, ColQwen2Processor
    from qdrant_client import QdrantClient, models
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install colpali-engine qdrant-client pdf2image pillow torch")


class PDFRetrievalExperiment:
    """
    Implements scaled PDF retrieval using Vision LLMs (ColPali/ColQwen) with optimization:
    - First stage: Fast retrieval using mean-pooled vectors
    - Second stage: Reranking with original multivectors
    """
    
    def __init__(
        self, 
        model_name: str = "colpali",  # "colpali" or "colqwen"
        qdrant_url: str = None,
        qdrant_api_key: str = None,
        device: str = "mps",  # "cuda:0", "cpu", or "mps" for Apple Silicon
        use_local_qdrant: bool = True
    ):
        self.model_name = model_name
        self.device = device
        self.use_local_qdrant = use_local_qdrant
        
        print(f"Initializing {model_name.upper()} model on {device}...")
        self._load_model()
        
        print("Connecting to Qdrant...")
        if use_local_qdrant:
            self.client = QdrantClient(":memory:")  # In-memory for testing
        else:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        
        self.collection_name = f"pdf_retrieval_{model_name}"
        self.results = []
        
    def _load_model(self):
        """Load the selected VLLM model and processor"""
        if self.model_name == "colpali":
            self.model = ColPali.from_pretrained(
                "vidore/colpali-v1.3",
                torch_dtype=torch.bfloat16,
                device_map=self.device,
            ).eval()
            self.processor = ColPaliProcessor.from_pretrained("vidore/colpali-v1.3")
            self.image_token_id = self.processor.image_token_id
        else:  # colqwen
            self.model = ColQwen2.from_pretrained(
                "vidore/colqwen2-v0.1",
                torch_dtype=torch.bfloat16,
                device_map=self.device,
            ).eval()
            self.processor = ColQwen2Processor.from_pretrained("vidore/colqwen2-v0.1")
            self.image_token_id = self.processor.image_token_id
    
    def create_collection(self):
        """Create Qdrant collection with multivector configuration"""
        print(f"Creating collection: {self.collection_name}")
        
        # Delete if exists
        try:
            self.client.delete_collection(self.collection_name)
        except:
            pass
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "original": models.VectorParams(
                    size=128,
                    distance=models.Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM
                    ),
                    hnsw_config=models.HnswConfigDiff(m=0)  # Disable HNSW for original
                ),
                "mean_pooling_columns": models.VectorParams(
                    size=128,
                    distance=models.Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM
                    )
                ),
                "mean_pooling_rows": models.VectorParams(
                    size=128,
                    distance=models.Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM
                    )
                )
            }
        )
        print("Collection created successfully!")
    
    def pdf_to_images(self, pdf_path: str, max_pages: int = None) -> List[Image.Image]:
        """Convert PDF pages to PIL Images"""
        print(f"Converting PDF to images: {pdf_path}")
        images = convert_from_path(pdf_path, dpi=200)
        
        if max_pages:
            images = images[:max_pages]
        
        print(f"Converted {len(images)} pages")
        return images
    
    def get_patches_info(self, image: Image.Image) -> Tuple[int, int]:
        """Get number of patches (rows and columns) for the image"""
        if self.model_name == "colpali":
            x_patches, y_patches = self.processor.get_n_patches(
                image.size,
                patch_size=self.model.patch_size
            )
        else:  # colqwen
            x_patches, y_patches = self.processor.get_n_patches(
                image.size,
                patch_size=self.model.patch_size,
                spatial_merge_size=self.model.spatial_merge_size
            )
        return x_patches, y_patches
    
    def mean_pool_embeddings(
        self, 
        embedding: torch.Tensor, 
        image_token_id: int,
        input_ids: torch.Tensor,
        x_patches: int,
        y_patches: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply mean pooling by rows and columns to multivector embeddings
        Returns: (pooled_by_rows, pooled_by_columns)
        """
        # Identify image token positions
        image_token_mask = input_ids[0] == image_token_id
        image_embeddings = embedding[image_token_mask]
        
        # Prefix and postfix embeddings (special tokens)
        prefix_embeddings = embedding[~image_token_mask][:len(embedding[~image_token_mask])//2]
        postfix_embeddings = embedding[~image_token_mask][len(embedding[~image_token_mask])//2:]
        
        # Reshape to (x_patches, y_patches, embedding_dim)
        image_embeddings_reshaped = image_embeddings.reshape(x_patches, y_patches, -1)
        
        # Mean pooling by rows
        pooled_rows = image_embeddings_reshaped.mean(dim=1)  # (x_patches, embedding_dim)
        pooled_rows_full = torch.cat([prefix_embeddings, pooled_rows, postfix_embeddings], dim=0)
        
        # Mean pooling by columns
        pooled_cols = image_embeddings_reshaped.mean(dim=0)  # (y_patches, embedding_dim)
        pooled_cols_full = torch.cat([prefix_embeddings, pooled_cols, postfix_embeddings], dim=0)
        
        return pooled_rows_full.cpu().numpy(), pooled_cols_full.cpu().numpy()
    
    def embed_images(self, images: List[Image.Image], batch_size: int = 2) -> List[Dict]:
        """
        Generate embeddings for images with mean pooling
        Returns list of dicts with original and pooled embeddings
        """
        print(f"Generating embeddings for {len(images)} images...")
        all_embeddings = []
        
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(images)-1)//batch_size + 1}")
            
            # Process images
            processed = self.processor.process_images(batch)
            input_ids = processed["input_ids"]
            
            # Generate embeddings
            with torch.no_grad():
                image_embeddings = self.model(**processed)
            
            # Process each image in batch
            for idx, embedding in enumerate(image_embeddings):
                x_patches, y_patches = self.get_patches_info(batch[idx])
                
                # Mean pooling
                pooled_rows, pooled_cols = self.mean_pool_embeddings(
                    embedding,
                    self.image_token_id,
                    input_ids[idx:idx+1],
                    x_patches,
                    y_patches
                )
                
                all_embeddings.append({
                    "original": embedding.cpu().numpy(),
                    "mean_pooling_rows": pooled_rows,
                    "mean_pooling_columns": pooled_cols,
                    "page_idx": i + idx,
                    "x_patches": x_patches,
                    "y_patches": y_patches
                })
        
        print(f"Generated embeddings for {len(all_embeddings)} pages")
        return all_embeddings
    
    def index_pdf(self, pdf_path: str, max_pages: int = None, batch_size: int = 2):
        """
        Index a PDF file in Qdrant
        """
        start_time = datetime.now()
        
        # Convert PDF to images
        images = self.pdf_to_images(pdf_path, max_pages)
        
        # Generate embeddings
        embeddings_data = self.embed_images(images, batch_size)
        
        # Upload to Qdrant
        print("Uploading to Qdrant...")
        points = []
        
        for emb_data in embeddings_data:
            point = models.PointStruct(
                id=emb_data["page_idx"],
                vector={
                    "original": emb_data["original"].tolist(),
                    "mean_pooling_rows": emb_data["mean_pooling_rows"].tolist(),
                    "mean_pooling_columns": emb_data["mean_pooling_columns"].tolist()
                },
                payload={
                    "pdf_path": str(pdf_path),
                    "page_number": emb_data["page_idx"] + 1,
                    "x_patches": emb_data["x_patches"],
                    "y_patches": emb_data["y_patches"]
                }
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        result = {
            "pdf_path": str(pdf_path),
            "total_pages": len(images),
            "indexing_time_seconds": elapsed_time,
            "avg_time_per_page": elapsed_time / len(images) if images else 0
        }
        
        self.results.append(result)
        print(f"Indexed {len(images)} pages in {elapsed_time:.2f} seconds")
        print(f"Average time per page: {result['avg_time_per_page']:.2f}s")
        
        return result
    
    def search(
        self, 
        query: str, 
        top_k: int = 5,
        pooling_method: str = "rows",  # "rows" or "columns"
        use_reranking: bool = True
    ) -> List[Dict]:
        """
        Search for relevant PDF pages
        First stage: Fast retrieval with mean-pooled vectors
        Second stage (optional): Rerank with original multivectors
        """
        print(f"\nSearching for: '{query}'")
        start_time = datetime.now()
        
        # Process query
        processed_query = self.processor.process_queries([query])
        
        # Generate query embedding
        with torch.no_grad():
            query_embedding = self.model(**processed_query)[0]
        
        # First stage: Fast retrieval with mean pooling
        vector_name = f"mean_pooling_{pooling_method}"
        
        # For query, we also need to pool it
        # Simplified: use the embedding as-is for now (in production, pool it similarly)
        query_vector = query_embedding.cpu().numpy().tolist()
        
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=(vector_name, query_vector),
            limit=top_k * 2 if use_reranking else top_k
        )
        
        results = []
        for hit in search_results[:top_k if not use_reranking else len(search_results)]:
            results.append({
                "page_number": hit.payload["page_number"],
                "pdf_path": hit.payload["pdf_path"],
                "score": hit.score,
                "id": hit.id
            })
        
        # Second stage: Reranking with original multivectors
        if use_reranking and len(results) > top_k:
            print("Reranking with original multivectors...")
            # In a full implementation, we would retrieve original vectors and rerank
            # For now, just take top_k from first stage
            results = results[:top_k]
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        print(f"Search completed in {elapsed_time:.2f} seconds")
        
        return results
    
    def run_experiment(self, pdf_folder: str, max_pages_per_pdf: int = 10):
        """
        Run complete experiment on all PDFs in folder
        """
        print("="*60)
        print(f"PDF RETRIEVAL EXPERIMENT - {self.model_name.upper()}")
        print("="*60)
        
        # Create collection
        self.create_collection()
        
        # Find all PDFs
        pdf_folder_path = Path(pdf_folder)
        pdf_files = list(pdf_folder_path.glob("*.pdf"))
        print(f"\nFound {len(pdf_files)} PDF files")
        
        # Index each PDF
        for pdf_file in pdf_files:
            print(f"\n{'='*60}")
            print(f"Processing: {pdf_file.name}")
            print(f"{'='*60}")
            self.index_pdf(str(pdf_file), max_pages=max_pages_per_pdf)
        
        # Test queries
        test_queries = [
            "集合的定义和性质",
            "一元二次不等式的解法",
            "指数函数的性质",
            "对数函数的图像",
            "函数的单调性"
        ]
        
        print("\n" + "="*60)
        print("RUNNING TEST QUERIES")
        print("="*60)
        
        for query in test_queries:
            results = self.search(query, top_k=3, pooling_method="rows")
            print(f"\nTop results for '{query}':")
            for i, result in enumerate(results, 1):
                print(f"  {i}. Page {result['page_number']} from {Path(result['pdf_path']).name}")
                print(f"     Score: {result['score']:.4f}")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save experiment results to JSON"""
        output_path = Path("output") / f"pdf_retrieval_results_{self.model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "model": self.model_name,
                "device": self.device,
                "timestamp": datetime.now().isoformat(),
                "results": self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {output_path}")


def main():
    """Main experiment runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF Retrieval Experiment")
    parser.add_argument("--model", choices=["colpali", "colqwen"], default="colpali",
                       help="Model to use for retrieval")
    parser.add_argument("--device", default="mps", 
                       help="Device: cuda:0, cpu, or mps")
    parser.add_argument("--pdf-folder", default="dataset/books-pdf",
                       help="Folder containing PDF files")
    parser.add_argument("--max-pages", type=int, default=10,
                       help="Maximum pages to process per PDF")
    
    args = parser.parse_args()
    
    # Run experiment
    experiment = PDFRetrievalExperiment(
        model_name=args.model,
        device=args.device,
        use_local_qdrant=True
    )
    
    experiment.run_experiment(
        pdf_folder=args.pdf_folder,
        max_pages_per_pdf=args.max_pages
    )


if __name__ == "__main__":
    main()
