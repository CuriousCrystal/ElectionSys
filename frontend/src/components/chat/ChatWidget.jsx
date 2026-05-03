import { useState } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import { chatAPI } from '../../api/apiService';

const quickTopics = [
  { label: 'How to register', prompt: 'How do I register to vote in the upcoming election?' },
  { label: 'How to vote', prompt: 'What are the steps to vote on election day?' },
  { label: 'Election timeline', prompt: 'Can you explain the election timeline and key dates?' },
  { label: 'Voter rights', prompt: 'What are my rights as a voter?' },
];

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message) => {
    if (!message.trim() || loading) return;
    const userMessage = message.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const res = await chatAPI.sendMessage(userMessage, 'web-session');
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }] );
    } finally {
      setLoading(false);
    }
  };

  const handleSend = () => sendMessage(input);

  const handleQuickTopic = (prompt) => sendMessage(prompt);

  if (!isOpen) {
    return (
      <button className="chat-bubble" onClick={() => setIsOpen(true)}>
        <MessageCircle size={24} />
      </button>
    );
  }

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h3>August - Election Process Guide</h3>
        <button onClick={() => setIsOpen(false)}>
          <X size={20} />
        </button>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <p>👋 Hi! I'm August, your election process guide.</p>
            <p>Ask me about registration, voting day steps, timelines, and voter rights.</p>
            <div className="quick-topics">
              {quickTopics.map((topic) => (
                <button
                  key={topic.label}
                  type="button"
                  className="quick-topic-btn"
                  onClick={() => handleQuickTopic(topic.prompt)}
                >
                  {topic.label}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'August'}:</strong>
            <p>{msg.content}</p>
          </div>
        ))}
        
        {loading && (
          <div className="chat-message assistant typing">
            <p>August is typing...</p>
          </div>
        )}
      </div>
      
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask about registration or voting..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}
