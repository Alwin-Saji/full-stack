import React, { useState } from 'react';
import { Search, Settings, Amazon, Database, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

const EnhancedGiftForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    interests: '',
    age_group: '18-25',
    budget: [30, 100],
    relationship: 'friend',
    gender: 'any',
    personality: '',
    malayali_humor: false,
    use_amazon_api: true
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleBudgetChange = (index, value) => {
    const newBudget = [...formData.budget];
    newBudget[index] = parseInt(value);
    setFormData(prev => ({ ...prev, budget: newBudget }));
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
          🎁 Gift Guru - Amazon Integrated
        </h2>
        <p className="text-gray-600">
          AI-powered recommendations from millions of Amazon products
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Data Source Selection */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <Zap className="text-purple-600" size={18} />
            Data Source
          </h3>
          
          <div className="flex gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="data_source"
                checked={formData.use_amazon_api === true}
                onChange={() => handleInputChange('use_amazon_api', true)}
                className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
              />
              <div className="flex items-center gap-2">
                <Amazon size={16} className="text-orange-500" />
                <span className="text-sm font-medium">Live Amazon Products</span>
              </div>
            </label>
            
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="data_source"
                checked={formData.use_amazon_api === false}
                onChange={() => handleInputChange('use_amazon_api', false)}
                className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
              />
              <div className="flex items-center gap-2">
                <Database size={16} className="text-gray-500" />
                <span className="text-sm font-medium">Local Database</span>
              </div>
            </label>
          </div>
          
          {formData.use_amazon_api && (
            <div className="mt-2 text-xs text-gray-600 bg-orange-50 p-2 rounded border border-orange-200">
              ✨ <strong>Live Amazon Integration:</strong> Get real-time prices, ratings, and availability from millions of products
            </div>
          )}
        </div>

        {/* Interests */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            What are they interested in? *
          </label>
          <textarea
            value={formData.interests}
            onChange={(e) => handleInputChange('interests', e.target.value)}
            placeholder="e.g., gaming, cooking, fitness, reading, tech gadgets, art, music..."
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            rows={3}
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            💡 Be specific! More details = better recommendations
          </p>
        </div>

        {/* Age Group */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Age Group
          </label>
          <select
            value={formData.age_group}
            onChange={(e) => handleInputChange('age_group', e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="13-17">13-17 (Teen)</option>
            <option value="18-25">18-25 (Young Adult)</option>
            <option value="26-35">26-35 (Millennial)</option>
            <option value="36-50">36-50 (Gen X)</option>
            <option value="50+">50+ (Boomer)</option>
          </select>
        </div>

        {/* Budget Range */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Budget Range: ${formData.budget[0]} - ${formData.budget[1]}
          </label>
          <div className="space-y-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Minimum ($)</label>
              <input
                type="range"
                min="5"
                max="200"
                value={formData.budget[0]}
                onChange={(e) => handleBudgetChange(0, e.target.value)}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Maximum ($)</label>
              <input
                type="range"
                min="10"
                max="500"
                value={formData.budget[1]}
                onChange={(e) => handleBudgetChange(1, e.target.value)}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>
          </div>
        </div>

        {/* Quick Options */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Relationship
            </label>
            <select
              value={formData.relationship}
              onChange={(e) => handleInputChange('relationship', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="friend">Friend</option>
              <option value="family">Family Member</option>
              <option value="partner">Partner/Spouse</option>
              <option value="colleague">Colleague</option>
              <option value="child">Child</option>
              <option value="parent">Parent</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Gender Preference
            </label>
            <select
              value={formData.gender}
              onChange={(e) => handleInputChange('gender', e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="any">Any</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="neutral">Gender Neutral</option>
            </select>
          </div>
        </div>

        {/* Advanced Options Toggle */}
        <div className="text-center">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-purple-600 hover:text-purple-700 font-medium text-sm flex items-center gap-2 mx-auto"
          >
            <Settings size={16} />
            {showAdvanced ? 'Hide' : 'Show'} Advanced Options
          </button>
        </div>

        {/* Advanced Options */}
        {showAdvanced && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="space-y-4 border-t pt-6"
          >
            {/* Personality Traits */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Personality Traits
              </label>
              <textarea
                value={formData.personality}
                onChange={(e) => handleInputChange('personality', e.target.value)}
                placeholder="e.g., creative, practical, adventurous, introverted, minimalist..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                rows={2}
              />
            </div>

            {/* Fun Options */}
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <h4 className="font-semibold text-green-800 mb-3">
                🌴 Kerala Special Features
              </h4>
              
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.malayali_humor}
                  onChange={(e) => handleInputChange('malayali_humor', e.target.checked)}
                  className="w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500"
                />
                <div>
                  <span className="font-medium text-green-800">
                    Add Malayali Humor 😄
                  </span>
                  <p className="text-sm text-green-600">
                    Sprinkle some Kerala-style commentary on recommendations!
                  </p>
                </div>
              </label>
            </div>
          </motion.div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !formData.interests.trim()}
          className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-bold py-4 px-6 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 text-lg shadow-lg hover:shadow-xl"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Finding Perfect Gifts...
            </>
          ) : (
            <>
              <Search size={20} />
              {formData.use_amazon_api ? 'Search Amazon Products' : 'Find Local Gifts'}
            </>
          )}
        </button>

        {loading && formData.use_amazon_api && (
          <div className="text-center text-sm text-gray-600 animate-pulse">
            🔍 Searching millions of Amazon products...
          </div>
        )}
      </form>
    </div>
  );
};

export default EnhancedGiftForm;
