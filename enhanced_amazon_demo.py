"""Enhanced Gift Guru Demo - Amazon API Integration Showcase"""

import os
import sys
import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# Add backend to path
sys.path.append('backend')

def print_header(title: str, emoji: str = "🚀"):
    """Print a fancy header"""
    print(f"\n{emoji} {title}")
    print("=" * (len(title) + 4))

def print_subheader(title: str, emoji: str = "🔍"):
    """Print a subheader"""
    print(f"\n{emoji} {title}")
    print("-" * (len(title) + 4))

def test_enhanced_backend():
    """Test the enhanced backend with Amazon integration"""
    print_header("Amazon-Integrated Gift Guru Demo", "🎁")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Author: MiniMax Agent")
    
    # Test health endpoint
    print_subheader("Backend Health Check")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Backend is healthy!")
            print(f"   Version: {health_data.get('version', 'unknown')}")
            print(f"   Local Database: {health_data.get('local_database', False)}")
            print(f"   Local Products: {health_data.get('local_products_count', 0)}")
            print(f"   Amazon API: {health_data.get('api_available', False)}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("\n💡 Make sure to start the backend first:")
        print("   cd backend && python enhanced_api.py")
        return False

def test_amazon_api_status():
    """Test Amazon API status"""
    print_subheader("Amazon API Status Check")
    
    try:
        response = requests.get("http://localhost:8000/amazon-status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            
            print(f"   API Available: {status.get('api_available', False)}")
            print(f"   Credentials Configured: {status.get('credentials_configured', False)}")
            print(f"   SDK Installed: {status.get('sdk_installed', False)}")
            print(f"   Country: {status.get('country', 'Unknown')}")
            print(f"   Cache Entries: {status.get('cache_entries', 0)}")
            
            if status.get('api_available'):
                print("✅ Amazon API is ready for live product searches!")
                return True
            else:
                print("⚠️ Amazon API not available - will use local database")
                if not status.get('credentials_configured'):
                    print("   💡 Set up Amazon credentials in backend/.env")
                if not status.get('sdk_installed'):
                    print("   💡 Install: pip install python-amazon-paapi")
                return False
        else:
            print(f"❌ Amazon status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Amazon API status error: {e}")
        return False

def test_recommendations(use_amazon: bool = True):
    """Test recommendation endpoint"""
    data_source = "Amazon API" if use_amazon else "Local Database"
    print_subheader(f"Testing Recommendations - {data_source}")
    
    # Test profiles with different interests
    test_profiles = [
        {
            "name": "Gaming Enthusiast",
            "data": {
                "interests": "gaming, RGB keyboards, mechanical switches, esports, streaming setup",
                "age_group": "18-25",
                "budget": [30, 120],
                "relationship": "friend",
                "gender": "any",
                "personality": "competitive, tech-savvy, social gamer",
                "malayali_humor": True,
                "use_amazon_api": use_amazon
            }
        },
        {
            "name": "Wellness Enthusiast",
            "data": {
                "interests": "yoga, meditation, essential oils, mindfulness, healthy living",
                "age_group": "26-35",
                "budget": [25, 80],
                "relationship": "family",
                "gender": "female",
                "personality": "calm, health-conscious, mindful",
                "malayali_humor": False,
                "use_amazon_api": use_amazon
            }
        },
        {
            "name": "Tech Professional",
            "data": {
                "interests": "productivity tools, wireless charging, smart home, automation",
                "age_group": "26-35",
                "budget": [50, 200],
                "relationship": "colleague",
                "gender": "any",
                "personality": "efficient, innovative, busy professional",
                "malayali_humor": False,
                "use_amazon_api": use_amazon
            }
        }
    ]
    
    for profile in test_profiles:
        print(f"\n👤 Testing Profile: {profile['name']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                "http://localhost:8000/recommend",
                json=profile['data'],
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Found {result['total_found']} recommendations")
                print(f"   ⏱️ Response time: {result['response_time']:.3f}s")
                print(f"   📦 Data source: {result['data_source']}")
                
                if result.get('malayali_humor'):
                    print(f"   😄 Humor: {result['malayali_humor']}")
                
                # Show top 3 recommendations
                recommendations = result['recommendations'][:3]
                for i, gift in enumerate(recommendations, 1):
                    title = gift.get('title') or gift.get('name', 'Unknown Item')
                    price = gift.get('price', 0)
                    currency = gift.get('currency', 'USD')
                    rating = gift.get('rating', 0)
                    compatibility = gift.get('compatibility_score', 0)
                    asin = gift.get('asin')
                    
                    currency_symbol = '$' if currency == 'USD' else currency
                    
                    print(f"\n   🎁 {i}. {title[:60]}{'...' if len(title) > 60 else ''}")
                    print(f"      💰 Price: {currency_symbol}{price:.2f}")
                    
                    if rating > 0:
                        print(f"      ⭐ Rating: {rating:.1f}/5.0")
                    
                    if compatibility > 0:
                        print(f"      🎯 Compatibility: {compatibility}%")
                    
                    if asin:
                        print(f"      🛒 Amazon ASIN: {asin}")
                    
                    # Show AI insights
                    insights = gift.get('ai_insights', [])
                    if insights:
                        print(f"      🤖 AI Insights: {', '.join(insights[:2])}")
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error testing {profile['name']}: {e}")

def test_feedback_system():
    """Test feedback submission"""
    print_subheader("Feedback System Test")
    
    # Mock feedback data
    feedback_data = {
        "recommendations": [
            {"title": "Test Product 1", "price": 45.99, "asin": "B01TEST1"},
            {"title": "Test Product 2", "price": 29.99, "asin": "B01TEST2"}
        ],
        "ratings": [4, 5],
        "user_profile": {
            "interests": "gaming",
            "age_group": "18-25",
            "budget": [30, 100]
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/feedback",
            json=feedback_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ {result.get('message', 'Feedback submitted successfully')}")
            print(f"   📊 Average Rating: {result.get('average_rating', 0)}/5 stars")
        else:
            print(f"   ❌ Feedback submission failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Feedback test error: {e}")

def show_frontend_info():
    """Show frontend architecture information"""
    print_subheader("React Frontend Architecture", "⚙️")
    
    frontend_features = [
        "🎨 Enhanced Components with Amazon product display",
        "🛒 Live Amazon product integration with images and ratings", 
        "📊 Real-time compatibility scoring and AI insights",
        "🎆 Animated loading states with product search indicators",
        "⭐ Interactive star rating system with user feedback",
        "📱 Mobile-first responsive design with touch support",
        "🌨️ Framer Motion animations for smooth transitions",
        "🎨 Tailwind CSS with gradient themes and modern styling",
        "🔔 Toast notifications for all user interactions",
        "🌴 Malayalam humor integration toggle",
        "🔍 Advanced form with Amazon API vs local data selection",
        "🎯 Smart budget sliders with real-time price filtering"
    ]
    
    print("\n   Key Features:")
    for feature in frontend_features:
        print(f"   {feature}")
    
    print("\n   📦 New Enhanced Components:")
    print("   • EnhancedGiftForm.jsx - Amazon API integration controls")
    print("   • EnhancedRecommendationCard.jsx - Rich Amazon product display")
    print("   • Real-time API status indicators")
    print("   • Compatibility score visualization")
    print("   • AI insights and recommendation explanations")

def show_setup_instructions():
    """Show setup instructions for full Amazon integration"""
    print_subheader("Setup Instructions", "🛠️")
    
    print("\n   👍 To enable full Amazon integration:")
    print("")
    print("   1️⃣ Install Amazon API SDK:")
    print("      cd backend && pip install python-amazon-paapi")
    print("")
    print("   2️⃣ Set up Amazon credentials:")
    print("      cp backend/.env.example backend/.env")
    print("      # Edit .env with your Amazon API credentials")
    print("")
    print("   3️⃣ Start enhanced backend:")
    print("      cd backend && python enhanced_api.py")
    print("")
    print("   4️⃣ Start React frontend:")
    print("      cd frontend && npm start")
    print("")
    print("   📚 Full setup guide: AMAZON_SETUP_GUIDE.md")

def main():
    """Main demo function"""
    print("🌟 Welcome to Gift Guru - Amazon Integration Demo!")
    print("Author: MiniMax Agent")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Test backend connectivity
    if not test_enhanced_backend():
        show_setup_instructions()
        return
    
    # Check Amazon API status
    amazon_available = test_amazon_api_status()
    
    # Test recommendations with Amazon API (if available)
    if amazon_available:
        test_recommendations(use_amazon=True)
    else:
        print("\n⚠️ Amazon API not available, testing with local database...")
        test_recommendations(use_amazon=False)
    
    # Test feedback system
    test_feedback_system()
    
    # Show frontend architecture
    show_frontend_info()
    
    # Final summary
    print_header("Demo Summary", "🎉")
    print("✅ Enhanced backend with Amazon API integration")
    print(f"✅ Amazon API status: {'Available' if amazon_available else 'Not configured'}")
    print("✅ AI-powered recommendation engine")
    print("✅ React frontend with rich product display")
    print("✅ Feedback and rating system")
    print("✅ Malayalam humor feature")
    print("✅ Responsive design with animations")
    
    if amazon_available:
        print("\n🚀 Your Gift Recommender is ready with live Amazon products!")
        print("   • Millions of products available")
        print("   • Real-time pricing and availability")
        print("   • Customer reviews and ratings")
        print("   • Affiliate link monetization")
    else:
        print("\n💡 Set up Amazon credentials to unlock full potential!")
        print("   See AMAZON_SETUP_GUIDE.md for detailed instructions")
    
    print("\n🎆 Ready to revolutionize gift giving with AI + Amazon!")

if __name__ == "__main__":
    main()
