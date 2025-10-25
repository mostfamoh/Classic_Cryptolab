import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { exercisesAPI, ciphersAPI, attacksAPI } from '../services/api';
import { Shield, Lock, Target, BookOpen, TrendingUp } from 'lucide-react';

const Dashboard = () => {
  const { user, isStudent } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentHistory, setRecentHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (isStudent()) {
          const [statsRes, historyRes] = await Promise.all([
            exercisesAPI.getStudentStats(),
            ciphersAPI.getHistory({ limit: 5 }),
          ]);
          setStats(statsRes.data);
          setRecentHistory(historyRes.data.results || historyRes.data);
        } else {
          const historyRes = await ciphersAPI.getHistory({ limit: 5 });
          setRecentHistory(historyRes.data.results || historyRes.data);
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [isStudent]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.first_name || user?.username}!
        </h1>
        <p className="text-gray-600 mt-2">
          {isStudent()
            ? 'Continue learning about classical encryption algorithms'
            : 'Manage your cipher operations and experiments'}
        </p>
      </div>

      {/* Stats Cards */}
      {isStudent() && stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Exercises</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_exercises}</p>
              </div>
              <BookOpen className="h-12 w-12 text-blue-600" />
            </div>
          </div>

          <div className="card bg-gradient-to-br from-green-50 to-green-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Completed</p>
                <p className="text-3xl font-bold text-gray-900">{stats.completed_exercises}</p>
              </div>
              <TrendingUp className="h-12 w-12 text-green-600" />
            </div>
          </div>

          <div className="card bg-gradient-to-br from-purple-50 to-purple-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Score</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_score}</p>
              </div>
              <Target className="h-12 w-12 text-purple-600" />
            </div>
          </div>

          <div className="card bg-gradient-to-br from-orange-50 to-orange-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Average Score</p>
                <p className="text-3xl font-bold text-gray-900">{stats.average_score.toFixed(1)}%</p>
              </div>
              <Shield className="h-12 w-12 text-orange-600" />
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/ciphers"
            className="flex items-center space-x-3 p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
          >
            <Lock className="h-8 w-8 text-primary-600" />
            <div>
              <h3 className="font-semibold text-gray-900">Encrypt/Decrypt</h3>
              <p className="text-sm text-gray-600">Work with ciphers</p>
            </div>
          </a>

          <a
            href="/attacks"
            className="flex items-center space-x-3 p-4 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
          >
            <Target className="h-8 w-8 text-red-600" />
            <div>
              <h3 className="font-semibold text-gray-900">Run Attacks</h3>
              <p className="text-sm text-gray-600">Break ciphers</p>
            </div>
          </a>

          <a
            href="/exercises"
            className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
          >
            <BookOpen className="h-8 w-8 text-green-600" />
            <div>
              <h3 className="font-semibold text-gray-900">Exercises</h3>
              <p className="text-sm text-gray-600">Practice skills</p>
            </div>
          </a>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
        {recentHistory.length > 0 ? (
          <div className="space-y-3">
            {recentHistory.map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Lock className="h-5 w-5 text-gray-500" />
                  <div>
                    <p className="font-medium text-gray-900">
                      {item.operation} with {item.cipher_type}
                    </p>
                    <p className="text-sm text-gray-600">
                      {new Date(item.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                  {item.mode}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600 text-center py-8">No recent activity</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
