# AI Ad Rewriter with Enhanced RAG and Knowledge Graph

An intelligent marketing copy generation system that rewrites ad text for different platforms using advanced AI techniques including Graph RAG, Knowledge Graph integration, and adaptive learning.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gemini API Key

### Installation
```bash
# Clone the repository
git clone https://github.com/Arittra-Bag/zocket-asg.git
cd Add Writer

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the project root with your Gemini API key:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Project Structure:**
```
zocket-asg/
├── .env                    # Your Gemini API key (create this file)
├── main.py                 # FastAPI backend server
├── index.html              # Frontend web interface
├── requirements.txt        # Python dependencies
└── ... (other files)
```

## 🏃‍♂️ Running the Complete Application

Follow these steps to run the prototype:

### Step 1: Start the Backend Server
```bash
# Run the FastAPI server
uvicorn main:app --reload

# The server will start at http://127.0.0.1:8000
# You'll see: "Uvicorn running on http://127.0.0.1:8000"
```

### Step 2: Open the Frontend
- Open `index.html` in your web browser (Chrome/Firefox/Edge)
- Simply double-click the file or drag it into your browser
- The interface will connect to the backend automatically

### Step 3: Test the Application
1. Enter an ad text (e.g., "Get 50% off on summer shoes!")
2. Select a tone (Fun, Professional, or Semi-Fun)
3. Choose platforms (Meta, Google, LinkedIn)
4. Click "Generate Optimized Ads"
5. Rate the generated ads to train the system

### API Documentation
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **Direct API calls**: Use Postman or curl

### Quick Test with cURL
```bash
# Test the API directly
curl -X POST "http://127.0.0.1:8000/run-enhanced-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "ad_text": "Summer sale - 50% off!",
    "tone": "fun",
    "platforms": ["Meta"]
  }'
```

## 📋 Submission Requirements

### 1. Use of Graph RAG / Agentic RAG ✅

Our system implements **Agentic RAG** through the `EnhancedRetriever` class:

- **Semantic Search**: Uses custom embeddings to find relevant guidelines beyond exact matches
- **Relevance Scoring**: Each retrieved guideline has a confidence score (0-1)
- **Multi-dimensional Analysis**: Considers emoji usage, formality, CTAs, and platform-specific features

**How it improves reasoning:**
- **Complex Multi-step Reasoning**: The retriever analyzes tone requirements → platform constraints → style guidelines in sequence
- **Improved Recall**: Semantic similarity captures related concepts (e.g., "fun" retrieves "playful", "energetic")
- **Enhanced Precision**: Relevance scores prioritize the most applicable guidelines

Example from `enhanced_retriever.py`:
```python
def semantic_search(self, query: str, top_k: int = 5) -> List[Tuple[str, str, float]]:
    # Performs semantic matching across all guidelines
    # Returns category, guideline, and similarity score
```

### 2. Knowledge Graph Integration ✅

The `EnhancedKnowledgeGraph` represents structured domain knowledge:

**Entities:**
- **Tones**: fun, professional, semi-fun (with formality/energy properties)
- **Platforms**: Meta, Google, LinkedIn (with char limits, emoji support)
- **Creative Types**: awareness, engagement, conversion

**Relationships:**
- `tone → platform` compatibility (weighted 0-1)
- `tone → creative_type` suitability
- `platform → creative_type` preferences

**How relationships improve relevance:**
```python
# Example: fun tone + LinkedIn platform
kg.get_recommendations("fun", "LinkedIn")
# Returns: compatibility: 0.3, warning: "Platform doesn't support emojis"
```

The graph traversal identifies:
- Incompatible combinations (warns before generation)
- Optimal creative strategies per platform
- Related nodes for context expansion

### 3. Evaluation Strategy ✅

Our comprehensive evaluation (`eval.py`) includes:

**Automated Metrics:**
- **ROUGE-L**: Measures content overlap (0.15-0.29 in tests)
- **BLEU-1**: Unigram precision with brevity penalty
- **F1 Score**: Balanced precision/recall for word overlap
- **Relevance Score**: Concept preservation (1.0 = all key concepts maintained)
- **Hallucination Detection**: Identifies invented information (0.0-0.1 range)

**Testing Approach:**
```python
# Automated testing on sample ads
original = "Get 50% off summer shoes!"
rewrites = generate_for_platforms(["Meta", "Google", "LinkedIn"])
metrics = evaluate_all(original, rewrites)
```

**Manual Testing:**
- Web interface for human evaluation
- 5-star rating system per ad
- Feedback stored for analysis

### 4. Pattern Recognition and Improvement Loop ✅

The system implements continuous learning through:

**Memory Module (`feedback_analyzer.py`):**
- Stores all user ratings with context
- Identifies winning combinations (e.g., fun+Meta: 4.5★)
- Detects underperforming patterns (e.g., fun+LinkedIn: 2.0★)

**Adaptive Learning:**
```python
# Generates performance-based weights
weights = feedback_analyzer.get_adaptive_weights()
# fun_Meta: 1.0 (high confidence)
# fun_LinkedIn: 0.6 (needs improvement)
```

**Feedback Loop:**
1. User rates generated ads (1-5 stars)
2. System analyzes patterns across tone/platform combos
3. Prompt builder adjusts weights for future generations
4. Historical insights included in prompts

**Refinement Example:**
- Initial: Generic prompts for all combinations
- After feedback: "LinkedIn shows high variance (σ=2.12) - use consistent approach"
- Result: More stable LinkedIn outputs

## 💼 Deliverables

### Working Prototype ✅
- **GitHub Repository**: Current repository with all source code
- **Live Demo**: Run locally with `uvicorn main:app --reload`
- **Web Interface**: Modern HTML frontend with GSAP animations

### FastAPI Backend ✅
**Required Endpoints:**
- `POST /run-enhanced-agent` - Main agent endpoint
- `POST /feedback` - Collect user ratings
- `GET /insights` - Performance analytics
- `GET /graph-insights/{tone}/{platform}` - KG analysis

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/run-enhanced-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "ad_text": "Summer sale - 50% off!",
    "tone": "fun",
    "platforms": ["Meta", "LinkedIn"]
  }'
```

## 📝 Technical Write-up

### Architecture and Tools Used

The AI Ad Rewriter leverages a modular architecture combining multiple AI techniques:

**Core Technologies:**
- **FastAPI**: High-performance backend framework for serving the API
- **Google Gemini 2.5 Flash**: State-of-the-art LLM for content generation
- **Custom RAG Implementation**: Enhanced retriever with semantic search capabilities
- **Graph-Based Knowledge Representation**: Python-based KG with traversal algorithms
- **Adaptive Learning System**: Feedback analyzer with pattern recognition

**Key Components:**
1. **Enhanced Prompt Builder**: Integrates RAG, KG insights, and historical performance
2. **Semantic Retriever**: Goes beyond keyword matching with embedding-based search
3. **Knowledge Graph Engine**: Models relationships between tones, platforms, and strategies
4. **Feedback Analyzer**: Mines patterns from user ratings for continuous improvement

### Challenges Faced and Solutions

**Challenge 1: Cross-Platform Consistency**
- Problem: Same tone produced wildly different results across platforms
- Solution: Implemented KG compatibility scoring to guide generation

**Challenge 2: NLTK Compatibility with Python 3.12**
- Problem: BLEU score calculation failed due to deprecated parameters
- Solution: Custom BLEU implementation focusing on unigram precision

**Challenge 3: Hallucination in Ad Copy**
- Problem: LLM added claims not in original (e.g., "limited time")
- Solution: Dedicated hallucination detection comparing source vs generated

### Potential Improvements and Next Steps

**Immediate Enhancements:**
1. **Vector Database Integration**: Replace simple embeddings with Pinecone/FAISS for scalable semantic search
2. **Neo4j Graph Database**: Migrate from Python dict to proper graph DB for complex queries
3. **A/B Testing Framework**: Automatically test variations and select winners

**Advanced Features:**
1. **Multi-LLM Ensemble**: Use multiple models (GPT-4, Claude) for diverse perspectives
2. **Real-time Learning**: Update weights immediately after each feedback
3. **Industry-Specific KGs**: Separate graphs for e-commerce, SaaS, B2B, etc.
4. **Multimodal Support**: Generate matching images/videos for ads

**Production Readiness:**
1. **Authentication**: Add API key management and user accounts
2. **Rate Limiting**: Prevent abuse with request throttling
3. **Monitoring**: Integrate with Datadog/Sentry for performance tracking
4. **Deployment**: Containerize with Docker and deploy to cloud platforms

## 🎯 Conclusion

This AI Ad Rewriter demonstrates how modern AI techniques can be combined to create an intelligent, adaptive system. By integrating Graph RAG, Knowledge Graphs, and continuous learning, I've built a solution that not only generates platform-optimized content but improves over time based on user feedback. The modular architecture ensures easy extension while maintaining the core functionality intact.
