import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: (refreshToken) => api.post('/auth/logout/', { refresh_token: refreshToken }),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.patch('/auth/profile/', data),
  changePassword: (data) => api.post('/auth/change-password/', data),
  getStudents: () => api.get('/auth/students/'),
};

// Ciphers
export const ciphersAPI = {
  operate: (data) => api.post('/ciphers/operate/', data),
  getInfo: (cipherType) => api.get('/ciphers/info/', { params: { cipher_type: cipherType } }),
  getAllInfo: () => api.get('/ciphers/info/all/'),
  getKeys: () => api.get('/ciphers/keys/'),
  createKey: (data) => api.post('/ciphers/keys/', data),
  updateKey: (id, data) => api.patch(`/ciphers/keys/${id}/`, data),
  deleteKey: (id) => api.delete(`/ciphers/keys/${id}/`),
  getHistory: (params) => api.get('/ciphers/history/', { params }),
};

// Attacks
export const attacksAPI = {
  caesarBruteForce: (data) => api.post('/attacks/caesar-brute-force/', data),
  frequencyAnalysis: (data) => api.post('/attacks/frequency-analysis/', data),
  hillKnownPlaintext: (data) => api.post('/attacks/hill-known-plaintext/', data),
  getRecommendations: (cipherType) => api.get('/attacks/recommendations/', { params: { cipher_type: cipherType } }),
  getLogs: (params) => api.get('/attacks/logs/', { params }),
};

// Exercises
export const exercisesAPI = {
  getExercises: (params) => api.get('/exercises/', { params }),
  getExercise: (id) => api.get(`/exercises/${id}/`),
  createExercise: (data) => api.post('/exercises/', data),
  updateExercise: (id, data) => api.patch(`/exercises/${id}/`, data),
  deleteExercise: (id) => api.delete(`/exercises/${id}/`),
  getSubmissions: (params) => api.get('/exercises/submissions/', { params }),
  submitExercise: (data) => api.post('/exercises/submissions/', data),
  updateSubmission: (id, data) => api.patch(`/exercises/submissions/${id}/`, data),
  getStudentStats: () => api.get('/exercises/student-stats/'),
  getInstructorDashboard: () => api.get('/exercises/instructor-dashboard/'),
  getActivityLogs: (params) => api.get('/exercises/activity-logs/', { params }),
  logActivity: (data) => api.post('/exercises/log-activity/', data),
};

// Messaging
export const messagingAPI = {
  getConversations: () => api.get('/messaging/conversations/'),
  createConversation: (data) => api.post('/messaging/conversations/', data),
  getConversation: (id) => api.get(`/messaging/conversations/${id}/`),
  deleteConversation: (id) => api.delete(`/messaging/conversations/${id}/`),
  getMessages: (conversationId) => api.get(`/messaging/conversations/${conversationId}/messages/`),
  sendMessage: (data) => api.post('/messaging/messages/send/', data),
  performMITMAttack: (data) => api.post('/messaging/mitm/attack/', data),
  getInterceptions: () => api.get('/messaging/mitm/interceptions/'),
};

export const isTokenValid = (token) => {
  if (!token) return false;
  try {
    const decoded = jwtDecode(token);
    return decoded.exp * 1000 > Date.now();
  } catch {
    return false;
  }
};

export default api;
