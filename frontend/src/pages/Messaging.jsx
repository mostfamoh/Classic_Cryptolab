import { useState, useEffect } from 'react';
import { messagingAPI } from '../services/api';
import api from '../services/api';

export default function Messaging() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [showNewConversation, setShowNewConversation] = useState(false);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [showSteps, setShowSteps] = useState(true);
  const [attackDetails, setAttackDetails] = useState({});
  const [loadingAttackDetails, setLoadingAttackDetails] = useState({});
  const [decryptedMessages, setDecryptedMessages] = useState({});
  const [decryptingMessages, setDecryptingMessages] = useState({});

  // New conversation form
  const [newConvData, setNewConvData] = useState({
    user_b_id: '',
    cipher_type: 'caesar',
    key: { shift: 3 }
  });

  const getCurrentUser = () => {
    try {
      const userStr = localStorage.getItem('user');
      return userStr ? JSON.parse(userStr) : { id: null, username: 'Unknown' };
    } catch (e) {
      console.error('Error parsing user from localStorage:', e);
      return { id: null, username: 'Unknown' };
    }
  };

  const currentUser = getCurrentUser();

  useEffect(() => {
    loadConversations();
    loadUsers();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      loadMessages(selectedConversation.id);
    }
  }, [selectedConversation]);

  const loadConversations = async () => {
    try {
      setLoading(true);
      const response = await messagingAPI.getConversations();
      // Handle both paginated response and direct array
      const convData = response.data.results || response.data;
      setConversations(Array.isArray(convData) ? convData : []);
      setError('');
    } catch (err) {
      setError('Failed to load conversations: ' + (err.response?.data?.detail || err.message));
      console.error('Load conversations error:', err);
      setConversations([]);
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      console.log('Loading users...');
      const response = await api.get('/auth/users/');
      console.log('Users loaded:', response.data);
      // Handle both paginated response and direct array
      const userData = response.data.results || response.data;
      setUsers(Array.isArray(userData) ? userData : []);
    } catch (err) {
      console.error('Failed to load users:', err);
      console.error('Error response:', err.response);
      setError('Failed to load users: ' + (err.response?.data?.detail || err.message));
      setUsers([]);
    }
  };

  const loadMessages = async (conversationId) => {
    try {
      const response = await messagingAPI.getMessages(conversationId);
      // Handle both paginated response and direct array
      const msgData = response.data.results || response.data;
      setMessages(Array.isArray(msgData) ? msgData : []);
    } catch (err) {
      setError('Failed to load messages');
      console.error(err);
      setMessages([]);
    }
  };

  const loadAttackDetailsForMessage = async (messageId) => {
    if (attackDetails[messageId]) return; // Already loaded
    
    setLoadingAttackDetails(prev => ({ ...prev, [messageId]: true }));
    try {
      const response = await messagingAPI.getInterceptions();
      const intData = response.data.results || response.data;
      const interceptions = Array.isArray(intData) ? intData : [];
      
      // Find attack details for this message
      const messageAttack = interceptions.find(
        int => int.original_message?.id === messageId
      );
      
      if (messageAttack) {
        setAttackDetails(prev => ({ ...prev, [messageId]: messageAttack }));
      }
    } catch (err) {
      console.error('Failed to load attack details:', err);
    } finally {
      setLoadingAttackDetails(prev => ({ ...prev, [messageId]: false }));
    }
  };

  const handleDecryptMessage = async (message) => {
    if (decryptedMessages[message.id]) return; // Already decrypted
    
    setDecryptingMessages(prev => ({ ...prev, [message.id]: true }));
    try {
      // Call the cipher API to decrypt the message
      const response = await api.post('/ciphers/operate/', {
        cipher_type: selectedConversation.cipher_type,
        operation: 'decrypt',
        text: message.ciphertext,
        key: selectedConversation.shared_key,
        show_steps: showSteps
      });
      
      setDecryptedMessages(prev => ({
        ...prev,
        [message.id]: {
          plaintext: response.data.result,
          steps: response.data.steps || []
        }
      }));
    } catch (err) {
      console.error('Failed to decrypt message:', err);
      alert('Failed to decrypt message: ' + (err.response?.data?.error || err.message));
    } finally {
      setDecryptingMessages(prev => ({ ...prev, [message.id]: false }));
    }
  };

  const handleCreateConversation = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      const conversationData = {
        user_b_id: parseInt(newConvData.user_b_id),
        cipher_type: newConvData.cipher_type,
        shared_key: newConvData.key
      };

      const response = await messagingAPI.createConversation(conversationData);
      
      // Handle both new conversation and existing conversation
      const conversation = response.data.conversation || response.data;
      
      // Check if it already exists in the list
      const existingIndex = conversations.findIndex(c => c.id === conversation.id);
      
      if (existingIndex === -1) {
        // Add to list if it's new
        setConversations([conversation, ...conversations]);
        setSuccessMsg('Conversation created successfully!');
      } else {
        setSuccessMsg('Opening existing conversation with this user');
      }
      
      setShowNewConversation(false);
      setSelectedConversation(conversation);
      setNewConvData({
        user_b_id: '',
        cipher_type: 'caesar',
        key: { shift: 3 }
      });
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create conversation');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteConversation = async (conversationId, e) => {
    // Stop propagation to prevent selecting the conversation when clicking delete
    if (e) e.stopPropagation();
    
    if (!window.confirm('Are you sure you want to delete this conversation? All messages will be lost.')) {
      return;
    }
    
    try {
      await messagingAPI.deleteConversation(conversationId);
      
      // Remove from list
      setConversations(conversations.filter(c => c.id !== conversationId));
      
      // Clear selection if this was the selected conversation
      if (selectedConversation?.id === conversationId) {
        setSelectedConversation(null);
        setMessages([]);
      }
      
      setSuccessMsg('Conversation deleted successfully');
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err) {
      setError('Failed to delete conversation: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedConversation) return;

    setLoading(true);
    setError('');

    try {
      const messageData = {
        conversation_id: selectedConversation.id,
        plaintext: newMessage,
        show_steps: showSteps
      };

      const response = await messagingAPI.sendMessage(messageData);
      const sentMessage = response.data;
      setMessages([...messages, sentMessage]);
      setNewMessage('');
      
      // Update conversation timestamp
      loadConversations();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const updateKeyForCipher = (cipherType) => {
    const defaultKeys = {
      caesar: { shift: 3 },
      affine: { a: 5, b: 8 },
      hill: { matrix: [[3, 3], [2, 5]] },
      playfair: { keyword: 'SECRET' }
    };
    setNewConvData({ ...newConvData, cipher_type: cipherType, key: defaultKeys[cipherType] });
  };

  const renderKeyInput = () => {
    const { cipher_type, key } = newConvData;

    switch (cipher_type) {
      case 'caesar':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Shift</label>
            <input
              type="number"
              min="0"
              max="25"
              value={key.shift || 0}
              onChange={(e) => setNewConvData({ ...newConvData, key: { shift: parseInt(e.target.value) } })}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
            />
          </div>
        );

      case 'affine':
        return (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Key A</label>
              <input
                type="number"
                value={key.a || 1}
                onChange={(e) => setNewConvData({ ...newConvData, key: { ...key, a: parseInt(e.target.value) } })}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Key B</label>
              <input
                type="number"
                value={key.b || 0}
                onChange={(e) => setNewConvData({ ...newConvData, key: { ...key, b: parseInt(e.target.value) } })}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        );

      case 'hill':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Matrix (2×2 or 3×3)</label>
            <select
              value={key.matrix?.length || 2}
              onChange={(e) => {
                const size = parseInt(e.target.value);
                const defaultMatrix = size === 2 
                  ? [[3, 3], [2, 5]]
                  : [[6, 24, 1], [13, 16, 10], [20, 17, 15]];
                setNewConvData({ ...newConvData, key: { matrix: defaultMatrix } });
              }}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 mb-2"
            >
              <option value="2">2×2 Matrix</option>
              <option value="3">3×3 Matrix</option>
            </select>
            <textarea
              value={JSON.stringify(key.matrix || [[3, 3], [2, 5]])}
              onChange={(e) => {
                try {
                  const matrix = JSON.parse(e.target.value);
                  setNewConvData({ ...newConvData, key: { matrix } });
                } catch (err) {
                  // Invalid JSON, ignore
                }
              }}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 font-mono text-sm"
              rows="3"
              placeholder="[[3,3],[2,5]]"
            />
            <p className="text-xs text-gray-500 mt-1">Enter matrix as JSON array</p>
          </div>
        );

      case 'playfair':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Keyword</label>
            <input
              type="text"
              value={key.keyword || ''}
              onChange={(e) => setNewConvData({ ...newConvData, key: { keyword: e.target.value.toUpperCase() } })}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
              placeholder="MONARCHY"
            />
          </div>
        );

      default:
        return null;
    }
  };

  const getOtherUser = (conversation) => {
    if (!conversation || !currentUser?.id) {
      return { username: 'Unknown', email: '' };
    }
    if (conversation.user_a?.id === currentUser.id) {
      return conversation.user_b || { username: 'Unknown', email: '' };
    }
    return conversation.user_a || { username: 'Unknown', email: '' };
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Secure Messaging</h1>
            <p className="text-gray-600 mt-1">Exchange encrypted messages with other users</p>
          </div>
          <button
            onClick={() => setShowNewConversation(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
          >
            <span className="text-xl">+</span>
            New Conversation
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {/* Success Message */}
        {successMsg && (
          <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg mb-4">
            {successMsg}
          </div>
        )}

        {/* Loading State */}
        {loading && conversations.length === 0 && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-gray-600 mt-4">Loading conversations...</p>
          </div>
        )}

        <div className="grid grid-cols-3 gap-6">
          {/* Conversations List */}
          <div className="col-span-1 bg-white rounded-lg shadow">
            <div className="p-4 border-b">
              <h2 className="font-semibold text-gray-900">Conversations</h2>
            </div>
            <div className="divide-y max-h-[600px] overflow-y-auto">
              {!Array.isArray(conversations) || conversations.length === 0 ? (
                <div className="p-4 text-center text-gray-500">
                  {loading ? 'Loading conversations...' : 'No conversations yet'}
                </div>
              ) : (
                conversations.map((conv) => {
                  const otherUser = getOtherUser(conv);
                  return (
                    <div
                      key={conv.id}
                      className={`relative group ${
                        selectedConversation?.id === conv.id ? 'bg-blue-50' : ''
                      }`}
                    >
                      <button
                        onClick={() => setSelectedConversation(conv)}
                        className="w-full p-4 text-left hover:bg-gray-50 transition"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="font-medium text-gray-900">{otherUser.username}</div>
                            <div className="text-sm text-gray-500 capitalize">{conv.cipher_type} cipher</div>
                          </div>
                          {conv.is_intercepted && (
                            <span className="text-red-500 text-sm">⚠️</span>
                          )}
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          {conv.message_count} messages
                        </div>
                      </button>
                      
                      {/* Delete button - appears on hover */}
                      <button
                        onClick={(e) => handleDeleteConversation(conv.id, e)}
                        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-red-500 hover:bg-red-600 text-white text-xs px-2 py-1 rounded"
                        title="Delete conversation"
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Messages Area */}
          <div className="col-span-2 bg-white rounded-lg shadow flex flex-col" style={{ height: '600px' }}>
            {selectedConversation ? (
              <>
                {/* Header */}
                <div className="p-4 border-b">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="font-semibold text-gray-900">
                        {getOtherUser(selectedConversation).username}
                      </h2>
                      <p className="text-sm text-gray-500 capitalize">
                        {selectedConversation.cipher_type} cipher
                        {selectedConversation.is_intercepted && (
                          <span className="text-red-500 ml-2">⚠️ Under attack</span>
                        )}
                      </p>
                    </div>
                    <label className="flex items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={showSteps}
                        onChange={(e) => setShowSteps(e.target.checked)}
                        className="rounded"
                      />
                      Show encryption steps
                    </label>
                  </div>
                </div>

                {/* Messages */}
                <div className="flex-1 p-4 overflow-y-auto space-y-4">
                  {messages.length === 0 ? (
                    <div className="text-center text-gray-500 mt-8">
                      No messages yet. Start the conversation!
                    </div>
                  ) : (
                    messages.map((msg) => {
                      const isCurrentUser = msg.sender?.id === currentUser?.id;
                      return (
                        <div
                          key={msg.id}
                          className={`flex ${isCurrentUser ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-[70%] rounded-lg p-3 ${
                              isCurrentUser
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-100 text-gray-900'
                            } ${msg.was_intercepted ? 'border-2 border-red-500' : ''}`}
                          >
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-medium text-sm">{msg.sender?.username}</span>
                              {msg.was_intercepted && (
                                <span className="text-red-500 text-xs font-bold">
                                  ⚠️ INTERCEPTED
                                </span>
                              )}
                            </div>
                            
                            {/* Show ciphertext (encrypted message) */}
                            <div className="mb-2">
                              <div className="text-xs opacity-75 mb-1">Encrypted Message:</div>
                              <div className="font-mono text-sm bg-black bg-opacity-20 p-2 rounded">
                                {msg.ciphertext}
                              </div>
                            </div>
                            
                            {/* Decrypt button for receiver */}
                            {!isCurrentUser && !decryptedMessages[msg.id] && (
                              <button
                                onClick={() => handleDecryptMessage(msg)}
                                disabled={decryptingMessages[msg.id]}
                                className="mt-2 text-xs bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 disabled:opacity-50 flex items-center gap-1"
                              >
                                {decryptingMessages[msg.id] ? '🔓 Decrypting...' : '🔓 Decrypt Message'}
                              </button>
                            )}
                            
                            {/* Show decrypted message for receiver */}
                            {!isCurrentUser && decryptedMessages[msg.id] && (
                              <div className="mt-2">
                                <div className="text-xs opacity-75 mb-1">Decrypted Message:</div>
                                <div className="text-sm bg-green-50 p-2 rounded border border-green-200">
                                  {decryptedMessages[msg.id].plaintext}
                                </div>
                                {showSteps && decryptedMessages[msg.id].steps && decryptedMessages[msg.id].steps.length > 0 && (
                                  <details className="mt-2 text-xs">
                                    <summary className="cursor-pointer opacity-75">View decryption steps</summary>
                                    <ul className="mt-1 space-y-1 ml-4 list-disc">
                                      {decryptedMessages[msg.id].steps.map((step, idx) => (
                                        <li key={idx}>{step}</li>
                                      ))}
                                    </ul>
                                  </details>
                                )}
                              </div>
                            )}
                            
                            {/* Only show plaintext to sender for verification */}
                            {isCurrentUser && (
                              <div className="mb-2 opacity-60">
                                <div className="text-xs mb-1">Your original message:</div>
                                <div className="text-sm italic">{msg.plaintext}</div>
                              </div>
                            )}
                            
                            {/* Show attack warning if intercepted */}
                            {msg.was_intercepted && (
                              <div className="mt-2">
                                <div className="p-2 bg-red-500 bg-opacity-20 rounded text-xs mb-2">
                                  <strong>⚠️ Security Alert:</strong> This message was intercepted and may have been modified by an attacker!
                                </div>
                                
                                {/* Button to load attack details */}
                                {!attackDetails[msg.id] ? (
                                  <button
                                    onClick={() => loadAttackDetailsForMessage(msg.id)}
                                    disabled={loadingAttackDetails[msg.id]}
                                    className="text-xs bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 disabled:opacity-50"
                                  >
                                    {loadingAttackDetails[msg.id] ? 'Loading...' : '🔍 View Attack Details'}
                                  </button>
                                ) : (
                                  <details className="mt-2 border border-red-300 rounded p-2">
                                    <summary className="text-xs font-bold cursor-pointer text-red-700">
                                      🛡️ MITM Attack Information
                                    </summary>
                                    <div className="mt-2 space-y-2">
                                      <div className="text-xs">
                                        <strong>Attacker:</strong> {attackDetails[msg.id].attacker?.username}
                                      </div>
                                      <div className="text-xs">
                                        <strong>Attack Status:</strong>{' '}
                                        <span className={attackDetails[msg.id].success ? 'text-red-600 font-bold' : 'text-green-600'}>
                                          {attackDetails[msg.id].success ? '✓ SUCCESSFUL' : '✗ FAILED'}
                                        </span>
                                      </div>
                                      {attackDetails[msg.id].decrypted_plaintext && (
                                        <div className="text-xs">
                                          <strong>Decrypted by attacker:</strong> {attackDetails[msg.id].decrypted_plaintext}
                                        </div>
                                      )}
                                      {attackDetails[msg.id].modified_plaintext && (
                                        <div className="text-xs text-red-700">
                                          <strong>⚠️ Modified to:</strong> {attackDetails[msg.id].modified_plaintext}
                                        </div>
                                      )}
                                      {attackDetails[msg.id].attack_steps && attackDetails[msg.id].attack_steps.length > 0 && (
                                        <details className="mt-2">
                                          <summary className="text-xs cursor-pointer">View attack steps</summary>
                                          <div className="mt-2 text-xs font-mono whitespace-pre-wrap max-h-60 overflow-y-auto bg-black bg-opacity-10 p-2 rounded">
                                            {attackDetails[msg.id].attack_steps.join('\n')}
                                          </div>
                                        </details>
                                      )}
                                    </div>
                                  </details>
                                )}
                              </div>
                            )}
                            
                            {msg.encryption_steps && msg.encryption_steps.length > 0 && (
                              <details className="mt-2">
                                <summary className="text-xs opacity-75 cursor-pointer hover:opacity-100">
                                  🔐 View encryption steps
                                </summary>
                                <div className="mt-2 text-xs opacity-90 font-mono whitespace-pre-wrap max-h-40 overflow-y-auto bg-black bg-opacity-10 p-2 rounded">
                                  {msg.encryption_steps.join('\n')}
                                </div>
                              </details>
                            )}
                            <div className="text-xs opacity-75 mt-2">
                              {new Date(msg.timestamp).toLocaleString()}
                            </div>
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>

                {/* Input */}
                <form onSubmit={handleSendMessage} className="p-4 border-t">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      placeholder="Type your message..."
                      className="flex-1 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                      disabled={loading}
                    />
                    <button
                      type="submit"
                      disabled={loading || !newMessage.trim()}
                      className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                    >
                      {loading ? 'Sending...' : 'Send'}
                    </button>
                  </div>
                </form>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center text-gray-500">
                Select a conversation to start messaging
              </div>
            )}
          </div>
        </div>

        {/* New Conversation Modal */}
        {showNewConversation && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h2 className="text-xl font-bold mb-4">New Secure Conversation</h2>
              <form onSubmit={handleCreateConversation} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Chat with
                  </label>
                  <select
                    value={newConvData.user_b_id}
                    onChange={(e) => setNewConvData({ ...newConvData, user_b_id: e.target.value })}
                    className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select a user</option>
                    {users && users.length > 0 ? (
                      users.filter(u => u.id !== currentUser?.id).map((user) => (
                        <option key={user.id} value={user.id}>
                          {user.username} ({user.email})
                        </option>
                      ))
                    ) : (
                      <option disabled>
                        {loading ? 'Loading users...' : 'No users available'}
                      </option>
                    )}
                  </select>
                  {users.length === 0 && !loading && (
                    <p className="text-xs text-red-600 mt-1">
                      No other users found. Make sure you're logged in and other users exist.
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Encryption Cipher
                  </label>
                  <select
                    value={newConvData.cipher_type}
                    onChange={(e) => updateKeyForCipher(e.target.value)}
                    className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="caesar">Caesar Cipher</option>
                    <option value="affine">Affine Cipher</option>
                    <option value="hill">Hill Cipher (2×2 or 3×3)</option>
                    <option value="playfair">Playfair Cipher</option>
                  </select>
                </div>

                {renderKeyInput()}

                <div className="flex gap-2 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowNewConversation(false)}
                    className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50 transition"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                  >
                    {loading ? 'Creating...' : 'Create'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
