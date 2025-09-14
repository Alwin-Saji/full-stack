# 🎁 Gift Guru - AI Gift Recommender MVP

A Gen Z-friendly, AI-powered gift recommendation system that helps you find the perfect gifts in under 5 seconds!

## 🎯 Features

- **Smart Recommendations**: AI-powered content-based filtering using cosine similarity
- **Gen Z Vibes**: Conversational, friendly interface with optional Malayali humor
- **Budget-Friendly**: Filter gifts by your comfortable spending range ($10-$100)
- **Quick Results**: Get 3-5 personalized recommendations in under 5 seconds
- **User Feedback**: Rate recommendations to help improve the system
- **Mobile-Friendly**: Responsive web design that works on all devices

## 🚀 Quick Start

### Local Development

1. **Clone and Setup**
   ```bash
   git clone <your-repo-url>
   cd gift-recommender-mvp
   pip install -r requirements.txt
   ```

2. **Run the App**
   ```bash
   streamlit run app.py
   ```

3. **Open Browser**
   Navigate to `http://localhost:8501`

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI for your OS
   # https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy to Heroku**
   ```bash
   heroku create your-gift-guru-app
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

3. **Open Your App**
   ```bash
   heroku open
   ```

## 🎨 How It Works

### User Journey
1. **Input**: User provides recipient details (age, interests, occasion, budget)
2. **Processing**: AI creates user profile and matches against gift database
3. **Output**: 3-5 personalized gift recommendations with purchase links
4. **Feedback**: User rates recommendations for system improvement

### Technical Architecture
- **Frontend**: Streamlit with custom CSS for Gen Z styling
- **AI Engine**: scikit-learn TF-IDF + Cosine Similarity
- **Database**: CSV file with 50+ curated gifts
- **Feedback**: CSV-based storage system

## 📈 Gift Database Structure

The system includes 50+ carefully curated gifts across categories:
- **Tech & Gaming** (RGB mice, wireless earbuds, speakers)
- **Wellness & Self-Care** (skincare sets, yoga mats, essential oils)
- **Home & Lifestyle** (plants, candles, organizers)
- **Creative & Hobbies** (art supplies, craft kits, books)
- **Food & Beverages** (gourmet chocolates, coffee subscriptions)

## 🎯 Success Metrics

### Target KPIs
- **User Satisfaction**: 80% of users rate ≥4 stars
- **Response Time**: <5 seconds for recommendations
- **Engagement**: 10-20 beta users in 4-6 weeks
- **Feedback Collection**: 5-10 detailed user insights

### Current Features
✅ User input form with intuitive dropdowns and fields  
✅ AI recommendation engine with content-based filtering  
✅ Gen Z-friendly UI with conversational tone  
✅ Optional Malayali humor integration  
✅ Budget-based filtering ($10-$100 range)  
✅ User feedback and rating system  
✅ Mobile-responsive design  
✅ CSV-based data storage  

### Planned Features (v2.0)
⏳ AR gift previews  
⏳ Social media integration  
⏳ Advanced AI with deep learning  
⏳ E-commerce API integration  
⏳ User accounts and gift history  

## 🛠️ Tech Stack

- **Framework**: Streamlit 1.28.1
- **AI/ML**: scikit-learn, pandas, numpy
- **Visualization**: Plotly Express
- **Deployment**: Heroku (free tier)
- **Storage**: CSV files (scalable to PostgreSQL)

## 📊 Project Structure

```
gift-recommender-mvp/
│
├── app.py                 # Main Streamlit application
├── gift_database.csv      # Curated gift database
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── README.md             # Project documentation
├── analytics.py          # User analytics dashboard
└── user_feedback.csv     # User feedback storage (auto-generated)
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Load app successfully
- [ ] Input various user profiles
- [ ] Verify recommendations relevance
- [ ] Test budget filtering
- [ ] Check response time (<5 sec)
- [ ] Submit feedback ratings
- [ ] Test on mobile device

### Beta Testing Plan
1. **Week 1-2**: Internal testing and bug fixes
2. **Week 3-4**: Friend and family beta (5-10 users)
3. **Week 5-6**: Extended beta testing (10-20 users)
4. **Week 7**: Analysis and iteration planning

## 💻 API Integration Ready

The system is designed to easily integrate with:
- **Amazon Product API** for real-time pricing
- **Shopify/WooCommerce** for direct purchases
- **Social Media APIs** for preference learning
- **Analytics platforms** for advanced insights

## 🌐 Browser Compatibility

✅ Chrome 90+  
✅ Firefox 88+  
✅ Safari 14+  
✅ Edge 90+  
✅ Mobile browsers (iOS Safari, Chrome Mobile)  

## 📝 License

MIT License - feel free to use and modify for your projects!

## 🤝 Contributing

Want to make gift-giving even better? 

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📧 Contact

Built with ❤️ for the gift-giving community!  

**Next Steps**: Ready to find the perfect gift? Run the app and let the AI work its magic! 🪄

---
*"Making gift-giving as easy as saying 'Adipoli!' since 2025"* 🎁
