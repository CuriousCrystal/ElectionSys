import { useState } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import { chatAPI } from '../../api/apiService';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = input.trim();
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
      }]);
    } finally {
      setLoading(false);
    }
  };

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
        <h3>August - Election Assistant</h3>
        <button onClick={() => setIsOpen(false)}>
          <X size={20} />
        </button>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <p>👋 Hi! I'm August, your election assistant.</p>
            <p>Ask me about booths, voter queues, or election management.</p>
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
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}
