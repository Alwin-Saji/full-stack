import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Star, ShoppingCart, ExternalLink, Heart } from 'lucide-react';

const RecommendationCard = ({ recommendation, index, onRate }) => {
  const [rating, setRating] = useState(0);
  const [isLiked, setIsLiked] = useState(false);

  const handleRating = (value) => {
    setRating(value);
    onRate(index, value);
  };

  return (
    <motion.div
      className="gift-card relative overflow-hidden"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
    >
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-white bg-opacity-10 rounded-full -translate-y-16 translate-x-16"></div>
      <div className="absolute bottom-0 left-0 w-20 h-20 bg-white bg-opacity-10 rounded-full translate-y-10 -translate-x-10"></div>
      
      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-1">
              🎁 {recommendation.name}
            </h3>
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-yellow-300">
                ${recommendation.price}
              </span>
              <span className="text-sm bg-white bg-opacity-20 px-2 py-1 rounded-full">
                {recommendation.category}
              </span>
            </div>
          </div>
          
          <button
            onClick={() => setIsLiked(!isLiked)}
            className={`p-2 rounded-full transition-all duration-200 ${
              isLiked ? 'bg-red-500' : 'bg-white bg-opacity-20 hover:bg-opacity-30'
            }`}
          >
            <Heart className={`w-5 h-5 ${isLiked ? 'text-white fill-current' : 'text-white'}`} />
          </button>
        </div>

        {/* Description */}
        <p className="text-white text-opacity-90 mb-4 leading-relaxed">
          {recommendation.description}
        </p>

        {/* Why this works */}
        <div className="recommendation-reason mb-4">
          <div className="flex items-start space-x-2">
            <span className="text-lg">💡</span>
            <div>
              <p className="font-semibold text-yellow-800 mb-1">Why this works:</p>
              <p className="text-sm text-yellow-700">
                Perfect match based on your interests and occasion!
              </p>
            </div>
          </div>
        </div>

        {/* Malayali humor */}
        <div className="malayali-humor mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-lg">🤣</span>
            <p className="font-medium">{recommendation.malayali_phrase}</p>
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex items-center space-x-3 mb-4">
          <a
            href={recommendation.link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 bg-white text-purple-600 px-4 py-2 rounded-xl font-semibold hover:bg-opacity-90 transition-all duration-200 flex-1 justify-center"
          >
            <ShoppingCart className="w-4 h-4" />
            <span>Buy this gift</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>

        {/* Rating */}
        <div className="border-t border-white border-opacity-20 pt-4">
          <p className="text-white text-sm mb-2 font-medium">Rate this recommendation:</p>
          <div className="flex items-center space-x-1">
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                onClick={() => handleRating(value)}
                className={`p-1 rounded transition-all duration-200 ${
                  rating >= value
                    ? 'text-yellow-300 scale-110'
                    : 'text-white text-opacity-50 hover:text-opacity-75'
                }`}
              >
                <Star className={`w-6 h-6 ${
                  rating >= value ? 'fill-current' : ''
                }`} />
              </button>
            ))}
            {rating > 0 && (
              <span className="ml-2 text-white text-sm font-medium">
                {rating} star{rating !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </div>

        {/* Similarity score (for debugging) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mt-2 text-xs text-white text-opacity-50">
            Match: {(recommendation.similarity_score * 100).toFixed(1)}%
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default RecommendationCard;