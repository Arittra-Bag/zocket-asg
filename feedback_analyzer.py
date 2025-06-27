import json
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict
import statistics

class FeedbackAnalyzer:
    """Analyze feedback patterns and provide improvement recommendations"""
    
    def __init__(self, feedback_file: str = "feedback_store.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
        
    def _load_feedback(self) -> List[Dict]:
        """Load feedback from JSON file"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def analyze_patterns(self) -> Dict[str, any]:
        """Analyze patterns in feedback data"""
        if not self.feedback_data:
            return {"error": "No feedback data available"}
            
        analysis = {
            "total_feedback": len(self.feedback_data),
            "average_rating": 0,
            "tone_performance": defaultdict(list),
            "platform_performance": defaultdict(list),
            "tone_platform_combo": defaultdict(list),
            "low_performing_patterns": [],
            "high_performing_patterns": [],
            "recommendations": []
        }
        
        # Collect ratings by different dimensions
        all_ratings = []
        
        for entry in self.feedback_data:
            rating = entry.get("rating", 0)
            tone = entry.get("tone", "unknown")
            platforms = entry.get("platforms", [])
            
            all_ratings.append(rating)
            analysis["tone_performance"][tone].append(rating)
            
            for platform in platforms:
                analysis["platform_performance"][platform].append(rating)
                combo_key = f"{tone}_{platform}"
                analysis["tone_platform_combo"][combo_key].append(rating)
                
        # Calculate averages
        analysis["average_rating"] = statistics.mean(all_ratings) if all_ratings else 0
        
        # Analyze tone performance
        tone_stats = {}
        for tone, ratings in analysis["tone_performance"].items():
            if ratings:
                avg = statistics.mean(ratings)
                tone_stats[tone] = {
                    "average": avg,
                    "count": len(ratings),
                    "std_dev": statistics.stdev(ratings) if len(ratings) > 1 else 0
                }
                
        analysis["tone_stats"] = tone_stats
        
        # Analyze platform performance
        platform_stats = {}
        for platform, ratings in analysis["platform_performance"].items():
            if ratings:
                avg = statistics.mean(ratings)
                platform_stats[platform] = {
                    "average": avg,
                    "count": len(ratings),
                    "std_dev": statistics.stdev(ratings) if len(ratings) > 1 else 0
                }
                
        analysis["platform_stats"] = platform_stats
        
        # Find patterns
        combo_stats = {}
        for combo, ratings in analysis["tone_platform_combo"].items():
            if ratings:
                avg = statistics.mean(ratings)
                combo_stats[combo] = {
                    "average": avg,
                    "count": len(ratings),
                    "ratings": ratings
                }
                
                # Identify low and high performers
                if avg < 2.5 and len(ratings) >= 2:
                    analysis["low_performing_patterns"].append({
                        "pattern": combo,
                        "average_rating": avg,
                        "sample_size": len(ratings)
                    })
                elif avg >= 4.0 and len(ratings) >= 2:
                    analysis["high_performing_patterns"].append({
                        "pattern": combo,
                        "average_rating": avg,
                        "sample_size": len(ratings)
                    })
                    
        analysis["combo_stats"] = combo_stats
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
        
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Tone recommendations
        tone_stats = analysis.get("tone_stats", {})
        for tone, stats in tone_stats.items():
            if stats["average"] < 3.0:
                recommendations.append(
                    f"Consider adjusting '{tone}' tone guidelines - average rating is {stats['average']:.2f}"
                )
            elif stats["average"] > 4.5:
                recommendations.append(
                    f"'{tone}' tone is performing excellently (avg: {stats['average']:.2f}) - use as reference"
                )
                
        # Platform recommendations
        platform_stats = analysis.get("platform_stats", {})
        for platform, stats in platform_stats.items():
            if stats["std_dev"] > 1.5:
                recommendations.append(
                    f"{platform} shows high variance (σ={stats['std_dev']:.2f}) - consider more consistent approach"
                )
                
        # Combo recommendations
        for pattern in analysis.get("low_performing_patterns", []):
            tone, platform = pattern["pattern"].split("_")
            recommendations.append(
                f"{tone} tone on {platform} is underperforming (avg: {pattern['average_rating']:.2f}) - needs revision"
            )
            
        for pattern in analysis.get("high_performing_patterns", []):
            tone, platform = pattern["pattern"].split("_")
            recommendations.append(
                f"{tone} tone on {platform} is a winning combination (avg: {pattern['average_rating']:.2f})"
            )
            
        # General recommendations
        overall_avg = analysis.get("average_rating", 0)
        if overall_avg < 3.5:
            recommendations.append(
                "Overall performance needs improvement - consider reviewing prompt templates"
            )
            
        if len(analysis.get("feedback_data", [])) < 10:
            recommendations.append(
                "Limited feedback data - collect more samples for reliable patterns"
            )
            
        return recommendations
        
    def get_adaptive_weights(self) -> Dict[str, float]:
        """Generate adaptive weights for prompt building based on feedback"""
        analysis = self.analyze_patterns()
        weights = {}
        
        # Base weights
        default_weight = 1.0
        
        # Adjust weights based on performance
        for combo, stats in analysis.get("combo_stats", {}).items():
            if stats["count"] >= 2:  # Only adjust if we have enough data
                performance_ratio = stats["average"] / 5.0  # Normalize to 0-1
                weights[combo] = 0.5 + (performance_ratio * 0.5)  # Scale between 0.5-1.0
            else:
                weights[combo] = default_weight
                
        return weights
        
    def get_time_based_trends(self) -> Dict[str, any]:
        """Analyze trends over time"""
        if not self.feedback_data:
            return {"error": "No feedback data available"}
            
        # Sort by timestamp
        sorted_feedback = sorted(
            self.feedback_data,
            key=lambda x: datetime.fromisoformat(x.get("timestamp", "2024-01-01"))
        )
        
        # Group by day
        daily_ratings = defaultdict(list)
        for entry in sorted_feedback:
            timestamp = datetime.fromisoformat(entry.get("timestamp", "2024-01-01"))
            day = timestamp.date().isoformat()
            daily_ratings[day].append(entry.get("rating", 0))
            
        # Calculate daily averages
        trends = {}
        for day, ratings in daily_ratings.items():
            trends[day] = {
                "average_rating": statistics.mean(ratings),
                "count": len(ratings)
            }
            
        return trends
        
    def export_insights(self, output_file: str = "feedback_insights.json"):
        """Export analysis insights to a file"""
        analysis = self.analyze_patterns()
        trends = self.get_time_based_trends()
        weights = self.get_adaptive_weights()
        
        insights = {
            "generated_at": datetime.now().isoformat(),
            "analysis": analysis,
            "trends": trends,
            "adaptive_weights": weights
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=2)
            
        return insights 