"""
Semantic Processor for Knowledge Graph Nodes

Features:
1. Generate embeddings for all nodes using OpenAI/Gemini API
2. Calculate cross-domain similarity matrix
3. Intelligent sampling based on semantic similarity
"""
from typing import List, Dict, Any, Tuple
import json
import numpy as np
from pathlib import Path
import os
from openai import OpenAI
from core.gemini_client import get_gemini_client
import pickle


class SemanticProcessor:
    """Process semantic embeddings and similarity for knowledge graph nodes"""
    
    def __init__(self, use_gemini: bool = True, cache_dir: str = "output/embeddings"):
        """
        Initialize semantic processor
        
        Args:
            use_gemini: Use Gemini API if True, otherwise OpenAI
            cache_dir: Directory to cache embeddings
        """
        self.use_gemini = use_gemini
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize client
        if use_gemini:
            self.client = get_gemini_client()
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        print(f"✓ SemanticProcessor initialized ({'Gemini' if use_gemini else 'OpenAI'})")
    
    def _get_node_text(self, node: Dict[str, Any]) -> str:
        """
        Extract meaningful text from a node for embedding
        
        Args:
            node: Knowledge graph node
            
        Returns:
            Concatenated text representation
        """
        parts = []
        
        # Add label
        if 'label' in node:
            parts.append(f"概念: {node['label']}")
        
        # Add description
        if 'properties' in node and 'description' in node['properties']:
            parts.append(f"描述: {node['properties']['description']}")
        
        # Add category/theme
        if 'properties' in node:
            props = node['properties']
            if 'category' in props:
                parts.append(f"分类: {props['category']}")
            if 'theme' in props:
                parts.append(f"主题: {props['theme']}")
            if 'cultivated_abilities' in props:
                abilities = ', '.join(props['cultivated_abilities'])
                parts.append(f"培养能力: {abilities}")
        
        return "\n".join(parts)
    
    def _get_embedding_openai(self, text: str) -> List[float]:
        """Get embedding using OpenAI API"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def _get_embedding_gemini(self, text: str) -> List[float]:
        """Get embedding using Gemini API"""
        result = self.client.embed_content(
            model="models/text-embedding-004",
            content=text
        )
        return result['embedding']
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text"""
        if self.use_gemini:
            return self._get_embedding_gemini(text)
        else:
            return self._get_embedding_openai(text)
    
    def generate_node_embeddings(
        self,
        graph: Dict[str, Any],
        domain: str,
        force_regenerate: bool = False
    ) -> Dict[str, List[float]]:
        """
        Generate embeddings for all nodes in a knowledge graph
        
        Args:
            graph: Knowledge graph with nodes
            domain: Domain name (e.g., 'physics', 'math')
            force_regenerate: Force regeneration even if cache exists
            
        Returns:
            Dictionary mapping node_id to embedding vector
        """
        cache_file = self.cache_dir / f"{domain}_embeddings.pkl"
        
        # Load from cache if exists
        if cache_file.exists() and not force_regenerate:
            print(f"Loading {domain} embeddings from cache...")
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        print(f"Generating embeddings for {domain} nodes...")
        embeddings = {}
        nodes = graph.get('nodes', [])
        
        for i, node in enumerate(nodes):
            node_id = node['id']
            text = self._get_node_text(node)
            
            try:
                embedding = self.get_embedding(text)
                embeddings[node_id] = embedding
                
                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1}/{len(nodes)} nodes")
            
            except Exception as e:
                print(f"  ✗ Failed to get embedding for {node_id}: {e}")
                continue
        
        # Save to cache
        with open(cache_file, 'wb') as f:
            pickle.dump(embeddings, f)
        
        print(f"✓ Generated {len(embeddings)} embeddings for {domain}")
        return embeddings
    
    def calculate_similarity_matrix(
        self,
        physics_embeddings: Dict[str, List[float]],
        math_embeddings: Dict[str, List[float]],
        output_file: str = "output/similarity_matrix.npz"
    ) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Calculate cosine similarity matrix between physics and math nodes
        
        Args:
            physics_embeddings: Physics node embeddings
            math_embeddings: Math node embeddings
            output_file: File to save the matrix
            
        Returns:
            Tuple of (similarity_matrix, physics_node_ids, math_node_ids)
        """
        print("Calculating similarity matrix...")
        
        # Get sorted node IDs
        physics_ids = sorted(physics_embeddings.keys())
        math_ids = sorted(math_embeddings.keys())
        
        # Convert to numpy arrays
        physics_matrix = np.array([physics_embeddings[pid] for pid in physics_ids])
        math_matrix = np.array([math_embeddings[mid] for mid in math_ids])
        
        # Normalize vectors
        physics_norm = physics_matrix / np.linalg.norm(physics_matrix, axis=1, keepdims=True)
        math_norm = math_matrix / np.linalg.norm(math_matrix, axis=1, keepdims=True)
        
        # Calculate cosine similarity matrix
        similarity_matrix = np.dot(physics_norm, math_norm.T)
        
        # Save matrix
        np.savez_compressed(
            output_file,
            similarity=similarity_matrix,
            physics_ids=physics_ids,
            math_ids=math_ids
        )
        
        print(f"✓ Similarity matrix shape: {similarity_matrix.shape}")
        print(f"✓ Saved to: {output_file}")
        
        return similarity_matrix, physics_ids, math_ids
    
    def get_top_similar_pairs(
        self,
        similarity_matrix: np.ndarray,
        physics_ids: List[str],
        math_ids: List[str],
        top_k: int = 300,
        min_similarity: float = 0.3
    ) -> List[Tuple[str, str, float]]:
        """
        Get top K most similar node pairs based on semantic similarity
        
        Args:
            similarity_matrix: Precomputed similarity matrix
            physics_ids: List of physics node IDs
            math_ids: List of math node IDs
            top_k: Number of top pairs to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of (physics_id, math_id, similarity_score) tuples
        """
        print(f"Finding top {top_k} similar pairs (min_similarity={min_similarity})...")
        
        # Flatten matrix and get indices
        flat_indices = np.argsort(similarity_matrix.ravel())[::-1]
        
        pairs = []
        seen = set()
        
        for idx in flat_indices:
            if len(pairs) >= top_k:
                break
            
            # Convert flat index to 2D coordinates
            i = idx // similarity_matrix.shape[1]
            j = idx % similarity_matrix.shape[1]
            
            similarity = similarity_matrix[i, j]
            
            if similarity < min_similarity:
                break
            
            physics_id = physics_ids[i]
            math_id = math_ids[j]
            pair_key = (physics_id, math_id)
            
            if pair_key not in seen:
                pairs.append((physics_id, math_id, float(similarity)))
                seen.add(pair_key)
        
        print(f"✓ Found {len(pairs)} pairs with similarity >= {min_similarity}")
        return pairs
    
    def random_sample_pairs(
        self,
        physics_ids: List[str],
        math_ids: List[str],
        n_samples: int = 500,
        seed: int = 42
    ) -> List[Tuple[str, str]]:
        """
        Randomly sample node pairs
        
        Args:
            physics_ids: List of physics node IDs
            math_ids: List of math node IDs
            n_samples: Number of samples
            seed: Random seed
            
        Returns:
            List of (physics_id, math_id) tuples
        """
        np.random.seed(seed)
        
        # Generate all possible pairs
        all_pairs = [(p, m) for p in physics_ids for m in math_ids]
        
        # Random sample
        n_samples = min(n_samples, len(all_pairs))
        indices = np.random.choice(len(all_pairs), size=n_samples, replace=False)
        
        sampled_pairs = [all_pairs[i] for i in indices]
        
        print(f"✓ Randomly sampled {len(sampled_pairs)} pairs")
        return sampled_pairs
