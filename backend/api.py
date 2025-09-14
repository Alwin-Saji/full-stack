from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from datetime import datetime
import os

app = FastAPI(title="Gift Guru API", description="AI-powered gift recommendations", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GiftRequest(BaseModel):
    age_range: str
    gender: str
    interests: str
    occasion: str
    budget_min: int
    budget_max: int
    include_malayali: bool = True

class FeedbackRequest(BaseModel):
    user_data: dict
    recommendations: List[dict]
    ratings: List[int]

class GiftRecommendation(BaseModel):
    name: str
    price: float
    description: str
    link: str
    category: str
    similarity_score: float
    malayali_phrase: str

class GiftRecommender:
    def __init__(self):
        self.load_gift_database()
        self.malayali_phrases = [
            "This is mallu-level epic! 🔥",
            "Adipoli choice, machane! 👌",
            "Perfect for your kuttiyude birthday! 🎂",
            "This will make them say 'Powli'! ⭐",
            "Trust me, this is absolutely pwolichath! 💯",
            "Your friend will be like 'Kollam'! 😍",
            "This gift is pure thalluka material! 🎯",
            "Guarantee: They'll say 'Kidilam'! 🚀"
        ]
    
    def load_gift_database(self):
        """Load and prepare the gift database"""
        try:
            # Try relative path first, then absolute path
            try:
                self.gifts_df = pd.read_csv('../gift_database.csv')
            except FileNotFoundError:
                self.gifts_df = pd.read_csv('gift_database.csv')
            
            # Create combined features for similarity matching
            self.gifts_df['combined_features'] = (
                self.gifts_df['category'].fillna('') + ' ' +
                self.gifts_df['tags'].fillna('') + ' ' +
                self.gifts_df['description'].fillna('')
            )
            
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=1000
            )
            
            # Fit vectorizer on gift features
            self.gift_vectors = self.vectorizer.fit_transform(self.gifts_df['combined_features'])
            
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Gift database not found")
    
    def create_user_profile(self, age_range, gender, interests, occasion, budget):
        """Create user profile for matching"""
        profile_text = f"{age_range} {gender} {interests} {occasion}"
        return profile_text.lower()
    
    def get_recommendations(self, user_profile, budget_min, budget_max, num_recommendations=5):
        """Get gift recommendations based on user profile"""
        if self.gifts_df.empty:
            return []
        
        # Filter by budget
        budget_filtered = self.gifts_df[
            (self.gifts_df['price'] >= budget_min) & 
            (self.gifts_df['price'] <= budget_max)
        ]
        
        if budget_filtered.empty:
            # If no gifts in budget, expand the range
            budget_filtered = self.gifts_df[
                self.gifts_df['price'] <= budget_max + 20
            ]
        
        if budget_filtered.empty:
            return []
        
        # Vectorize user profile
        user_vector = self.vectorizer.transform([user_profile])
        
        # Get similarity scores for budget-filtered items
        budget_indices = budget_filtered.index
        filtered_vectors = self.gift_vectors[budget_indices]
        
        similarity_scores = cosine_similarity(user_vector, filtered_vectors).flatten()
        
        # Get top recommendations
        top_indices = similarity_scores.argsort()[-num_recommendations:][::-1]
        
        recommendations = []
        for idx in top_indices:
            gift_idx = budget_indices[idx]
            gift = self.gifts_df.iloc[gift_idx]
            
            recommendations.append({
                'name': gift['product_name'],
                'price': float(gift['price']),
                'description': gift['description'],
                'link': gift['link'],
                'category': gift['category'],
                'similarity_score': float(similarity_scores[idx]),
                'malayali_phrase': random.choice(self.malayali_phrases)
            })
        
        return recommendations

    def save_feedback(self, user_data, recommendations, ratings):
        """Save user feedback to CSV"""
        feedback_data = {
            'timestamp': datetime.now().isoformat(),
            'age_range': user_data.get('age_range', ''),
            'gender': user_data.get('gender', ''),
            'interests': user_data.get('interests', ''),
            'occasion': user_data.get('occasion', ''),
            'budget': f"${user_data.get('budget_min', 0)}-${user_data.get('budget_max', 0)}",
            'recommendations': str([r['name'] for r in recommendations]),
            'ratings': str(ratings),
            'average_rating': np.mean([r for r in ratings if r > 0]) if any(r > 0 for r in ratings) else 0
        }
        
        feedback_df = pd.DataFrame([feedback_data])
        
        # Append to existing feedback file or create new one
        try:
            feedback_file = '../user_feedback.csv'
            if not os.path.exists(feedback_file):
                feedback_file = 'user_feedback.csv'
        except:
            feedback_file = 'user_feedback.csv'
        if os.path.exists(feedback_file):
            existing_feedback = pd.read_csv(feedback_file)
            feedback_df = pd.concat([existing_feedback, feedback_df], ignore_index=True)
        
        feedback_df.to_csv(feedback_file, index=False)
        return True

# Initialize the recommender
recommender = GiftRecommender()

@app.get("/")
async def root():
    return {"message": "Gift Guru API is running! 🎁✨", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_loaded": len(recommender.gifts_df) > 0,
        "total_gifts": len(recommender.gifts_df)
    }

@app.post("/recommendations", response_model=List[GiftRecommendation])
async def get_recommendations(request: GiftRequest):
    """Get personalized gift recommendations"""
    try:
        # Create user profile
        user_profile = recommender.create_user_profile(
            request.age_range,
            request.gender,
            request.interests,
            request.occasion,
            request.budget_max
        )
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            user_profile,
            request.budget_min,
            request.budget_max,
            num_recommendations=5
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=404, 
                detail="No gifts found matching your criteria. Try adjusting your budget or interests!"
            )
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback for recommendations"""
    try:
        success = recommender.save_feedback(
            request.user_data,
            request.recommendations,
            request.ratings
        )
        
        if success:
            return {"message": "Thank you for your feedback! 🙏", "success": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to save feedback")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving feedback: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        stats = {
            "total_gifts": len(recommender.gifts_df),
            "price_range": {
                "min": float(recommender.gifts_df['price'].min()),
                "max": float(recommender.gifts_df['price'].max())
            },
            "categories": recommender.gifts_df['category'].unique().tolist(),
            "malayali_phrases_count": len(recommender.malayali_phrases)
        }
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
