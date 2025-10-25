import { useState } from 'react';
import { attacksAPI } from '../services/api';
import { Target, Zap, BarChart } from 'lucide-react';

const Attacks = () => {
  const [selectedAttack, setSelectedAttack] = useState('caesar_brute');
  const [ciphertext, setCiphertext] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAttack = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);

    try {
      let response;
      if (selectedAttack === 'caesar_brute') {
        response = await attacksAPI.caesarBruteForce({ ciphertext });
        setResults(response.data.results.slice(0, 10));
      } else if (selectedAttack === 'frequency') {
        response = await attacksAPI.frequencyAnalysis({ text: ciphertext });
        setResults(response.data.analysis);
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Attack failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Cryptanalysis Attacks</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <form onSubmit={handleAttack} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Attack Type</label>
              <select
                value={selectedAttack}
                onChange={(e) => setSelectedAttack(e.target.value)}
                className="input-field"
              >
                <option value="caesar_brute">Caesar Brute Force</option>
                <option value="frequency">Frequency Analysis</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ciphertext</label>
              <textarea
                value={ciphertext}
                onChange={(e) => setCiphertext(e.target.value)}
                className="input-field"
                rows="4"
                placeholder="Enter encrypted text to analyze"
                required
              />
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center">
              <Target className="h-5 w-5 mr-2" />
              {loading ? 'Analyzing...' : 'Run Attack'}
            </button>
          </form>

          {results && selectedAttack === 'caesar_brute' && (
            <div className="mt-6">
              <h3 className="font-bold text-gray-900 mb-3">Top Results:</h3>
              <div className="space-y-2">
                {results.map((r, i) => (
                  <div key={i} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-1">
                      <span className="font-semibold">Shift {r.shift}</span>
                      <span className="text-sm text-gray-600">Score: {r.score.toFixed(2)}</span>
                    </div>
                    <p className="font-mono text-sm text-gray-700">{r.decrypted_text}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {results && selectedAttack === 'frequency' && (
            <div className="mt-6">
              <h3 className="font-bold text-gray-900 mb-3">Frequency Analysis:</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-sm mb-2">Most Common Letters:</h4>
                  <div className="grid grid-cols-5 gap-2">
                    {results.most_common.map((item, i) => (
                      <div key={i} className="p-2 bg-primary-50 rounded text-center">
                        <div className="font-bold text-primary-700">{item.letter}</div>
                        <div className="text-xs text-gray-600">{item.frequency}%</div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-sm">
                    <strong>Total Letters:</strong> {results.total_letters}
                  </p>
                  <p className="text-sm">
                    <strong>Chi-Squared:</strong> {results.chi_squared}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Attack Guide</h2>
          <div className="space-y-3 text-sm text-gray-600">
            <p>
              <strong>Caesar Brute Force:</strong> Tries all 26 possible shifts and ranks results by English letter
              frequency.
            </p>
            <p>
              <strong>Frequency Analysis:</strong> Analyzes letter frequencies and compares with typical English text.
            </p>
            <p className="text-xs text-gray-500 mt-4">
              💡 Tip: Longer ciphertexts produce more accurate frequency analysis results.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Attacks;
