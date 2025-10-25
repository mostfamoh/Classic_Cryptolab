import { useState, useEffect } from 'react';
import { exercisesAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { BookOpen, CheckCircle, Clock } from 'lucide-react';

const Exercises = () => {
  const { isStudent } = useAuth();
  const [exercises, setExercises] = useState([]);
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExercises();
  }, []);

  const fetchExercises = async () => {
    try {
      const response = await exercisesAPI.getExercises();
      setExercises(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching exercises:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await exercisesAPI.submitExercise({
        exercise: selectedExercise.id,
        answer,
      });
      alert('Exercise submitted successfully!');
      setAnswer('');
      setSelectedExercise(null);
      fetchExercises();
    } catch (error) {
      alert(error.response?.data?.error || 'Submission failed');
    }
  };

  if (loading) {
    return <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Exercises</h1>

      {!selectedExercise ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="card hover:shadow-lg transition-shadow cursor-pointer" onClick={() => setSelectedExercise(exercise)}>
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-bold text-lg text-gray-900">{exercise.title}</h3>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  exercise.difficulty === 'easy' ? 'bg-green-100 text-green-700' :
                  exercise.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-red-100 text-red-700'
                }`}>
                  {exercise.difficulty}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-3">{exercise.description.substring(0, 100)}...</p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">{exercise.cipher_type.toUpperCase()}</span>
                <span className="font-semibold text-primary-600">{exercise.points} pts</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card max-w-3xl mx-auto">
          <button onClick={() => setSelectedExercise(null)} className="text-primary-600 mb-4">← Back to exercises</button>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">{selectedExercise.title}</h2>
          <p className="text-gray-600 mb-4">{selectedExercise.description}</p>
          <div className="bg-gray-50 p-4 rounded-lg mb-4">
            <h3 className="font-semibold mb-2">Ciphertext:</h3>
            <p className="font-mono text-gray-800">{selectedExercise.ciphertext}</p>
          </div>
          
          {isStudent() && (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Your Answer:</label>
                <textarea
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  className="input-field"
                  rows="4"
                  placeholder="Enter the decrypted plaintext"
                  required
                />
              </div>
              <button type="submit" className="btn-primary w-full">Submit Answer</button>
            </form>
          )}
        </div>
      )}
    </div>
  );
};

export default Exercises;
