import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Sparkles, DollarSign, Calendar, User, Heart } from 'lucide-react';

const GiftForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    age_range: '18-25 (Young Adult)',
    gender: 'Any',
    interests: '',
    occasion: 'Birthday',
    budget_min: 20,
    budget_max: 60,
    include_malayali: true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.interests.trim()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const ageRanges = [
    "13-17 (Teen)",
    "18-25 (Young Adult)",
    "26-35 (Millennial)",
    "36-45 (Gen X)",
    "46-55 (Middle-aged)",
    "55+ (Senior)"
  ];

  const occasions = [
    "Birthday",
    "Anniversary",
    "Christmas",
    "Valentine's Day",
    "Graduation",
    "Housewarming",
    "Just Because",
    "Other"
  ];

  const genderOptions = ["Any", "Male", "Female", "Non-binary"];

  return (
    <motion.div
      className="card bg-white shadow-2xl"
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center space-x-2">
          <Sparkles className="w-6 h-6 text-primary-500" />
          <span>Tell us about the gift! 🤔</span>
        </h2>
        <p className="text-gray-600">The more details, the better recommendations you'll get!</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Age Range */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center space-x-2">
            <Calendar className="w-4 h-4" />
            <span>Recipient's Age Range</span>
          </label>
          <select
            className="input-field"
            value={formData.age_range}
            onChange={(e) => handleChange('age_range', e.target.value)}
          >
            {ageRanges.map(range => (
              <option key={range} value={range}>{range}</option>
            ))}
          </select>
        </div>

        {/* Gender */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center space-x-2">
            <User className="w-4 h-4" />
            <span>Gender (Optional)</span>
          </label>
          <select
            className="input-field"
            value={formData.gender}
            onChange={(e) => handleChange('gender', e.target.value)}
          >
            {genderOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        {/* Interests */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center space-x-2">
            <Heart className="w-4 h-4" />
            <span>Interests & Hobbies *</span>
          </label>
          <textarea
            className="input-field min-h-[120px] resize-none"
            placeholder="e.g., gaming, reading, cooking, fitness, music, art, travel..."
            value={formData.interests}
            onChange={(e) => handleChange('interests', e.target.value)}
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            💡 Pro tip: Be specific! "loves FPS games" is better than just "gaming"
          </p>
        </div>

        {/* Occasion */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center space-x-2">
            <Sparkles className="w-4 h-4" />
            <span>Occasion</span>
          </label>
          <select
            className="input-field"
            value={formData.occasion}
            onChange={(e) => handleChange('occasion', e.target.value)}
          >
            {occasions.map(occasion => (
              <option key={occasion} value={occasion}>{occasion}</option>
            ))}
          </select>
        </div>

        {/* Budget Range */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3 flex items-center space-x-2">
            <DollarSign className="w-4 h-4" />
            <span>Budget Range: ${formData.budget_min} - ${formData.budget_max}</span>
          </label>
          
          <div className="space-y-4">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Minimum Budget</label>
              <input
                type="range"
                min="10"
                max="95"
                step="5"
                value={formData.budget_min}
                onChange={(e) => {
                  const newMin = parseInt(e.target.value);
                  if (newMin < formData.budget_max) {
                    handleChange('budget_min', newMin);
                  }
                }}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>
            
            <div>
              <label className="block text-xs text-gray-500 mb-1">Maximum Budget</label>
              <input
                type="range"
                min="15"
                max="100"
                step="5"
                value={formData.budget_max}
                onChange={(e) => {
                  const newMax = parseInt(e.target.value);
                  if (newMax > formData.budget_min) {
                    handleChange('budget_max', newMax);
                  }
                }}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>
          </div>
          
          <div className="flex justify-between text-xs text-gray-500 mt-2">
            <span>$10</span>
            <span className="font-semibold text-primary-600">
              Your range: ${formData.budget_min} - ${formData.budget_max}
            </span>
            <span>$100</span>
          </div>
        </div>

        {/* Malayali Humor Toggle */}
        <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-xl border border-green-200">
          <input
            type="checkbox"
            id="malayali-humor"
            checked={formData.include_malayali}
            onChange={(e) => handleChange('include_malayali', e.target.checked)}
            className="w-5 h-5 text-green-600 focus:ring-green-500 border-green-300 rounded"
          />
          <label htmlFor="malayali-humor" className="flex-1">
            <span className="font-semibold text-gray-700">🥥 Add Malayali humor</span>
            <p className="text-sm text-gray-600 mt-1">
              Get some fun Kerala-style commentary with your recommendations!
            </p>
          </label>
        </div>

        {/* Submit Button */}
        <motion.button
          type="submit"
          disabled={isLoading || !formData.interests.trim()}
          className={`w-full btn-primary flex items-center justify-center space-x-2 ${
            isLoading || !formData.interests.trim()
              ? 'opacity-50 cursor-not-allowed'
              : 'hover:shadow-xl transform hover:-translate-y-1'
          }`}
          whileHover={!isLoading ? { scale: 1.02 } : {}}
          whileTap={!isLoading ? { scale: 0.98 } : {}}
        >
          <Search className="w-5 h-5" />
          <span>
            {isLoading ? 'Finding Perfect Gifts...' : '🔍 Find Perfect Gifts!'}
          </span>
        </motion.button>
      </form>

      {/* Pro Tips */}
      <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
        <h3 className="font-semibold text-blue-800 mb-2">💡 Pro Tips:</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Be specific about interests ("loves FPS games" vs "gaming")</li>
          <li>• Include personality traits ("minimalist", "tech enthusiast")</li>
          <li>• Mention restrictions ("no food items", "eco-friendly only")</li>
        </ul>
      </div>
    </motion.div>
  );
};

export default GiftForm;