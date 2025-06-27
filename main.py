import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from enhanced_prompt_builder import EnhancedPromptBuilder
from feedback_analyzer import FeedbackAnalyzer
from google import generativeai as genai
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

# Set your Gemini API key here (or load via env var in production)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize enhanced components
enhanced_builder = EnhancedPromptBuilder()
feedback_analyzer = FeedbackAnalyzer()

class AdRequest(BaseModel):
    ad_text: str
    tone: str
    platforms: List[str]

class Feedback(BaseModel):
    ad_text: str
    tone: str
    platforms: List[str]
    rewritten_output: str
    rating: int  # 1 to 5

@app.post("/run-enhanced-agent")
def run_enhanced_agent(request: AdRequest):
    """Run the agent with enhanced RAG, KG traversal, and adaptive learning"""
    try:
        # Use enhanced prompt builder
        prompt = enhanced_builder.build_adaptive_prompt(
            request.ad_text, 
            request.tone, 
            request.platforms
        )
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Get improvement suggestions
        suggestions = enhanced_builder.get_improvement_suggestions()
        
        return {
            "rewritten_ads": response.text,
            "metadata": {
                "used_enhanced_features": True,
                "improvement_suggestions": suggestions[:3]  # Top 3 suggestions
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "ad_text": feedback.ad_text,
        "tone": feedback.tone,
        "platforms": feedback.platforms,
        "rewritten_output": feedback.rewritten_output,
        "rating": feedback.rating
    }

    try:
        with open("feedback_store.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
        return {"message": "Feedback submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing feedback: {str(e)}")

@app.get("/insights")
def get_insights():
    """Get insights from feedback analysis"""
    try:
        analysis = feedback_analyzer.analyze_patterns()
        trends = feedback_analyzer.get_time_based_trends()
        weights = feedback_analyzer.get_adaptive_weights()
        
        return {
            "analysis_summary": {
                "total_feedback": analysis.get("total_feedback", 0),
                "average_rating": round(analysis.get("average_rating", 0), 2),
                "recommendations": analysis.get("recommendations", [])[:5]
            },
            "performance_by_tone": analysis.get("tone_stats", {}),
            "performance_by_platform": analysis.get("platform_stats", {}),
            "winning_combinations": analysis.get("high_performing_patterns", []),
            "needs_improvement": analysis.get("low_performing_patterns", []),
            "adaptive_weights": weights,
            "recent_trends": trends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph-insights/{tone}/{platform}")
def get_graph_insights(tone: str, platform: str):
    """Get knowledge graph insights for a specific tone-platform combination"""
    try:
        from enhanced_knowledge_graph import EnhancedKnowledgeGraph
        kg = EnhancedKnowledgeGraph()
        
        recommendations = kg.get_recommendations(tone, platform)
        relationship = kg.explain_relationship(tone, platform)
        
        # Find related nodes
        tone_related = kg.traverse_bfs(tone, max_depth=2)
        platform_related = kg.traverse_bfs(platform, max_depth=2)
        
        return {
            "tone_platform_analysis": {
                "tone": tone,
                "platform": platform,
                "compatibility_score": recommendations["compatibility_score"],
                "relationship_explanation": relationship,
                "suggestions": recommendations["suggested_elements"],
                "warnings": recommendations["warnings"],
                "recommended_creative_types": recommendations["creative_types"]
            },
            "graph_connections": {
                "tone_connections": list(tone_related.keys()),
                "platform_connections": list(platform_related.keys())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

