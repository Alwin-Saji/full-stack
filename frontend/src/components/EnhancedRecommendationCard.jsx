import React from 'react';
import { ExternalLink, Star, ShoppingCart, Award, TrendingUp, DollarSign } from 'lucide-react';
import { motion } from 'framer-motion';

const RecommendationCard = ({ gift, index, onRate, userRating }) => {
  const {
    title,
    name, // fallback for local products
    price,
    currency = 'USD',
    link,
    affiliate_url,
    image_url,
    rating,
    review_count,
    description,
    malayali_joke,
    compatibility_score,
    ai_insights = [],
    price_position,
    recommendation_reason,
    asin,
    brand,
    availability = 'Available'
  } = gift;

  const displayTitle = title || name || 'Gift Item';
  const displayUrl = affiliate_url || link || '#';
  const currencySymbol = currency === 'USD' ? '$' : currency === 'EUR' ? '€' : currency;
  const isAmazonProduct = Boolean(asin);

  const handleStarClick = (starValue) => {
    onRate(index, starValue);
  };

  const renderStars = (rating, interactive = false, size = 16) => {
    return (
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            size={size}
            className={`${
              interactive ? 'cursor-pointer hover:scale-110 transition-transform' : ''
            } ${
              star <= (interactive ? userRating || 0 : rating || 0)
                ? 'fill-yellow-400 text-yellow-400'
                : 'text-gray-300'
            }`}
            onClick={interactive ? () => handleStarClick(star) : undefined}
          />
        ))}
        {!interactive && rating > 0 && (
          <span className="text-sm text-gray-600 ml-1">
            {rating.toFixed(1)}
            {review_count > 0 && (
              <span className="text-gray-500"> ({review_count.toLocaleString()})</span>
            )}
          </span>
        )}
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group"
    >
      {/* Product Image */}
      <div className="relative h-48 bg-gradient-to-br from-purple-100 to-pink-100 overflow-hidden">
        {image_url ? (
          <img
            src={image_url}
            alt={displayTitle}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'flex';
            }}
          />
        ) : null}
        
        {/* Fallback for missing images */}
        <div className={`${image_url ? 'hidden' : 'flex'} w-full h-full items-center justify-center`}>
          <div className="text-6xl opacity-20">🎁</div>
        </div>

        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-2">
          {isAmazonProduct && (
            <div className="bg-orange-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1">
              <ShoppingCart size={12} />
              Amazon
            </div>
          )}
          
          {availability === 'Available' && (
            <div className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium">
              In Stock
            </div>
          )}
          
          {price_position === 'budget-friendly' && (
            <div className="bg-blue-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1">
              <DollarSign size={12} />
              Great Value
            </div>
          )}
          
          {rating >= 4.5 && (
            <div className="bg-yellow-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1">
              <Award size={12} />
              Top Rated
            </div>
          )}
        </div>

        {/* Compatibility Score */}
        {compatibility_score && (
          <div className="absolute top-3 right-3">
            <div className="bg-white/90 backdrop-blur-sm rounded-full px-2 py-1 text-xs font-bold flex items-center gap-1">
              <TrendingUp size={12} className="text-green-600" />
              <span className={`${
                compatibility_score >= 80 ? 'text-green-600' :
                compatibility_score >= 60 ? 'text-yellow-600' : 'text-gray-600'
              }`}>
                {compatibility_score}% match
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className="p-5">
        {/* Title and Brand */}
        <div className="mb-3">
          <h3 className="font-bold text-lg text-gray-800 line-clamp-2 group-hover:text-purple-600 transition-colors">
            {displayTitle}
          </h3>
          {brand && (
            <p className="text-sm text-gray-500 mt-1">by {brand}</p>
          )}
        </div>

        {/* Price */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-purple-600">
              {currencySymbol}{price.toFixed(2)}
            </span>
            {price_position === 'premium' && (
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                Premium
              </span>
            )}
          </div>
          
          {/* Amazon Rating */}
          {rating > 0 && (
            <div className="text-right">
              {renderStars(rating)}
            </div>
          )}
        </div>

        {/* AI Insights */}
        {ai_insights.length > 0 && (
          <div className="mb-3">
            <div className="flex flex-wrap gap-1">
              {ai_insights.slice(0, 2).map((insight, idx) => (
                <span
                  key={idx}
                  className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-full border border-blue-200"
                >
                  {insight}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Recommendation Reason */}
        {recommendation_reason && (
          <p className="text-sm text-gray-600 mb-3 italic">
            🎯 {recommendation_reason}
          </p>
        )}

        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {description || 'Perfect gift for someone special!'}
        </p>

        {/* Malayalam Humor */}
        {malayali_joke && (
          <div className="bg-gradient-to-r from-green-50 to-yellow-50 border-l-4 border-green-400 p-3 mb-4 rounded-r">
            <p className="text-sm text-green-700 font-medium">{malayali_joke}</p>
          </div>
        )}

        {/* User Rating */}
        <div className="mb-4">
          <p className="text-sm text-gray-500 mb-2">Rate this recommendation:</p>
          {renderStars(0, true, 20)}
        </div>

        {/* Action Button */}
        <a
          href={displayUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 group"
        >
          {isAmazonProduct ? 'Buy on Amazon' : 'View Product'}
          <ExternalLink size={16} className="group-hover:translate-x-1 transition-transform" />
        </a>

        {/* ASIN for Amazon products */}
        {asin && (
          <p className="text-xs text-gray-400 mt-2 text-center">
            Amazon ASIN: {asin}
          </p>
        )}
      </div>
    </motion.div>
  );
};

export default RecommendationCard;
