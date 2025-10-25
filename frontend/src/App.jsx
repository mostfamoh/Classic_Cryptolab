import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Ciphers from './pages/Ciphers';
import Attacks from './pages/Attacks';
import Exercises from './pages/Exercises';
import InstructorDashboard from './pages/InstructorDashboard';
import Messaging from './pages/Messaging';
import MITMAttack from './pages/MITMAttack';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route element={<Layout />}>
            <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/ciphers" element={<ProtectedRoute><Ciphers /></ProtectedRoute>} />
            <Route path="/attacks" element={<ProtectedRoute><Attacks /></ProtectedRoute>} />
            <Route path="/exercises" element={<ProtectedRoute><Exercises /></ProtectedRoute>} />
            <Route path="/messaging" element={<ProtectedRoute><Messaging /></ProtectedRoute>} />
            <Route path="/mitm-attack" element={<ProtectedRoute><MITMAttack /></ProtectedRoute>} />
            <Route path="/instructor" element={<ProtectedRoute requireInstructor><InstructorDashboard /></ProtectedRoute>} />
          </Route>
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
