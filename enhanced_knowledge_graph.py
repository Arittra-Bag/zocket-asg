from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque

class EnhancedKnowledgeGraph:
    """Enhanced Knowledge Graph with traversal capabilities"""
    
    def __init__(self):
        # Node properties
        self.nodes = {
            # Tones
            "fun": {
                "type": "tone",
                "properties": {
                    "formality": 0.2,
                    "energy": 0.9,
                    "creativity": 0.8
                }
            },
            "professional": {
                "type": "tone",
                "properties": {
                    "formality": 0.9,
                    "energy": 0.5,
                    "creativity": 0.3
                }
            },
            "semi-fun": {
                "type": "tone",
                "properties": {
                    "formality": 0.5,
                    "energy": 0.7,
                    "creativity": 0.6
                }
            },
            
            # Platforms
            "Meta": {
                "type": "platform",
                "properties": {
                    "char_limit": 2200,
                    "emoji_friendly": True,
                    "hashtag_friendly": True,
                    "visual_emphasis": 0.9
                }
            },
            "Google": {
                "type": "platform",
                "properties": {
                    "char_limit": 90,
                    "emoji_friendly": False,
                    "hashtag_friendly": False,
                    "visual_emphasis": 0.2
                }
            },
            "LinkedIn": {
                "type": "platform",
                "properties": {
                    "char_limit": 3000,
                    "emoji_friendly": False,
                    "hashtag_friendly": True,
                    "visual_emphasis": 0.4
                }
            },
            
            # Creative Types
            "awareness": {
                "type": "creative_type",
                "properties": {
                    "goal": "brand_visibility",
                    "cta_strength": 0.3
                }
            },
            "engagement": {
                "type": "creative_type",
                "properties": {
                    "goal": "interaction",
                    "cta_strength": 0.7
                }
            },
            "conversion": {
                "type": "creative_type",
                "properties": {
                    "goal": "sales",
                    "cta_strength": 1.0
                }
            }
        }
        
        # Edges (relationships)
        self.edges = defaultdict(list)
        self._build_relationships()
        
    def _build_relationships(self):
        """Build graph relationships"""
        # Tone -> Platform compatibility
        self.add_edge("fun", "Meta", "highly_compatible", weight=0.9)
        self.add_edge("fun", "LinkedIn", "moderately_compatible", weight=0.3)
        self.add_edge("fun", "Google", "poorly_compatible", weight=0.1)
        
        self.add_edge("professional", "LinkedIn", "highly_compatible", weight=0.95)
        self.add_edge("professional", "Google", "highly_compatible", weight=0.9)
        self.add_edge("professional", "Meta", "moderately_compatible", weight=0.5)
        
        self.add_edge("semi-fun", "Meta", "highly_compatible", weight=0.8)
        self.add_edge("semi-fun", "LinkedIn", "highly_compatible", weight=0.7)
        self.add_edge("semi-fun", "Google", "moderately_compatible", weight=0.5)
        
        # Tone -> Creative Type
        self.add_edge("fun", "awareness", "suitable_for", weight=0.9)
        self.add_edge("fun", "engagement", "suitable_for", weight=0.95)
        self.add_edge("professional", "conversion", "suitable_for", weight=0.9)
        self.add_edge("semi-fun", "engagement", "suitable_for", weight=0.8)
        
        # Platform -> Creative Type preferences
        self.add_edge("Meta", "engagement", "prefers", weight=0.9)
        self.add_edge("LinkedIn", "conversion", "prefers", weight=0.8)
        self.add_edge("Google", "conversion", "prefers", weight=0.95)
        
    def add_edge(self, from_node: str, to_node: str, relationship: str, weight: float = 1.0):
        """Add an edge to the graph"""
        self.edges[from_node].append({
            "to": to_node,
            "relationship": relationship,
            "weight": weight
        })
        
    def traverse_bfs(self, start_node: str, max_depth: int = 2) -> Dict[str, List[Tuple[str, str, float]]]:
        """Breadth-first traversal to find related nodes"""
        visited = set()
        queue = deque([(start_node, 0)])
        paths = defaultdict(list)
        
        while queue:
            current_node, depth = queue.popleft()
            
            if current_node in visited or depth > max_depth:
                continue
                
            visited.add(current_node)
            
            for edge in self.edges.get(current_node, []):
                to_node = edge["to"]
                relationship = edge["relationship"]
                weight = edge["weight"]
                
                paths[to_node].append((current_node, relationship, weight))
                
                if depth < max_depth:
                    queue.append((to_node, depth + 1))
                    
        return dict(paths)
        
    def find_best_path(self, start: str, end: str) -> Optional[List[Tuple[str, str, float]]]:
        """Find the best path between two nodes using weighted edges"""
        # Simple Dijkstra-like approach
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        previous = {}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            
            if distances[current] == float('inf'):
                break
                
            unvisited.remove(current)
            
            for edge in self.edges.get(current, []):
                neighbor = edge["to"]
                weight = 1 - edge["weight"]  # Convert to distance (lower is better)
                distance = distances[current] + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = (current, edge["relationship"], edge["weight"])
                    
        # Reconstruct path
        if end not in previous:
            return None
            
        path = []
        current = end
        while current != start:
            if current not in previous:
                return None
            prev_node, rel, weight = previous[current]
            path.append((prev_node, rel, weight))
            current = prev_node
            
        return list(reversed(path))
        
    def get_recommendations(self, tone: str, platform: str) -> Dict[str, any]:
        """Get recommendations based on tone and platform"""
        recommendations = {
            "compatibility_score": 0,
            "suggested_elements": [],
            "warnings": [],
            "creative_types": []
        }
        
        # Check direct compatibility
        for edge in self.edges.get(tone, []):
            if edge["to"] == platform:
                recommendations["compatibility_score"] = edge["weight"]
                break
                
        # Find related creative types
        tone_paths = self.traverse_bfs(tone, max_depth=1)
        platform_paths = self.traverse_bfs(platform, max_depth=1)
        
        # Extract creative type recommendations
        for node, paths in tone_paths.items():
            if self.nodes.get(node, {}).get("type") == "creative_type":
                for _, rel, weight in paths:
                    if rel == "suitable_for" and weight > 0.7:
                        recommendations["creative_types"].append(node)
                        
        # Platform-specific suggestions
        platform_props = self.nodes.get(platform, {}).get("properties", {})
        tone_props = self.nodes.get(tone, {}).get("properties", {})
        
        if platform_props.get("emoji_friendly") and tone_props.get("creativity", 0) > 0.7:
            recommendations["suggested_elements"].append("Use emojis to enhance engagement")
        elif not platform_props.get("emoji_friendly") and tone == "fun":
            recommendations["warnings"].append("Platform doesn't support emojis well - adjust tone")
            
        if platform_props.get("char_limit", float('inf')) < 100:
            recommendations["suggested_elements"].append("Keep message extremely concise")
            
        return recommendations
        
    def explain_relationship(self, node1: str, node2: str) -> str:
        """Explain the relationship between two nodes"""
        # Check direct connection first
        for edge in self.edges.get(node1, []):
            if edge["to"] == node2:
                return f"{node1} is {edge['relationship']} with {node2} (strength: {edge['weight']:.2f})"
        
        # If no direct connection, find path
        path = self.find_best_path(node1, node2)
        
        if not path:
            return f"No direct relationship found between {node1} and {node2}"
            
        explanation = []
        current = node1
        for prev_node, relationship, weight in path:
            # The path reconstruction gives us the path backwards, so we need to handle it correctly
            explanation.append(f"{prev_node} {relationship} {current} (strength: {weight:.2f})")
            current = prev_node
            
        return " → ".join(explanation) 