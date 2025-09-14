from app import GiftRecommender
import time

print('🎯 LIVE DEMO: Gift Guru AI in Action')
print('='*50)

# Initialize the recommender
recommender = GiftRecommender()
print(f'✅ AI Engine Loaded: {len(recommender.gifts_df)} gifts ready')

# Sample user input (what you'd enter in the web form)
print('\n📝 Sample User Input:')
print('   Age: 18-25 (Young Adult)')
print('   Interests: gaming, RGB lighting, mechanical keyboards')
print('   Occasion: Birthday') 
print('   Budget: $30-70')

# Create user profile and get recommendations
user_profile = recommender.create_user_profile(
    '18-25 (Young Adult)',
    'Male', 
    'gaming, RGB lighting, mechanical keyboards, esports',
    'Birthday',
    70
)

# Time the recommendation process
start_time = time.time()
recommendations = recommender.get_recommendations(user_profile, 30, 70, 3)
response_time = time.time() - start_time

print(f'\n⚡ AI Processing Time: {response_time:.3f} seconds (Target: <5s)')
print(f'✨ Generated {len(recommendations)} personalized recommendations:')

# Display results
for i, rec in enumerate(recommendations, 1):
    print(f'\n🎁 Recommendation {i}:')
    print(f'   Name: {rec["name"]}')
    print(f'   Price: ${rec["price"]:.0f}')
    print(f'   Why: {rec["description"]}')
    print(f'   Humor: {rec["malayali_phrase"]}')
    print(f'   Buy: {rec["link"]}')

print(f'\n🎯 Success! Perfect gifts found in {response_time:.3f}s')
