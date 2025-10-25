import api from './api';

const messagingService = {
  // Conversations
  getConversations: async () => {
    const response = await api.get('/messaging/conversations/');
    return response.data;
  },

  createConversation: async (data) => {
    const response = await api.post('/messaging/conversations/', data);
    return response.data;
  },

  getConversation: async (id) => {
    const response = await api.get(`/messaging/conversations/${id}/`);
    return response.data;
  },

  // Messages
  getMessages: async (conversationId) => {
    const response = await api.get(`/messaging/conversations/${conversationId}/messages/`);
    return response.data;
  },

  sendMessage: async (data) => {
    const response = await api.post('/messaging/messages/send/', data);
    return response.data;
  },

  // MITM Attacks
  performMITMAttack: async (data) => {
    const response = await api.post('/messaging/mitm/attack/', data);
    return response.data;
  },

  getInterceptions: async () => {
    const response = await api.get('/messaging/mitm/interceptions/');
    return response.data;
  },

  // Users (for selecting conversation partners)
  getUsers: async () => {
    const response = await api.get('/auth/users/');
    return response.data;
  }
};
