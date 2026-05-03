import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import HelpPage from './pages/HelpPage';
import ChatWidget from './components/chat/ChatWidget';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <Layout>
            <HelpPage />
          </Layout>
        } />
        <Route path="/help" element={
          <Layout>
            <HelpPage />
          </Layout>
        } />
      </Routes>
      <ChatWidget />
    </BrowserRouter>
  );
}

export default App;
