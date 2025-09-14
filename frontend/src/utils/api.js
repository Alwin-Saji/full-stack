import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const giftAPI = {
  // Get gift recommendations
  getRecommendations: async (requestData) => {
    try {
      const response = await api.post('/recommendations', requestData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get recommendations');
    }
  },

  // Submit user feedback
  submitFeedback: async (feedbackData) => {
    try {
      const response = await api.post('/feedback', feedbackData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to submit feedback');
    }
  },

  // Get API stats
  getStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get stats');
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'API is not responding');
    }
  }
};

export default api;
