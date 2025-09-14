import React, { useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';
import { Gift, Sparkles, Heart, Amazon, Database } from 'lucide-react';

// Import enhanced components
import EnhancedGiftForm from './components/EnhancedGiftForm';
import EnhancedRecommendationCard from './components/EnhancedRecommendationCard';
import LoadingSpinner from './components/LoadingSpinner';

// API utility
import { getRecommendations, submitFeedback } from './utils/api';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [ratings, setRatings] = useState({});
  const [lastRequest, setLastRequest] = useState(null);
  const [apiStatus, setApiStatus] = useState(null);

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setRecommendations([]);
    setRatings({});
    
    const loadingToast = toast.loading(
      formData.use_amazon_api 
        ? '🔍 Searching millions of Amazon products...' 
        : '🔍 Finding perfect gifts...'
    );

    try {
      const response = await getRecommendations(formData);
      
      if (response.recommendations && response.recommendations.length > 0) {
        setRecommendations(response.recommendations);
        setLastRequest(formData);
        setApiStatus({
          dataSource: response.data_source,
          responseTime: response.response_time,
          totalFound: response.total_found,
          malayaliHumor: response.malayali_humor
        });
        
        toast.success(
          `🎉 Found ${response.total_found} perfect gifts! (${response.response_time}s)`,
          { id: loadingToast }
        );
        
        // Show Malayalam humor if available
        if (response.malayali_humor) {
          setTimeout(() => {
            toast(response.malayali_humor, {
              icon: '🌴',
              duration: 4000,
              style: {
                background: '#10B981',
                color: 'white',
              },
            });
          }, 1000);
        }
      } else {
        toast.error('No gifts found. Try different interests or budget range.', {
          id: loadingToast
        });
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      toast.error(
        error.message || 'Something went wrong. Please try again.',
        { id: loadingToast }
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRating = (giftIndex, rating) => {
    setRatings(prev => ({
      ...prev,
      [giftIndex]: rating
    }));
    
    const gift = recommendations[giftIndex];
    const giftName = gift.title || gift.name || 'this gift';
    
    toast.success(`Rated ${giftName} ${rating} stars! ⭐`, {
      duration: 2000,
    });
  };

  const handleSubmitAllFeedback = async () => {
    if (!lastRequest || Object.keys(ratings).length === 0) {
      toast.error('Please rate at least one recommendation first!');
      return;
    }

    const feedbackData = {
      recommendations: recommendations,
      ratings: Object.values(ratings),
      user_profile: lastRequest
    };

    try {
      const response = await submitFeedback(feedbackData);
      toast.success(response.message || 'Thank you for your feedback! 🙏');
      
      // Reset ratings after successful submission
      setRatings({});
    } catch (error) {
      console.error('Error submitting feedback:', error);
      toast.error('Failed to submit feedback. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50">
      {/* Toast notifications */}
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 4000,
            iconTheme: {
              primary: '#10B981',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#EF4444',
              secondary: '#fff',
            },
          },
        }}
      />

      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 backdrop-blur-md border-b border-purple-100 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl flex items-center justify-center">
                <Gift className="text-white" size={24} />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Gift Guru
                </h1>
                <p className="text-sm text-gray-500">Amazon-Integrated AI Recommendations</p>
              </div>
            </div>
            
            {/* API Status Indicator */}
            {apiStatus && (
              <div className="hidden md:flex items-center gap-2 text-sm">
                {apiStatus.dataSource === 'amazon_api' ? (
                  <div className="flex items-center gap-1 bg-orange-100 text-orange-700 px-3 py-1 rounded-full">
                    <Amazon size={14} />
                    <span>Live Amazon Data</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-1 bg-gray-100 text-gray-700 px-3 py-1 rounded-full">
                    <Database size={14} />
                    <span>Local Database</span>
                  </div>
                )}
                <span className="text-gray-500">({apiStatus.responseTime}s)</span>
              </div>
            )}
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 bg-white/80 backdrop-blur-md rounded-full px-6 py-3 border border-purple-200 mb-6">
            <Sparkles className="text-purple-600" size={20} />
            <span className="text-purple-700 font-medium">AI-Powered • Amazon-Integrated • Gen Z Friendly</span>
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold text-gray-800 mb-4">
            Find the <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Perfect Gift</span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Discover personalized gift recommendations from millions of Amazon products using our AI-powered engine. 
            <span className="text-green-600 font-medium">🌴 Now with Malayalam humor!</span>
          </p>
        </motion.div>

        {/* Gift Form */}
        <div className="mb-12">
          <EnhancedGiftForm onSubmit={handleFormSubmit} loading={loading} />
        </div>

        {/* Loading State */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex justify-center mb-12"
            >
              <LoadingSpinner />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Recommendations Grid */}
        <AnimatePresence>
          {recommendations.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mb-12"
            >
              {/* Results Header */}
              <div className="text-center mb-8">
                <h3 className="text-3xl font-bold text-gray-800 mb-2">
                  🎁 Your Perfect Gift Matches
                </h3>
                <p className="text-gray-600">
                  Found {recommendations.length} amazing gifts 
                  {apiStatus?.dataSource === 'amazon_api' && (
                    <span className="text-orange-600 font-medium">from Amazon’s catalog</span>
                  )}
                </p>
                
                {/* Data Source Badge */}
                <div className="flex justify-center mt-4">
                  {apiStatus?.dataSource === 'amazon_api' ? (
                    <div className="flex items-center gap-2 bg-orange-100 text-orange-700 px-4 py-2 rounded-full border border-orange-200">
                      <Amazon size={16} />
                      <span className="font-medium">Live Amazon Products</span>
                      <span className="text-orange-500">•</span>
                      <span className="text-sm">Real-time pricing & reviews</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-full border border-gray-200">
                      <Database size={16} />
                      <span className="font-medium">Curated Collection</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Recommendations Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {recommendations.map((gift, index) => (
                  <EnhancedRecommendationCard
                    key={index}
                    gift={gift}
                    index={index}
                    onRate={handleRating}
                    userRating={ratings[index]}
                  />
                ))}
              </div>

              {/* Feedback Section */}
              {Object.keys(ratings).length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-12 text-center"
                >
                  <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md mx-auto">
                    <Heart className="mx-auto mb-4 text-pink-500" size={32} />
                    <h4 className="text-xl font-bold text-gray-800 mb-2">
                      Thanks for Rating!
                    </h4>
                    <p className="text-gray-600 mb-6">
                      You’ve rated {Object.keys(ratings).length} recommendation{Object.keys(ratings).length !== 1 ? 's' : ''}. 
                      Help us improve by submitting your feedback.
                    </p>
                    
                    <button
                      onClick={handleSubmitAllFeedback}
                      className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 px-8 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl"
                    >
                      Submit Feedback 🙏
                    </button>
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Features Showcase */}
        {recommendations.length === 0 && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12"
          >
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Amazon className="text-orange-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Amazon Integration</h3>
              <p className="text-gray-600">
                Access millions of products with real-time pricing, customer reviews, and instant availability.
              </p>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="text-purple-600" size={32} />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">AI-Powered Matching</h3>
              <p className="text-gray-600">
                Smart algorithms analyze interests, personality, and preferences to find the perfect match.
              </p>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-green-600 text-2xl">🌴</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Kerala Special</h3>
              <p className="text-gray-600">
                Optional Malayalam humor and cultural touches make gift-giving more fun and relatable.
              </p>
            </div>
          </motion.div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-md border-t border-purple-100 mt-20">
        <div className="max-w-7xl mx-auto px-4 py-8 text-center">
          <p className="text-gray-600">
            Made with ❤️ by <span className="font-semibold text-purple-600">MiniMax Agent</span> 
            {' '}•{' '} 
            <span className="text-sm">Powered by AI • Amazon API • React • Tailwind CSS</span>
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Version 2.0.0 - Amazon Integrated Edition
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
