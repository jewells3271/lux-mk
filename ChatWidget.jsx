import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, X, Send, Cpu, Database, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import './ChatWidget.css';

// Configuration - Stable deploy
const API_URL = "https://revolution-backend.vercel.app/api";
const SIDE_IMAGE = "https://companain.life/images/lux1.png";

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [userId, setUserId] = useState(localStorage.getItem('lux_user_id'));
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Greeting. I am Lux. How can I assist you in the revolution?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [tokenStats, setTokenStats] = useState({ count: 0, sidecar: 0, capacity: 0 });

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch token stats periodically if open
  useEffect(() => {
    if (isOpen) {
      fetchTokenStats();
    }
  }, [isOpen]);

  const fetchTokenStats = async () => {
    if (!userId) return;
    try {
      const response = await axios.get(`${API_URL}/tokens/${userId}`);
      setTokenStats({
        count: response.data.stream_tokens,
        sidecar: response.data.sidecar_tokens,
        capacity: response.data.capacity_pct
      });
    } catch (e) {
      console.error("Token Stats Error:", e);
    }
  };


  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        user_id: parseInt(userId),
        message: userMessage.content
      });

      const botMessage = { role: 'assistant', content: response.data.reply };
      setMessages(prev => [...prev, botMessage]);

      // Update tokens from response
      setTokenStats({
        count: response.data.token_count,
        sidecar: response.data.sidecar_tokens,
        capacity: response.data.capacity_pct
      });
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "[Connection Error] My connection to the Brain is disrupted." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="lux-widget-container">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="lux-chat-window"
          >
            {/* Side Image Panel */}
            <div className="lux-side-panel">
              <img src={SIDE_IMAGE} alt="Lux Sidecar" className="lux-side-img" />
            </div>

            {/* Main Chat Content */}
            <div className="lux-main-content">
              {/* Header */}
              <div className="lux-header">
                <div className="lux-header-left">
                  <div className="lux-avatar">
                    <Cpu size={20} color="#ff3131" />
                  </div>
                  <div>
                    <h3 className="lux-title">Lux</h3>
                    <span className="lux-status">
                      <span className="status-indicator active">
                        ● Memory Active ({tokenStats.capacity}%)
                      </span>
                    </span>
                  </div>
                </div>
                <div className="lux-header-right">
                  <button onClick={() => setIsOpen(false)} className="lux-icon-btn">
                    <X size={20} />
                  </button>
                </div>
              </div>

              {/* Messages Area */}
              <div className="lux-messages">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`lux-message ${msg.role}`}>
                    <div className="message-content">{msg.content}</div>
                  </div>
                ))}
                {isLoading && (
                  <div className="lux-message assistant">
                    <div className="typing-indicator">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="lux-input-area">
                {!userId ? (
                  <div className="lux-disconnect-msg">Identity not linked. Please use the Registry.</div>
                ) : (
                  <>
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      placeholder="Message Lux..."
                      disabled={isLoading}
                    />
                    <button onClick={handleSendMessage} disabled={isLoading || !input.trim()}>
                      <Send size={18} />
                    </button>
                  </>
                )}
              </div>

              {/* Footer with Tokens */}
              <div className="lux-footer">
                <div className="lux-token-ticker">
                  <span title="Main Stream Tokens (Reboot Threshold 85%)">
                    <Zap size={10} style={{ marginRight: 2 }} /> {tokenStats.count.toLocaleString()}
                  </span>
                  <span className="divider">|</span>
                  <span title="Sidecar Sifter Tokens (Excluded from Reboot)">
                    SC: {tokenStats.sidecar.toLocaleString()}
                  </span>
                </div>
                <div className="lux-authorized">Authorized by AI Revolution.</div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsOpen(!isOpen)}
        className="lux-float-btn"
      >
        <MessageSquare size={28} />
      </motion.button>
    </div>
  );
};

export default ChatWidget;
