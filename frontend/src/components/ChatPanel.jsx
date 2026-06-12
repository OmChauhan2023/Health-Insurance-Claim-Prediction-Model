import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, X, Bot, User, Loader2, Sparkles } from 'lucide-react';

const ChatPanel = ({ onClose }) => {
  const [messages, setMessages] = useState([
    { role: 'model', content: "Hi! I'm your AI Data Analyst. Ask me anything about the model's Gini score, feature importance, or specific patient risk factors.", thoughts: [] }
  ]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e, customMessage = null) => {
    if (e) e.preventDefault();
    const textToSend = customMessage || input;
    if (!textToSend.trim() || isStreaming) return;

    const userMessage = { role: 'user', content: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);

    const modelMessageIndex = messages.length + 1;
    setMessages((prev) => [
      ...prev,
      { role: 'model', content: '', thoughts: [], suggestions: [] }
    ]);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: textToSend,
          history: messages.map(m => ({ role: m.role, content: m.content }))
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.replace('data: ', '').trim();
              if (data === '[DONE]') {
                setIsStreaming(false);
                break;
              }
              if (!data) continue;

              try {
                const parsed = JSON.parse(data);
                setMessages((prev) => {
                  const updated = [...prev];
                  const currentModelMsg = updated[updated.length - 1];
                  
                  if (parsed.type === 'THOUGHT') {
                    currentModelMsg.thoughts.push(parsed.content);
                  } else if (parsed.type === 'FINAL_RESPONSE') {
                    currentModelMsg.content += parsed.content;
                  } else if (parsed.type === 'SUGGESTION') {
                    if (!currentModelMsg.suggestions) currentModelMsg.suggestions = [];
                    currentModelMsg.suggestions.push(parsed.content);
                  }
                  
                  return updated;
                });
              } catch (e) {
                console.error("Error parsing SSE JSON:", e, data);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      setIsStreaming(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-[#0c0c0f]">
      {/* Header */}
      <div className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 flex justify-between items-center bg-zinc-50 dark:bg-zinc-900/50">
        <div className="flex items-center gap-2">
          <Sparkles size={18} className="text-blue-500" />
          <h3 className="font-semibold text-zinc-950 dark:text-zinc-50 text-sm">AI Data Analyst</h3>
        </div>
        <button onClick={onClose} className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200">
          <X size={18} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/50 dark:text-blue-400' : 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400'}`}>
              {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>
            
            <div className={`max-w-[85%] ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-2' : 'rounded-2xl rounded-tl-sm px-1 py-1'}`}>
              
              {/* Thoughts Area (Only for model) */}
              {msg.role === 'model' && msg.thoughts && msg.thoughts.length > 0 && (
                <div className="mb-2 text-xs italic text-zinc-400 dark:text-zinc-500 border-l-2 border-zinc-200 dark:border-zinc-700 pl-2">
                  <span className="flex items-center gap-1"><Loader2 size={10} className="animate-spin" /> {msg.thoughts[msg.thoughts.length - 1]}</span>
                </div>
              )}

              {/* Markdown Content */}
              {msg.content && (
                <div className={`prose prose-sm dark:prose-invert max-w-none ${msg.role === 'user' ? 'text-white' : 'text-zinc-700 dark:text-zinc-300'}`}>
                   <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                </div>
              )}

              {/* Suggestions */}
              {msg.role === 'model' && msg.suggestions && msg.suggestions.length > 0 && !isStreaming && idx === messages.length - 1 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {msg.suggestions.map((sug, sIdx) => (
                    <button 
                      key={sIdx}
                      onClick={() => handleSubmit(null, sug)}
                      className="text-xs bg-blue-50 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/20 dark:text-blue-400 dark:hover:bg-blue-900/40 px-3 py-1.5 rounded-full transition-colors border border-blue-200 dark:border-blue-800/30"
                    >
                      {sug}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isStreaming && messages[messages.length-1].role === 'user' && (
             <div className="flex gap-3">
               <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400">
                  <Bot size={16} />
               </div>
               <div className="flex items-center gap-2 text-zinc-400">
                 <Loader2 size={16} className="animate-spin" />
                 <span className="text-xs italic">Thinking...</span>
               </div>
             </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 border-t border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0c0c0f]">
        <form onSubmit={handleSubmit} className="relative flex items-end">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about the model data..."
            className="w-full bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-xl pl-4 pr-12 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none max-h-32 text-zinc-950 dark:text-zinc-100 placeholder-zinc-400"
            rows="2"
          />
          <button 
            type="submit" 
            disabled={!input.trim() || isStreaming}
            className="absolute right-2 bottom-2 p-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;
