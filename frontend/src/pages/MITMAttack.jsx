import { useState, useEffect } from 'react';
import { messagingAPI } from '../services/api';

export default function MITMAttack() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [interceptions, setInterceptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Attack form
  const [attackData, setAttackData] = useState({
    attacker_key: {},
    modified_plaintext: '',
    show_steps: true
  });

  useEffect(() => {
    loadConversations();
    loadInterceptions();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      loadMessages(selectedConversation.id);
    }
  }, [selectedConversation]);

  useEffect(() => {
    if (selectedConversation) {
      const defaultKeys = {
        caesar: { shift: 3 },
        affine: { a: 5, b: 8 },
        hill: { matrix: [[3, 3], [2, 5]] },
        playfair: { keyword: 'SECRET' }
      };
      setAttackData({
        ...attackData,
        attacker_key: defaultKeys[selectedConversation.cipher_type]
      });
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
      console.error('Failed to load conversations:', err);
      setConversations([]);
    } finally {
      setLoading(false);
    }
  };

  const loadMessages = async (conversationId) => {
    try {
      const response = await messagingAPI.getMessages(conversationId);
      // Handle both paginated response and direct array
      const msgData = response.data.results || response.data;
      setMessages(Array.isArray(msgData) ? msgData : []);
    } catch (err) {
      console.error('Failed to load messages:', err);
      setMessages([]);
    }
  };

  const loadInterceptions = async () => {
    try {
      const response = await messagingAPI.getInterceptions();
      // Handle both paginated response and direct array
      const intData = response.data.results || response.data;
      setInterceptions(Array.isArray(intData) ? intData : []);
    } catch (err) {
      console.error('Failed to load interceptions:', err);
      setInterceptions([]);
    }
  };

  const handleAttack = async (e) => {
    e.preventDefault();
    if (!selectedMessage) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await messagingAPI.performMITMAttack({
        message_id: selectedMessage.id,
        ...attackData
      });

      const result = response.data;
      setSuccess(result.success ? 'Attack successful! Message decrypted correctly.' : 'Attack failed. Wrong key.');
      setSelectedMessage(null);
      loadInterceptions();
      loadMessages(selectedConversation.id);
    } catch (err) {
      setError(err.response?.data?.error || 'Attack failed');
    } finally {
      setLoading(false);
    }
  };

  const renderKeyInput = () => {
    if (!selectedConversation) return null;

    const { cipher_type } = selectedConversation;
    const { attacker_key } = attackData;

    switch (cipher_type) {
      case 'caesar':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Guessed Shift</label>
            <input
              type="number"
              min="0"
              max="25"
              value={attacker_key.shift || 0}
              onChange={(e) => setAttackData({ ...attackData, attacker_key: { shift: parseInt(e.target.value) } })}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
            />
          </div>
        );

      case 'affine':
        return (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Guessed A</label>
              <input
                type="number"
                value={attacker_key.a || 1}
                onChange={(e) => setAttackData({ ...attackData, attacker_key: { ...attacker_key, a: parseInt(e.target.value) } })}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Guessed B</label>
              <input
                type="number"
                value={attacker_key.b || 0}
                onChange={(e) => setAttackData({ ...attackData, attacker_key: { ...attacker_key, b: parseInt(e.target.value) } })}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
              />
            </div>
          </div>
        );

      case 'hill':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Guessed Matrix</label>
            <textarea
              value={JSON.stringify(attacker_key.matrix || [[3, 3], [2, 5]])}
              onChange={(e) => {
                try {
                  const matrix = JSON.parse(e.target.value);
                  setAttackData({ ...attackData, attacker_key: { matrix } });
                } catch (err) {
                  // Invalid JSON
                }
              }}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500 font-mono text-sm"
              rows="3"
            />
          </div>
        );

      case 'playfair':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Guessed Keyword</label>
            <input
              type="text"
              value={attacker_key.keyword || ''}
              onChange={(e) => setAttackData({ ...attackData, attacker_key: { keyword: e.target.value.toUpperCase() } })}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
            />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">🕵️ Man-in-the-Middle Attack Simulator</h1>
          <p className="text-gray-600 mt-1">
            Intercept and decrypt encrypted messages (for educational purposes)
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
            {success}
          </div>
        )}

        <div className="grid grid-cols-2 gap-6 mb-8">
          {/* Attack Interface */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 text-red-600">🎯 Perform Attack</h2>

            <div className="space-y-4">
              {/* Select Conversation */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Target Conversation
                </label>
                <select
                  value={selectedConversation?.id || ''}
                  onChange={(e) => {
                    const conv = conversations.find(c => c.id === parseInt(e.target.value));
                    setSelectedConversation(conv);
                    setSelectedMessage(null);
                  }}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                >
                  <option value="">Select a conversation</option>
                  {conversations.map((conv) => (
                    <option key={conv.id} value={conv.id}>
                      {conv.user_a.username} ↔ {conv.user_b.username} ({conv.cipher_type})
                    </option>
                  ))}
                </select>
              </div>

              {/* Select Message */}
              {selectedConversation && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Target Message
                  </label>
                  <select
                    value={selectedMessage?.id || ''}
                    onChange={(e) => {
                      const msg = messages.find(m => m.id === parseInt(e.target.value));
                      setSelectedMessage(msg);
                    }}
                    className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                  >
                    <option value="">Select a message to intercept</option>
                    {messages.map((msg) => (
                      <option key={msg.id} value={msg.id}>
                        From {msg.sender.username} - {msg.ciphertext.substring(0, 30)}...
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* Show selected message */}
              {selectedMessage && (
                <div className="bg-gray-50 p-4 rounded border">
                  <div className="text-sm text-gray-600 mb-2">Intercepted Ciphertext:</div>
                  <div className="font-mono text-sm bg-white p-2 rounded border">
                    {selectedMessage.ciphertext}
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    Actual plaintext (hidden from attacker): {selectedMessage.plaintext}
                  </div>
                </div>
              )}

              {/* Attack Form */}
              {selectedMessage && (
                <form onSubmit={handleAttack} className="space-y-4">
                  <div className="border-t pt-4">
                    <h3 className="font-semibold mb-3">Guess the Key</h3>
                    {renderKeyInput()}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Modified Message (optional)
                    </label>
                    <input
                      type="text"
                      value={attackData.modified_plaintext}
                      onChange={(e) => setAttackData({ ...attackData, modified_plaintext: e.target.value })}
                      placeholder="Enter modified message to re-encrypt"
                      className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      If you guess the correct key, you can modify and re-encrypt the message
                    </p>
                  </div>

                  <label className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={attackData.show_steps}
                      onChange={(e) => setAttackData({ ...attackData, show_steps: e.target.checked })}
                      className="rounded"
                    />
                    Show attack steps
                  </label>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
                  >
                    {loading ? 'Attacking...' : '🚀 Launch Attack'}
                  </button>
                </form>
              )}
            </div>
          </div>

          {/* Recent Interceptions */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">📊 Attack History</h2>
            <div className="space-y-4 max-h-[600px] overflow-y-auto">
              {interceptions.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  No attacks recorded yet
                </div>
              ) : (
                interceptions.map((interception) => (
                  <div
                    key={interception.id}
                    className={`border rounded-lg p-4 ${
                      interception.success ? 'border-red-300 bg-red-50' : 'border-gray-300 bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">{interception.attacker.username}</span>
                        {interception.success ? (
                          <span className="text-red-600 text-sm">✅ Success</span>
                        ) : (
                          <span className="text-gray-600 text-sm">❌ Failed</span>
                        )}
                      </div>
                      <span className="text-xs text-gray-500">
                        {new Date(interception.timestamp).toLocaleString()}
                      </span>
                    </div>

                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="text-gray-600">Target:</span>{' '}
                        <span className="font-mono">
                          Message #{interception.original_message.id}
                        </span>
                      </div>
                      
                      <div>
                        <span className="text-gray-600">Decrypted:</span>{' '}
                        <span className={interception.success ? 'text-green-700 font-medium' : 'text-red-600'}>
                          {interception.decrypted_plaintext}
                        </span>
                      </div>

                      {interception.modified_plaintext && (
                        <div>
                          <span className="text-gray-600">Modified to:</span>{' '}
                          <span className="text-red-700 font-medium">
                            {interception.modified_plaintext}
                          </span>
                        </div>
                      )}

                      {interception.attack_steps && interception.attack_steps.length > 0 && (
                        <details className="mt-2">
                          <summary className="text-xs text-gray-600 cursor-pointer hover:text-gray-900">
                            View attack details
                          </summary>
                          <div className="mt-2 bg-white p-2 rounded border text-xs font-mono whitespace-pre-wrap max-h-60 overflow-y-auto">
                            {interception.attack_steps.join('\n')}
                          </div>
                        </details>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Educational Note */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 className="font-semibold text-yellow-900 mb-2">⚠️ Educational Purpose Only</h3>
          <p className="text-sm text-yellow-800">
            This tool demonstrates how man-in-the-middle attacks work against classical ciphers.
            It shows why key secrecy is crucial and why modern encryption methods are necessary.
            In real-world scenarios, such attacks are illegal and unethical.
          </p>
        </div>
      </div>
    </div>
  );
}
