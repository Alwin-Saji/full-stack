"""Enhanced FastAPI backend with Amazon API integration"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

from amazon_api import amazon_api, AmazonProduct

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Gift Guru API - Amazon Integrated",
    description="AI-powered gift recommendations with live Amazon product data",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class RecommendationRequest(BaseModel):
    interests: str = Field(..., description="User's interests and hobbies")
    age_group: str = Field(..., description="Age group (13-17, 18-25, 26-35, 36-50, 50+)")
    budget: List[int] = Field(..., description="Budget range [min, max]")
    relationship: str = Field(..., description="Relationship to recipient")
    gender: str = Field(..., description="Gender preference")
    personality: str = Field(..., description="Personality traits")
    malayali_humor: bool = Field(default=False, description="Add Malayalam humor")
    use_amazon_api: bool = Field(default=True, description="Use live Amazon data")

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    total_found: int
    response_time: float
    data_source: str  # "amazon_api" or "local_database"
    malayali_humor: Optional[str] = None

class FeedbackRequest(BaseModel):
    recommendations: List[Dict[str, Any]]
    ratings: List[int]
    user_profile: Dict[str, Any]

# Global variables
local_df = None
tfidf_vectorizer = None
tfidf_matrix = None

def load_local_database():
    """Load local gift database as fallback"""
    global local_df, tfidf_vectorizer, tfidf_matrix
    
    try:
        local_df = pd.read_csv('gift_database.csv')
        
        # Create TF-IDF matrix for local products
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = tfidf_vectorizer.fit_transform(local_df['tags'])
        
        logger.info(f"Loaded {len(local_df)} local products")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load local database: {e}")
        return False

def get_malayali_humor() -> str:
    """Generate Malayalam-inspired humor"""
    humor_options = [
        "Adipoli choice, machane! 👌",
        "Pwoli gift aanu ithu! 🔥", 
        "Ithokke gift koduthaal, recipient parayum 'njan poli aanu' ennu! 😄",
        "Mass gift! Perfect for any celebration! 🎉",
        "Kerala style gift recommendation! Traditional yet modern! 🌴",
        "Gift guru level: Malayalam Boss! 😎"
    ]
    
    return np.random.choice(humor_options)

def search_amazon_products(interests: str, 
                         age_group: str,
                         budget: List[int],
                         max_results: int = 10) -> List[AmazonProduct]:
    """Search Amazon for relevant products"""
    
    # Enhanced keyword generation based on age group
    age_keywords = {
        "13-17": ["teen", "student", "gaming", "trendy", "tech"],
        "18-25": ["college", "young adult", "lifestyle", "gadgets", "fashion"],
        "26-35": ["professional", "home", "fitness", "premium", "quality"],
        "36-50": ["family", "luxury", "practical", "wellness", "hobby"],
        "50+": ["comfort", "classic", "health", "traditional", "relaxation"]
    }
    
    # Combine user interests with age-appropriate keywords
    search_keywords = f"{interests} {' '.join(age_keywords.get(age_group, []))}"
    
    # Multiple search strategies
    products = []
    
    # Primary search with user interests
    primary_results = amazon_api.search_products(
        keywords=search_keywords,
        min_price=budget[0],
        max_price=budget[1],
        max_results=max_results
    )
    products.extend(primary_results)
    
    # If not enough results, try broader searches
    if len(products) < max_results // 2:
        # Search by interest categories
        interest_words = interests.lower().split()
        for word in interest_words[:3]:  # Top 3 interest words
            if len(word) > 3:  # Skip short words
                additional_results = amazon_api.search_products(
                    keywords=f"{word} gift",
                    min_price=budget[0],
                    max_price=budget[1],
                    max_results=3
                )
                products.extend(additional_results)
                
                if len(products) >= max_results:
                    break
    
    # Remove duplicates based on ASIN
    seen_asins = set()
    unique_products = []
    for product in products:
        if product.asin not in seen_asins:
            seen_asins.add(product.asin)
            unique_products.append(product)
    
    return unique_products[:max_results]

def search_local_products(interests: str, budget: List[int], max_results: int = 10) -> List[Dict]:
    """Search local database for products"""
    if local_df is None or tfidf_vectorizer is None:
        return []
    
    try:
        # Filter by budget
        budget_filtered = local_df[
            (local_df['price'] >= budget[0]) & 
            (local_df['price'] <= budget[1])
        ].copy()
        
        if budget_filtered.empty:
            return []
        
        # TF-IDF similarity matching
        user_interests_vector = tfidf_vectorizer.transform([interests])
        budget_tfidf = tfidf_vectorizer.transform(budget_filtered['tags'])
        
        similarities = cosine_similarity(user_interests_vector, budget_tfidf).flatten()
        
        # Add similarity scores
        budget_filtered.loc[:, 'similarity'] = similarities
        
        # Sort by similarity and get top results
        top_results = budget_filtered.nlargest(max_results, 'similarity')
        
        return top_results.to_dict('records')
        
    except Exception as e:
        logger.error(f"Local search error: {e}")
        return []

def enhance_recommendations_with_ai_insights(products: List[Dict], 
                                           user_profile: Dict) -> List[Dict]:
    """Add AI-generated insights and compatibility scores"""
    
    enhanced = []
    for product in products:
        try:
            # Calculate compatibility score based on user profile
            compatibility_factors = []
            
            # Age appropriateness
            age_score = 0.8  # Default high score
            if user_profile.get('age_group') == '13-17' and 'mature' in product.get('title', '').lower():
                age_score = 0.3
            elif user_profile.get('age_group') == '50+' and 'gaming' in product.get('title', '').lower():
                age_score = 0.5
            
            compatibility_factors.append(age_score)
            
            # Price appropriateness (closer to middle of budget = higher score)
            budget = user_profile.get('budget', [20, 100])
            price = product.get('price', 0)
            budget_mid = (budget[0] + budget[1]) / 2
            price_score = 1 - abs(price - budget_mid) / (budget[1] - budget[0])
            price_score = max(0.2, min(1.0, price_score))
            
            compatibility_factors.append(price_score)
            
            # Overall compatibility
            compatibility = np.mean(compatibility_factors) * 100
            
            # AI insights based on product and user profile
            insights = []
            
            if product.get('rating', 0) > 4.0:
                insights.append("⭐ Highly rated by customers")
            
            if product.get('review_count', 0) > 100:
                insights.append("📊 Popular choice with many reviews")
            
            if price < budget_mid:
                insights.append("💰 Great value for money")
            
            if 'premium' in product.get('title', '').lower() or price > budget_mid * 1.5:
                insights.append("✨ Premium quality option")
            
            # Enhanced product data
            enhanced_product = product.copy()
            enhanced_product.update({
                'compatibility_score': round(compatibility, 1),
                'ai_insights': insights,
                'price_position': 'budget-friendly' if price < budget_mid else 'premium',
                'recommendation_reason': f"Matches your interest in {user_profile.get('interests', 'gifts').split()[0]}"
            })
            
            enhanced.append(enhanced_product)
            
        except Exception as e:
            logger.error(f"Enhancement error: {e}")
            enhanced.append(product)
    
    return enhanced

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("🚀 Starting Gift Guru API with Amazon Integration")
    
    # Load local database as fallback
    if load_local_database():
        logger.info("✅ Local database loaded successfully")
    else:
        logger.warning("⚠️ Local database not available")
    
    # Check Amazon API status
    api_status = amazon_api.get_api_status()
    if api_status['api_available']:
        logger.info("✅ Amazon API ready")
    else:
        logger.warning("⚠️ Amazon API not available - using local data only")

@app.get("/")
async def root():
    """API health check"""
    api_status = amazon_api.get_api_status()
    return {
        "service": "Gift Guru API - Amazon Integrated",
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "local_database": local_df is not None,
        "local_products_count": len(local_df) if local_df is not None else 0,
        **api_status
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get gift recommendations with Amazon integration"""
    start_time = datetime.now()
    
    try:
        recommendations = []
        data_source = "unknown"
        
        # User profile for AI enhancement
        user_profile = {
            'interests': request.interests,
            'age_group': request.age_group,
            'budget': request.budget,
            'relationship': request.relationship,
            'gender': request.gender,
            'personality': request.personality
        }
        
        # Try Amazon API first if enabled and available
        if request.use_amazon_api and amazon_api.get_api_status()['api_available']:
            logger.info("🔍 Searching Amazon products...")
            
            amazon_products = search_amazon_products(
                interests=request.interests,
                age_group=request.age_group,
                budget=request.budget,
                max_results=10
            )
            
            if amazon_products:
                # Convert Amazon products to dict format
                amazon_dicts = [product.to_dict() for product in amazon_products]
                recommendations = enhance_recommendations_with_ai_insights(
                    amazon_dicts, user_profile
                )
                data_source = "amazon_api"
                logger.info(f"✅ Found {len(recommendations)} Amazon products")
            else:
                logger.warning("No Amazon products found, falling back to local database")
        
        # Fallback to local database if Amazon API didn't work or wasn't used
        if not recommendations:
            logger.info("🔍 Searching local database...")
            
            local_products = search_local_products(
                interests=request.interests,
                budget=request.budget,
                max_results=10
            )
            
            if local_products:
                recommendations = enhance_recommendations_with_ai_insights(
                    local_products, user_profile
                )
                data_source = "local_database"
                logger.info(f"✅ Found {len(recommendations)} local products")
            else:
                logger.warning("No products found in local database either")
        
        # Generate Malayalam humor if requested
        malayali_humor_text = None
        if request.malayali_humor and recommendations:
            malayali_humor_text = get_malayali_humor()
        
        # Calculate response time
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_found=len(recommendations),
            response_time=round(response_time, 3),
            data_source=data_source,
            malayali_humor=malayali_humor_text
        )
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit user feedback for recommendations"""
    try:
        # Save feedback (implement your storage logic here)
        feedback_data = {
            'timestamp': datetime.now().isoformat(),
            'ratings': feedback.ratings,
            'average_rating': np.mean(feedback.ratings),
            'user_profile': feedback.user_profile,
            'total_recommendations': len(feedback.recommendations)
        }
        
        logger.info(f"📊 Feedback received: avg rating {feedback_data['average_rating']:.1f}")
        
        return {
            "status": "success",
            "message": "Thank you for your feedback! 🙏",
            "average_rating": round(feedback_data['average_rating'], 1)
        }
        
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/amazon-status")
async def amazon_api_status():
    """Get detailed Amazon API status"""
    status = amazon_api.get_api_status()
    
    # Additional diagnostics
    credentials_available = all([
        os.getenv('AMAZON_API_KEY'),
        os.getenv('AMAZON_API_SECRET'),
        os.getenv('AMAZON_ASSOCIATE_TAG')
    ])
    
    return {
        **status,
        "credentials_configured": credentials_available,
        "country": os.getenv('AMAZON_COUNTRY', 'US'),
        "sdk_installed": AmazonApi is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
