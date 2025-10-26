import { useState, useEffect } from 'react';
import { ciphersAPI } from '../services/api';
import { Lock, Key, History, Info } from 'lucide-react';

const Ciphers = () => {
  const [selectedCipher, setSelectedCipher] = useState('caesar');
  const [operation, setOperation] = useState('encrypt');
  const [text, setText] = useState('');
  const [key, setKey] = useState({});
  const [result, setResult] = useState('');
  const [steps, setSteps] = useState([]);
  const [showSteps, setShowSteps] = useState(true);
  const [cipherInfo, setCipherInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCipherInfo();
  }, [selectedCipher]);

  const fetchCipherInfo = async () => {
    try {
      const response = await ciphersAPI.getInfo(selectedCipher);
      setCipherInfo(response.data);
    } catch (error) {
      console.error('Error fetching cipher info:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSteps([]);
    try {
      const response = await ciphersAPI.operate({
        cipher_type: selectedCipher,
        operation,
        text,
        key,
        mode: 'preshared',
        log_operation: true,
        show_steps: showSteps,
      });
      setResult(response.data.result);
      if (response.data.steps) {
        setSteps(response.data.steps);
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Cipher Operations</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Form */}
        <div className="lg:col-span-2 card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cipher Type</label>
                <select
                  value={selectedCipher}
                  onChange={(e) => setSelectedCipher(e.target.value)}
                  className="input-field"
                >
                  <option value="caesar">Caesar</option>
                  <option value="affine">Affine</option>
                  <option value="hill">Hill (2×2 or 3×3)</option>
                  <option value="playfair">Playfair</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Operation</label>
                <select value={operation} onChange={(e) => setOperation(e.target.value)} className="input-field">
                  <option value="encrypt">Encrypt</option>
                  <option value="decrypt">Decrypt</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Input Text</label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="input-field"
                rows="4"
                placeholder="Enter text to encrypt/decrypt"
                required
              />
            </div>

            {/* Cipher-specific key inputs */}
            {selectedCipher === 'caesar' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Shift (0-25)</label>
                <input
                  type="number"
                  min="0"
                  max="25"
                  value={key.shift || 0}
                  onChange={(e) => setKey({ shift: parseInt(e.target.value) })}
                  className="input-field"
                  required
                />
              </div>
            )}

            {selectedCipher === 'affine' && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Key A (coprime with 26)</label>
                  <input
                    type="number"
                    value={key.a || 1}
                    onChange={(e) => setKey({ ...key, a: parseInt(e.target.value) })}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Key B (0-25)</label>
                  <input
                    type="number"
                    value={key.b || 0}
                    onChange={(e) => setKey({ ...key, b: parseInt(e.target.value) })}
                    className="input-field"
                    required
                  />
                </div>
              </div>
            )}

            {selectedCipher === 'hill' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Key Input Method</label>
                <select
                  value={key.inputMethod || 'text'}
                  onChange={(e) => {
                    const method = e.target.value;
                    if (method === 'text') {
                      setKey({ inputMethod: 'text', text_key: '' });
                    } else {
                      setKey({ inputMethod: 'matrix', matrix: [[3, 3], [2, 5]] });
                    }
                  }}
                  className="input-field mb-3"
                >
                  <option value="text">Text Key (Recommended)</option>
                  <option value="matrix">Matrix (Advanced)</option>
                </select>

                {key.inputMethod === 'text' ? (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Text Key</label>
                    <input
                      type="text"
                      value={key.text_key || ''}
                      onChange={(e) => setKey({ ...key, text_key: e.target.value.toUpperCase() })}
                      className="input-field"
                      placeholder="Enter key (e.g., HILL, CRYPTO)"
                      required
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      💡 Enter a text key (letters only). Examples: "HILL" for 2×2, "CRYPTOLAB" for 3×3.
                      The system will automatically generate a valid matrix and show all steps.
                    </p>
                  </div>
                ) : (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Matrix Size</label>
                    <select
                      value={key.matrix?.length || 2}
                      onChange={(e) => {
                        const size = parseInt(e.target.value);
                        const defaultMatrix = size === 2 
                          ? [[3, 3], [2, 5]]
                          : [[6, 24, 1], [13, 16, 10], [20, 17, 15]];
                        setKey({ ...key, matrix: defaultMatrix });
                      }}
                      className="input-field mb-2"
                    >
                      <option value="2">2×2 Matrix</option>
                      <option value="3">3×3 Matrix</option>
                    </select>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Key Matrix</label>
                    <textarea
                      value={JSON.stringify(key.matrix || [[3, 3], [2, 5]])}
                      onChange={(e) => {
                        try {
                          const matrix = JSON.parse(e.target.value);
                          setKey({ ...key, matrix });
                        } catch (err) {
                          // Invalid JSON
                        }
                      }}
                      className="input-field font-mono text-sm"
                      rows="3"
                      placeholder="[[3,3],[2,5]]"
                      required
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Enter matrix as JSON. Examples: 2×2: [[3,3],[2,5]] or 3×3: [[6,24,1],[13,16,10],[20,17,15]]
                    </p>
                  </div>
                )}
              </div>
            )}

            {selectedCipher === 'playfair' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Keyword</label>
                <input
                  type="text"
                  value={key.keyword || ''}
                  onChange={(e) => setKey({ keyword: e.target.value })}
                  className="input-field"
                  placeholder="Enter keyword"
                  required
                />
              </div>
            )}

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="show-steps"
                checked={showSteps}
                onChange={(e) => setShowSteps(e.target.checked)}
                className="rounded"
              />
              <label htmlFor="show-steps" className="text-sm text-gray-700">
                Show step-by-step encryption/decryption process
              </label>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Processing...' : `${operation.charAt(0).toUpperCase() + operation.slice(1)}`}
            </button>
          </form>

          {result && (
            <div className="mt-6 space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Result:</h3>
                <p className="font-mono text-gray-800 break-all">{result}</p>
              </div>

              {steps.length > 0 && (
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">📝 Step-by-Step Process:</h3>
                  <div className="font-mono text-sm text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
                    {steps.join('\n')}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Info Panel */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Info className="h-5 w-5 mr-2" />
            Cipher Information
          </h2>
          {cipherInfo && (
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-gray-900">{cipherInfo.name}</h3>
                <p className="text-sm text-gray-600 mt-1">{cipherInfo.description}</p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 text-sm">Key Type:</h4>
                <p className="text-sm text-gray-600">{cipherInfo.key_type}</p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 text-sm">Weaknesses:</h4>
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                  {cipherInfo.weaknesses.map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Ciphers;
