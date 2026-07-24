import React, { useState, useRef, useEffect } from 'react';

const ChatBox = () => {
    const [messages, setMessages] = useState([
        { text: "Hello! I am your AI Privacy Auditor. Ask me any questions about your confidential documents.", isUser: false }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const endOfMessagesRef = useRef(null);

    const scrollToBottom = () => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { text: userMsg, isUser: true }]);
        setLoading(true);

        try {
            const token = localStorage.getItem('token');
            const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
            const response = await fetch(`${apiBase}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ query: userMsg })
            });

            if (!response.ok) throw new Error('Chat failed');

            const data = await response.json();
            setMessages(prev => [...prev, { text: data.response, isUser: false, contextFound: data.context_found }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { text: "Sorry, I couldn't reach the chat service.", isUser: false, isError: true }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[500px] bg-white border border-slate-200 rounded-2xl overflow-hidden mt-6 shadow-sm">
            <div className="bg-slate-50 p-4 border-b border-slate-200">
                <h3 className="text-lg font-bold text-slate-800 flex items-center">
                    <svg className="w-5 h-5 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    Auditor Chat (RAG)
                </h3>
            </div>
            
            <div className="flex-1 p-4 overflow-y-auto space-y-4 bg-white">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-3.5 rounded-2xl shadow-sm ${msg.isUser ? 'bg-indigo-600 text-white rounded-br-none' : msg.isError ? 'bg-red-50 text-red-700 rounded-bl-none border border-red-100' : 'bg-slate-100 text-slate-700 rounded-bl-none border border-slate-200'}`}>
                            <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.text}</p>
                            {msg.contextFound && (
                                <p className="text-[10px] text-indigo-400 mt-2 font-bold uppercase tracking-wider">🔍 Context Matched</p>
                            )}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-slate-100 text-slate-400 p-4 rounded-2xl rounded-bl-none border border-slate-200 text-sm flex items-center space-x-2 shadow-sm">
                            <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
                            <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></span>
                            <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></span>
                        </div>
                    </div>
                )}
                <div ref={endOfMessagesRef} />
            </div>

            <form onSubmit={handleSend} className="p-4 bg-slate-50 border-t border-slate-200 flex space-x-3">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about your data..."
                    className="flex-1 bg-white border border-slate-300 rounded-xl px-4 py-2.5 text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent shadow-sm transition-all"
                    disabled={loading}
                />
                <button 
                    type="submit" 
                    disabled={loading || !input.trim()}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2.5 rounded-xl font-semibold shadow-sm transition-all disabled:opacity-50 disabled:hover:bg-indigo-600"
                >
                    Send
                </button>
            </form>
        </div>
    );
};

export default ChatBox;
