from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict
import re

class EnhancedRetriever:
    """Enhanced RAG with semantic similarity scoring"""
    
    def __init__(self, guideline_path: str = "tone_guidelines.txt"):
        self.guideline_path = guideline_path
        self.guidelines = self._load_guidelines()
        self.embeddings_cache = {}
        
    def _load_guidelines(self) -> Dict[str, List[str]]:
        """Load guidelines from file"""
        guidelines = defaultdict(list)
        current_key = None
        
        with open(self.guideline_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    current_key = line.replace(":", "").strip().lower()
                elif current_key:
                    guidelines[current_key].append(line.strip("- ").strip())
        
        return dict(guidelines)
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """Create simple word-based embeddings for semantic similarity"""
        # Normalize text
        text = text.lower()
        
        # Extract key features
        features = {
            'length': len(text.split()),
            'has_emoji': int(bool(re.search(r'[😀-🙏]', text))),
            'has_exclamation': int('!' in text),
            'formal_words': sum(1 for word in ['professional', 'value', 'benefits', 'business'] if word in text),
            'casual_words': sum(1 for word in ['fun', 'playful', 'emoji', 'snappy'] if word in text),
            'cta_presence': int(any(word in text for word in ['cta', 'button', 'click'])),
            'hashtag_mention': int('#' in text or 'hashtag' in text),
        }
        
        # Convert to vector
        return np.array(list(features.values()), dtype=np.float32)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Tuple[str, str, float]]:
        """Perform semantic search across all guidelines"""
        query_embedding = self._simple_embedding(query)
        results = []
        
        for category, items in self.guidelines.items():
            for item in items:
                item_embedding = self._simple_embedding(item)
                similarity = self._cosine_similarity(query_embedding, item_embedding)
                results.append((category, item, similarity))
        
        # Sort by similarity score
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:top_k]
    
    def retrieve_with_relevance(self, tone: str, platforms: List[str]) -> Dict[str, any]:
        """Enhanced retrieval with relevance scoring"""
        context_query = f"{tone} tone for {' '.join(platforms)} platforms"
        semantic_results = self.semantic_search(context_query)
        
        # Structure the response with relevance scores
        response = {
            "direct_matches": {},
            "semantic_matches": [],
            "relevance_scores": {}
        }
        
        # Direct matches (existing logic)
        tone_lower = tone.lower()
        if tone_lower in self.guidelines:
            response["direct_matches"][tone] = self.guidelines[tone_lower]
            response["relevance_scores"][tone] = 1.0
        
        for platform in platforms:
            p_lower = platform.lower()
            if p_lower in self.guidelines:
                response["direct_matches"][platform] = self.guidelines[p_lower]
                response["relevance_scores"][platform] = 1.0
        
        # Add semantic matches
        for category, item, score in semantic_results:
            if category not in response["direct_matches"]:
                response["semantic_matches"].append({
                    "category": category,
                    "guideline": item,
                    "relevance": score
                })
        
        return response
    
    def format_guidance_with_scores(self, retrieval_result: Dict) -> str:
        """Format retrieval results with relevance scores"""
        output = []
        
        # Direct matches
        for key, guidelines in retrieval_result["direct_matches"].items():
            score = retrieval_result["relevance_scores"].get(key, 0)
            output.append(f"\n{key} Guidelines (Relevance: {score:.2f}):")
            for guideline in guidelines:
                output.append(f"  - {guideline}")
        
        # Semantic matches
        if retrieval_result["semantic_matches"]:
            output.append("\nAdditional Relevant Guidelines:")
            for match in retrieval_result["semantic_matches"][:3]:  # Top 3
                output.append(f"  - [{match['category']}] {match['guideline']} (Score: {match['relevance']:.2f})")
        
        return "\n".join(output) 