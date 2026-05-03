import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/layout/Layout';
import DashboardPage from './pages/DashboardPage';
import BoothsPage from './pages/BoothsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import AlertsPage from './pages/AlertsPage';
import SettingsPage from './pages/SettingsPage';
import HelpPage from './pages/HelpPage';
import Login from './Login';
import ChatWidget from './components/chat/ChatWidget';

function PrivateRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <PrivateRoute>
              <Layout>
                <DashboardPage />
              </Layout>
            </PrivateRoute>
          } />
          <Route path="/booths" element={
            <PrivateRoute>
              <Layout>
                <BoothsPage />
              </Layout>
            </PrivateRoute>
          } />
          <Route path="/analytics" element={
            <PrivateRoute>
              <Layout>
                <AnalyticsPage />
              </Layout>
            </PrivateRoute>
          } />
          <Route path="/alerts" element={
            <PrivateRoute>
              <Layout>
                <AlertsPage />
              </Layout>
            </PrivateRoute>
          } />
          <Route path="/help" element={
            <PrivateRoute>
              <Layout>
                <HelpPage />
              </Layout>
            </PrivateRoute>
          } />
          <Route path="/settings" element={
            <PrivateRoute>
              <Layout>
                <SettingsPage />
              </Layout>
            </PrivateRoute>
          } />
        </Routes>
        <ChatWidget />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
