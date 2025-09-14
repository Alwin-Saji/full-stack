import React from 'react';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ message = "AI is thinking... Finding perfect gifts! 🤖✨" }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <motion.div
        className="relative w-16 h-16 mb-4"
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
      >
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-primary-200 rounded-full"></div>
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full"></div>
      </motion.div>
      
      <motion.div
        className="text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <p className="text-lg font-semibold text-gray-700 mb-2">{message}</p>
        <p className="text-sm text-gray-500">This should take less than 5 seconds...</p>
      </motion.div>
      
      {/* Bouncing gift emojis */}
      <div className="flex space-x-2 mt-4">
        {['🎁', '🎉', '✨'].map((emoji, index) => (
          <motion.span
            key={emoji}
            className="text-2xl"
            animate={{ y: [-10, 0, -10] }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              delay: index * 0.2
            }}
          >
            {emoji}
          </motion.span>
        ))}
      </div>
    </div>
  );
};

export default LoadingSpinner;