import React, { useState, useRef, useEffect } from 'react'
import { Send } from 'lucide-react';
import { useTranslation } from 'react-i18next';

function ChatboxWithMultilingual() {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: t('chatbot.welcome'),
      sender: 'bot',
      timestamp: new Date(),
      language: i18n.language
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null)

  // Update welcome message when language changes
  useEffect(() => {
    setMessages(prevMessages => {
      const updatedMessages = [...prevMessages];
      if (updatedMessages.length > 0 && updatedMessages[0].sender === 'bot') {
        updatedMessages[0].text = t('chatbot.welcome');
        updatedMessages[0].language = i18n.language;
      }
      return updatedMessages;
    });
  }, [i18n.language, t]);

  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
      language: i18n.language
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: inputMessage,
          language: i18n.language
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: messages.length + 2,
        text: data.answer || t('chatbot.noAnswer'),
        sender: 'bot',
        timestamp: new Date(),
        language: i18n.language,
        metadata: {
          source_language: data.source_language,
          target_language: data.target_language
        }
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: t('chatbot.error'),
        sender: 'bot',
        timestamp: new Date(),
        language: i18n.language
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="h-[70vh] flex flex-col bg-slate-800/50 rounded-xl border border-cyan-500/30 shadow-2xl shadow-cyan-500/10 backdrop-blur-sm">
      {/* Header */}
      <div className="p-4 border-b border-cyan-500/30 bg-gradient-to-r from-slate-800/80 to-slate-700/80 rounded-t-xl">
        <h2 className="text-xl font-semibold text-cyan-400 flex items-center space-x-2">
          <span>🛰️ {t('chatbot.title')}</span>
        </h2>
        <p className="text-xs text-cyan-300/70 mt-1">
          {t('navbar.language')}: {i18n.language.toUpperCase()}
        </p>
      </div>

      {/* Messages Container */}
      <div
        className="flex-1 overflow-y-auto p-4 space-y-4"
        style={{
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
        }}
        ref={messagesContainerRef}
      >
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${message.sender === 'user'
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg shadow-cyan-500/25'
                  : 'bg-slate-700/80 text-gray-100 border border-slate-600/50 shadow-lg'
                }`}
            >
              <p className="text-sm">{message.text}</p>
              <p className="text-xs opacity-60 mt-1">
                {message.timestamp.toLocaleTimeString()}
              </p>
              {message.metadata && (
                <p className="text-xs opacity-50 mt-1">
                  {message.metadata.source_language} → {message.metadata.target_language}
                </p>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-700/80 text-gray-100 border border-slate-600/50 px-4 py-2 rounded-lg">
              <p className="text-sm">{t('chatbot.loading')}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-cyan-500/30 bg-gradient-to-r from-slate-800/80 to-slate-700/80 rounded-b-xl">
        <div className="flex gap-3">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={t('chatbot.placeholder')}
            disabled={isLoading}
            className="flex-1 px-4 py-2 bg-slate-700/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500 transition-colors disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim()}
            className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg hover:from-cyan-600 hover:to-blue-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-cyan-500/25"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatboxWithMultilingual;
