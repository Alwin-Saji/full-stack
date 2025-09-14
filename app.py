import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import random
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="🎁 Gift Guru - Your AI Gift Recommender",
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Gen Z styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #FF6B6B;
    text-align: center;
    font-weight: bold;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #4ECDC4;
    margin-bottom: 1rem;
}
.gift-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.recommendation-reason {
    background-color: #FFF3CD;
    padding: 0.5rem;
    border-radius: 8px;
    border-left: 4px solid #FFC107;
    margin: 0.5rem 0;
}
.malayali-humor {
    background-color: #E8F5E8;
    padding: 0.5rem;
    border-radius: 8px;
    font-style: italic;
    border-left: 4px solid #28A745;
    margin: 0.5rem 0;
}
.stats-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

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
            st.error("Gift database not found! Please ensure gift_database.csv exists.")
            self.gifts_df = pd.DataFrame()
    
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
                'price': gift['price'],
                'description': gift['description'],
                'link': gift['link'],
                'category': gift['category'],
                'similarity_score': similarity_scores[idx],
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
            'average_rating': np.mean([r for r in ratings if r > 0])
        }
        
        feedback_df = pd.DataFrame([feedback_data])
        
        # Append to existing feedback file or create new one
        feedback_file = 'user_feedback.csv'
        if os.path.exists(feedback_file):
            existing_feedback = pd.read_csv(feedback_file)
            feedback_df = pd.concat([existing_feedback, feedback_df], ignore_index=True)
        
        feedback_df.to_csv(feedback_file, index=False)

# Initialize the recommender
@st.cache_resource
def load_recommender():
    return GiftRecommender()

recommender = load_recommender()

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🎁 Gift Guru</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your AI-powered gift recommender that gets it right every time! ✨</p>', unsafe_allow_html=True)
    
    # Sidebar for user input
    with st.sidebar:
        st.markdown('<h2 class="sub-header">Tell us about the gift! 🤔</h2>', unsafe_allow_html=True)
        
        # User inputs
        age_range = st.selectbox(
            "📅 Recipient's Age Range",
            ["13-17 (Teen)", "18-25 (Young Adult)", "26-35 (Millennial)", 
             "36-45 (Gen X)", "46-55 (Middle-aged)", "55+ (Senior)"]
        )
        
        gender = st.selectbox(
            "👤 Gender (Optional)",
            ["Any", "Male", "Female", "Non-binary"]
        )
        
        interests = st.text_area(
            "🎯 Interests & Hobbies",
            placeholder="e.g., gaming, reading, cooking, fitness, music, art, travel...",
            help="Describe what they love doing! The more specific, the better."
        )
        
        occasion = st.selectbox(
            "🎉 Occasion",
            ["Birthday", "Anniversary", "Christmas", "Valentine's Day", 
             "Graduation", "Housewarming", "Just Because", "Other"]
        )
        
        budget_range = st.slider(
            "💰 Budget Range ($)",
            min_value=10,
            max_value=100,
            value=(20, 60),
            step=5,
            help="Set your comfortable spending range"
        )
        
        include_malayali = st.checkbox(
            "🥥 Add Malayali humor",
            value=True,
            help="Get some fun Kerala-style commentary with your recommendations!"
        )
        
        get_recommendations = st.button(
            "🔍 Find Perfect Gifts!",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if get_recommendations and interests.strip():
        with st.spinner("🤖 AI is thinking... Finding the perfect gifts for you!"):
            # Create user profile
            user_profile = recommender.create_user_profile(
                age_range, gender, interests, occasion, budget_range[1]
            )
            
            # Get recommendations
            recommendations = recommender.get_recommendations(
                user_profile,
                budget_range[0],
                budget_range[1],
                num_recommendations=5
            )
            
            if recommendations:
                st.success(f"🎉 Found {len(recommendations)} amazing gift ideas for you!")
                
                # Display recommendations
                cols = st.columns(min(len(recommendations), 2))
                ratings = []
                
                for i, rec in enumerate(recommendations):
                    with cols[i % 2]:
                        with st.container():
                            st.markdown(
                                f"""
                                <div class="gift-card">
                                    <h3>🎁 {rec['name']}</h3>
                                    <h4>${rec['price']:.0f}</h4>
                                    <p>{rec['description']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # Recommendation reason
                            st.markdown(
                                f"""
                                <div class="recommendation-reason">
                                    <strong>💡 Why this works:</strong> Based on your interests in {interests[:50]}{'...' if len(interests) > 50 else ''} and {occasion.lower()} occasion, this is a perfect match!
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # Malayali humor
                            if include_malayali:
                                st.markdown(
                                    f"""
                                    <div class="malayali-humor">
                                        🥥 {rec['malayali_phrase']}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            
                            # Purchase link
                            st.markdown(f"[🛒 Buy this gift]({rec['link']})")
                            
                            # Rating
                            rating = st.radio(
                                "Rate this recommendation:",
                                ["⭐ (1)", "⭐⭐ (2)", "⭐⭐⭐ (3)", "⭐⭐⭐⭐ (4)", "⭐⭐⭐⭐⭐ (5)", "Skip"],
                                key=f"rating_{i}",
                                horizontal=True
                            )
                            
                            rating_value = 0 if rating == "Skip" else int(rating.split("(")[1].split(")")[0])
                            ratings.append(rating_value)
                            
                            st.divider()
                
                # Feedback submission
                if st.button("📝 Submit Feedback", type="secondary", use_container_width=True):
                    user_data = {
                        'age_range': age_range,
                        'gender': gender,
                        'interests': interests,
                        'occasion': occasion,
                        'budget_min': budget_range[0],
                        'budget_max': budget_range[1]
                    }
                    
                    recommender.save_feedback(user_data, recommendations, ratings)
                    st.success("🙏 Thank you for your feedback! It helps us improve our recommendations.")
            
            else:
                st.error("😅 Oops! Couldn't find gifts in your budget range. Try expanding your budget or different interests!")
    
    elif get_recommendations:
        st.warning("📝 Please tell us about their interests to get personalized recommendations!")
    
    else:
        # Welcome message and stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                """
                <div class="stats-card">
                    <h3>🎯</h3>
                    <p><strong>50+</strong><br>Curated Gifts</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div class="stats-card">
                    <h3>⚡</h3>
                    <p><strong>&lt;5 sec</strong><br>Response Time</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                """
                <div class="stats-card">
                    <h3>😊</h3>
                    <p><strong>Gen Z</strong><br>Friendly Tone</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(
            """
            ### How it works:
            
            1. **Tell us about the recipient** - Age, interests, and occasion
            2. **Set your budget** - We'll find gifts in your price range
            3. **Get AI-powered recommendations** - 3-5 personalized gift ideas
            4. **Rate and provide feedback** - Help us get better for everyone!
            
            ---
            
            **Pro Tips:**
            - Be specific about interests ("loves FPS games" vs "gaming")
            - Include personality traits ("minimalist", "tech enthusiast")
            - Mention any restrictions ("no food items", "eco-friendly only")
            
            Ready to find the perfect gift? Fill out the form on the left! 👈
            """
        )
    
    # Footer
    st.markdown(
        """
        ---
        <p style="text-align: center; color: #888; font-size: 0.9rem;">
        Made with ❤️ by Gift Guru | Helping you nail gift-giving since 2025 🎁
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
