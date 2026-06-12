import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, X, Bot, User, Loader2, Sparkles, Trash2 } from 'lucide-react';

const INITIAL_MSG = {
  role: 'model',
  content: "Hi! I'm your ZEBRA AI Analyst 🦓\n\nI can help you understand the **Health Insurance Claim Prediction Model** — ask me about Gini scores, feature importance, training strategy, or how to interpret a specific risk prediction!",
  thoughts: [],
  suggestions: ['What is the Gini score?', 'Explain K-Fold stacking', 'What drives high risk claims?']
};

const ChatPanel = ({ onClose }) => {
  const [messages, setMessages] = useState([INITIAL_MSG]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef(null);
  const abortRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(scrollToBottom, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  }, [input]);

  const sendMessage = async (text) => {
    const msg = text || input;
    if (!msg.trim() || isStreaming) return;
    setInput('');
    setIsStreaming(true);

    const newUserMsg = { role: 'user', content: msg };
    const newModelMsg = { role: 'model', content: '', thoughts: [], suggestions: [] };

    setMessages(prev => [...prev, newUserMsg, newModelMsg]);

    // abort any previous stream
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const resp = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: msg,
          history: messages.map(m => ({ role: m.role, content: m.content })),
        }),
        signal: controller.signal,
      });

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // keep partial line

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data:')) continue;
          const raw = trimmed.slice(5).trim();
          if (raw === '[DONE]') { setIsStreaming(false); break; }
          if (!raw) continue;
          try {
            const parsed = JSON.parse(raw);
            setMessages(prev => {
              const updated = [...prev];
              const last = { ...updated[updated.length - 1] };
              if (parsed.type === 'THOUGHT') {
                last.thoughts = [...(last.thoughts || []), parsed.content];
              } else if (parsed.type === 'FINAL_RESPONSE') {
                last.content = (last.content || '') + parsed.content;
              } else if (parsed.type === 'SUGGESTION') {
                last.suggestions = [...(last.suggestions || []), parsed.content];
              }
              updated[updated.length - 1] = last;
              return updated;
            });
          } catch { /* skip parse errors */ }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        setMessages(prev => {
          const updated = [...prev];
          const last = { ...updated[updated.length - 1] };
          last.content = '**Error:** Could not reach the API. Make sure the backend is running on port 8000.';
          updated[updated.length - 1] = last;
          return updated;
        });
      }
    } finally {
      setIsStreaming(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const clearChat = () => { setMessages([INITIAL_MSG]); setInput(''); };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50 shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
            <Sparkles size={14} className="text-white" />
          </div>
          <div>
            <p className="text-sm font-bold text-zinc-950 dark:text-zinc-50 leading-none">ZEBRA AI Analyst</p>
            <p className="text-[10px] text-zinc-400 mt-0.5">Powered by Gemini</p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button onClick={clearChat} title="Clear chat" className="p-1.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg transition-colors">
            <Trash2 size={15} />
          </button>
          <button onClick={onClose} className="p-1.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg transition-colors">
            <X size={15} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-5">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-2.5 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
            {/* Avatar */}
            <div className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
              msg.role === 'user'
                ? 'bg-blue-500 text-white'
                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400'
            }`}>
              {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
            </div>

            <div className={`max-w-[86%] ${msg.role === 'user' ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
              {/* Thoughts */}
              {msg.role === 'model' && msg.thoughts?.length > 0 && (
                <div className="text-[10px] italic text-zinc-400 dark:text-zinc-500 border-l-2 border-zinc-200 dark:border-zinc-700 pl-2 flex items-center gap-1">
                  {isStreaming && idx === messages.length - 1 && <Loader2 size={9} className="animate-spin" />}
                  {msg.thoughts[msg.thoughts.length - 1]}
                </div>
              )}

              {/* Bubble */}
              {(msg.content || (isStreaming && idx === messages.length - 1 && msg.role === 'model')) && (
                <div className={`px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-sm'
                    : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 rounded-tl-sm'
                }`}>
                  {msg.role === 'user' ? (
                    <p>{msg.content}</p>
                  ) : msg.content ? (
                    <div className="prose prose-sm dark:prose-invert max-w-none [&>p]:mb-2 [&>ul]:mb-2 [&>ol]:mb-2 [&>h3]:font-bold [&>h3]:mb-1">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                    </div>
                  ) : (
                    <div className="flex gap-1 items-center py-0.5">
                      <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:0ms]"/>
                      <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:150ms]"/>
                      <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:300ms]"/>
                    </div>
                  )}
                </div>
              )}

              {/* Suggestions */}
              {msg.role === 'model' && msg.suggestions?.length > 0 && !isStreaming && idx === messages.length - 1 && (
                <div className="flex flex-col gap-1.5 mt-1 w-full">
                  {msg.suggestions.map((s, si) => (
                    <button
                      key={si}
                      onClick={() => sendMessage(s)}
                      className="text-left text-xs px-3 py-1.5 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-blue-600 dark:text-blue-400 rounded-xl hover:bg-blue-50 dark:hover:bg-blue-900/30 hover:border-blue-300 dark:hover:border-blue-700 transition-all"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="px-3 py-3 border-t border-zinc-100 dark:border-zinc-800 bg-white dark:bg-[#0c0c0f] shrink-0">
        <div className="flex items-end gap-2 bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-xl px-3 py-2 focus-within:ring-2 focus-within:ring-blue-500/40 focus-within:border-blue-400 transition-all">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Ask about the model…"
            rows={1}
            className="flex-1 bg-transparent resize-none text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none"
            style={{ maxHeight: 120 }}
          />
          <button
            onClick={() => sendMessage()}
            disabled={!input.trim() || isStreaming}
            className="p-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
          >
            {isStreaming ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
          </button>
        </div>
        <p className="text-[10px] text-zinc-300 dark:text-zinc-600 mt-1.5 text-center">Shift+Enter for newline · Enter to send</p>
      </div>
    </div>
  );
};

export default ChatPanel;
