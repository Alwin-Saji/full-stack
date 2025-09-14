#!/usr/bin/env python3
"""
Gift Guru MVP Demo
Demonstrates the core recommendation functionality
"""

import sys
import os
sys.path.append('.')

from app import GiftRecommender
import pandas as pd

def demo_gift_recommendations():
    """Demo the Gift Guru recommendation system"""
    
    print("🎯 Gift Guru MVP - Core Functionality Demo")
    print("Author: MiniMax Agent")
    print("=" * 60)
    
    # Initialize recommender
    print("\n🤖 Initializing AI Gift Recommender...")
    recommender = GiftRecommender()
    print(f"✅ Loaded {len(recommender.gifts_df)} gifts from database")
    
    # Demo scenarios
    demo_scenarios = [
        {
            'name': "Gaming Enthusiast",
            'age_range': "18-25 (Young Adult)",
            'gender': "Male",
            'interests': "gaming, RGB lighting, mechanical keyboards, esports, tech gadgets",
            'occasion': "Birthday",
            'budget': (30, 70)
        },
        {
            'name': "Wellness Lover",
            'age_range': "26-35 (Millennial)", 
            'gender': "Female",
            'interests': "yoga, meditation, essential oils, self-care, mindfulness, aromatherapy",
            'occasion': "Just Because",
            'budget': (25, 60)
        },
        {
            'name': "Foodie Friend",
            'age_range': "22-30",
            'gender': "Any",
            'interests': "cooking, gourmet food, coffee, trying new recipes, kitchen gadgets",
            'occasion': "Housewarming",
            'budget': (40, 80)
        }
    ]
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🎯 Demo Scenario {i}: {scenario['name']}")
        print("-" * 40)
        
        # Create user profile
        user_profile = recommender.create_user_profile(
            scenario['age_range'],
            scenario['gender'], 
            scenario['interests'],
            scenario['occasion'],
            scenario['budget'][1]
        )
        
        print(f"👤 Profile: {scenario['age_range']}, loves {scenario['interests'][:50]}...")
        print(f"💰 Budget: ${scenario['budget'][0]}-${scenario['budget'][1]}")
        print(f"🎉 Occasion: {scenario['occasion']}")
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            user_profile,
            scenario['budget'][0],
            scenario['budget'][1], 
            num_recommendations=3
        )
        
        if recommendations:
            print(f"\n✨ Top {len(recommendations)} Gift Recommendations:")
            
            for j, rec in enumerate(recommendations, 1):
                print(f"\n  {j}. 🎁 {rec['name']} - ${rec['price']:.0f}")
                print(f"     💡 {rec['description']}")
                print(f"     🛒 {rec['link']}")
                print(f"     😄 {rec['malayali_phrase']}")
                
        else:
            print("❌ No recommendations found for this profile")
        
        print("\n" + "="*60)
    
    # Show database statistics
    print(f"\n📊 Gift Database Statistics:")
    print(f"   • Total Gifts: {len(recommender.gifts_df)}")
    print(f"   • Price Range: ${recommender.gifts_df['price'].min():.0f} - ${recommender.gifts_df['price'].max():.0f}")
    print(f"   • Categories: {', '.join(recommender.gifts_df['category'].unique()[:8])}...")
    
    # Show sample Malayali humor
    print(f"\n😄 Sample Malayali Humor Phrases:")
    for phrase in recommender.malayali_phrases[:3]:
        print(f"   • {phrase}")
    
    print(f"\n🎉 Gift Guru MVP is ready to help users find perfect gifts!")
    print(f"🚀 Run 'streamlit run app.py' to start the web application")

if __name__ == "__main__":
    demo_gift_recommendations()
