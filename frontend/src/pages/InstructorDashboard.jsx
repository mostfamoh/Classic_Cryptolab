import { useState, useEffect } from 'react';
import { exercisesAPI } from '../services/api';
import { Users, BookOpen, CheckCircle, TrendingUp } from 'lucide-react';

const InstructorDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await exercisesAPI.getInstructorDashboard();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center py-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Instructor Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Exercises</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_exercises || 0}</p>
            </div>
            <BookOpen className="h-12 w-12 text-blue-600" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-50 to-green-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Students</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.active_students || 0}</p>
            </div>
            <Users className="h-12 w-12 text-green-600" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-purple-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Submissions</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_submissions || 0}</p>
            </div>
            <CheckCircle className="h-12 w-12 text-purple-600" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-orange-50 to-orange-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg Score</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.average_score?.toFixed(1) || 0}%</p>
            </div>
            <TrendingUp className="h-12 w-12 text-orange-600" />
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Submissions</h2>
        {stats?.recent_submissions?.length > 0 ? (
          <div className="space-y-2">
            {stats.recent_submissions.map((sub) => (
              <div key={sub.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">{sub.student_name}</p>
                  <p className="text-sm text-gray-600">{sub.exercise_title}</p>
                </div>
                <div className="text-right">
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    sub.status === 'correct' ? 'bg-green-100 text-green-700' :
                    sub.status === 'incorrect' ? 'bg-red-100 text-red-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    {sub.status}
                  </span>
                  <p className="text-sm text-gray-600 mt-1">{sub.score} pts</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600 text-center py-8">No recent submissions</p>
        )}
      </div>
    </div>
  );
};

export default InstructorDashboard;
