from enhanced_retriever import EnhancedRetriever
from enhanced_knowledge_graph import EnhancedKnowledgeGraph
from feedback_analyzer import FeedbackAnalyzer
from typing import List, Dict

class EnhancedPromptBuilder:
    """Enhanced prompt builder with all advanced features integrated"""
    
    def __init__(self):
        self.retriever = EnhancedRetriever()
        self.knowledge_graph = EnhancedKnowledgeGraph()
        self.feedback_analyzer = FeedbackAnalyzer()
        
    def build_adaptive_prompt(self, ad_text: str, tone: str, platforms: List[str]) -> str:
        """Build an adaptive prompt using all enhancement layers"""
        
        # 1. Get enhanced RAG results with relevance scores
        rag_results = self.retriever.retrieve_with_relevance(tone, platforms)
        formatted_guidance = self.retriever.format_guidance_with_scores(rag_results)
        
        # 2. Get knowledge graph insights with traversal
        kg_insights = []
        
        # Get recommendations for each platform
        for platform in platforms:
            recommendations = self.knowledge_graph.get_recommendations(tone, platform)
            kg_insights.append(f"\n{platform} Insights:")
            kg_insights.append(f"  - Compatibility Score: {recommendations['compatibility_score']:.2f}")
            
            if recommendations['suggested_elements']:
                kg_insights.append("  - Suggestions: " + ", ".join(recommendations['suggested_elements']))
            
            if recommendations['warnings']:
                kg_insights.append("  - ⚠️ Warnings: " + ", ".join(recommendations['warnings']))
                
            if recommendations['creative_types']:
                kg_insights.append("  - Recommended Creative Types: " + ", ".join(recommendations['creative_types']))
            
            # Add relationship explanations
            relationship = self.knowledge_graph.explain_relationship(tone, platform)
            kg_insights.append(f"  - Relationship: {relationship}")
        
        kg_insights_str = "\n".join(kg_insights)
        
        # 3. Get adaptive weights from feedback analysis
        weights = self.feedback_analyzer.get_adaptive_weights()
        
        # 4. Add performance insights if available
        analysis = self.feedback_analyzer.analyze_patterns()
        performance_notes = []
        
        if analysis.get("recommendations"):
            relevant_recs = [rec for rec in analysis["recommendations"] 
                           if any(p.lower() in rec.lower() for p in platforms) or tone.lower() in rec.lower()]
            if relevant_recs:
                performance_notes.append("\nHistorical Performance Notes:")
                performance_notes.extend([f"  - {rec}" for rec in relevant_recs[:3]])
        
        performance_str = "\n".join(performance_notes) if performance_notes else ""
        
        # 5. Build the enhanced prompt
        platform_str = ", ".join(platforms)
        
        # Apply adaptive weights to emphasize better-performing combinations
        weight_notes = []
        for platform in platforms:
            combo_key = f"{tone}_{platform}"
            weight = weights.get(combo_key, 1.0)
            if weight > 0.8:
                weight_notes.append(f"  - {platform}: High confidence (historical success)")
            elif weight < 0.6:
                weight_notes.append(f"  - {platform}: Needs improvement (based on feedback)")
        
        weight_str = "\n".join(weight_notes) if weight_notes else ""
        
        prompt = f"""
You are an expert ad copywriter with access to advanced AI assistance.

TASK: Rewrite the following ad text in a {tone} tone and optimize it individually for: {platform_str}

ORIGINAL AD TEXT: "{ad_text}"

=== ENHANCED GUIDANCE (with Relevance Scores) ===
{formatted_guidance}

=== KNOWLEDGE GRAPH INSIGHTS ===
{kg_insights_str}

=== ADAPTIVE LEARNING INSIGHTS ===
{weight_str}
{performance_str}

=== INSTRUCTIONS ===
1. Maintain the core message and key information from the original ad
2. Adapt the tone and style according to the guidelines above
3. Consider the compatibility scores and warnings for each platform
4. Use suggested elements where appropriate
5. Avoid any warned elements or approaches
6. Apply lessons from historical performance data

OUTPUT FORMAT:
Provide a separate, optimized version for each platform:

{''.join([f'{p}:\n<Your rewritten ad text here>\n\n' for p in platforms])}

Remember: Each platform version should be uniquely tailored while maintaining brand consistency.
"""
        
        return prompt
    
    def get_improvement_suggestions(self) -> List[str]:
        """Get suggestions for improving the system based on feedback"""
        analysis = self.feedback_analyzer.analyze_patterns()
        suggestions = []
        
        # Check overall performance
        avg_rating = analysis.get("average_rating", 0)
        if avg_rating < 3.5:
            suggestions.append("Consider updating tone guidelines based on feedback patterns")
            
        # Check for problematic combinations
        for pattern in analysis.get("low_performing_patterns", []):
            tone, platform = pattern["pattern"].split("_")
            suggestions.append(f"Review and update guidelines for {tone} tone on {platform}")
            
        # Suggest new relationships for KG
        high_performers = analysis.get("high_performing_patterns", [])
        if high_performers:
            suggestions.append("Consider strengthening KG relationships for high-performing combinations")
            
        return suggestions 