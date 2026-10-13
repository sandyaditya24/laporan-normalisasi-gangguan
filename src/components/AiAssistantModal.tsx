import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '../types';

interface AiAssistantModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AiAssistantModal: React.FC<AiAssistantModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg-init',
      sender: 'ai',
      text: 'Halo! Saya adalah Asisten AI Operasional untuk Sistem Manajemen PLTA Curug & PJT II. Silakan tanyakan hal seputar operasi PLTA, gardu induk 70 / 6,3 kV, gangguan, SOP normalisasi, checklist manuver, K3, atau informasi teknis Bendung Curug lainnya.',
      timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, loading]);

  if (!isOpen) return null;

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    const query = input.trim();
    if (!query || loading) return;

    const userMsg: ChatMessage = {
      id: 'msg-' + Date.now(),
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/ask-ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: query }),
      });

      const data = await response.json();

      if (response.ok && data.success !== false && data.answer) {
        const aiMsg: ChatMessage = {
          id: 'msg-ai-' + Date.now(),
          sender: 'ai',
          text: data.answer,
          timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, aiMsg]);
      } else {
        const errorMsg: ChatMessage = {
          id: 'msg-err-' + Date.now(),
          sender: 'ai',
          text: 'Maaf, terjadi kendala: ' + (data.error || 'Gagal memproses jawaban.'),
          timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMsg]);
      }
    } catch (err: any) {
      const fallbackMsg: ChatMessage = {
        id: 'msg-err-' + Date.now(),
        sender: 'ai',
        text: 'Terjadi gangguan jaringan ke server. Pastikan server aktif lalu coba kembali.',
        timestamp: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, fallbackMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center p-3"
      style={{
        zIndex: 1050,
        backgroundColor: 'rgba(7, 15, 30, 0.75)',
        backdropFilter: 'blur(8px)',
      }}
    >
      <div className="chat-wrapper w-100" style={{ maxWidth: '850px' }}>
        <div className="chat-card shadow-lg">
          <div className="chat-header d-flex justify-content-between align-items-center">
            <div>
              <h3 className="mb-0 fw-bold fs-4">
                <i className="fa-solid fa-robot me-2 text-info"></i> Asisten AI Q&amp;A Operasional
              </h3>
              <p className="mb-0 text-white-50 small mt-1">
                Konsultasi prosedur SOP, normalisasi, dan informasi teknis Bendung Curug
              </p>
            </div>
            <button
              type="button"
              className="btn btn-outline-light btn-sm px-3 rounded-pill fw-semibold"
              onClick={onClose}
            >
              <i className="fa-solid fa-xmark me-1"></i> Tutup
            </button>
          </div>

          <div className="chat-box" id="chatBox" ref={chatBoxRef}>
            {messages.map((m) => (
              <div key={m.id} className={`message ${m.sender}`}>
                <div className="bubble">
                  {m.text}
                  <div
                    className="small mt-1 text-end opacity-75"
                    style={{ fontSize: '0.7rem' }}
                  >
                    {m.timestamp}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="message ai">
                <div className="bubble">
                  <span className="spinner-border spinner-border-sm me-2 text-primary" role="status"></span>
                  Sedang memproses jawaban...
                </div>
              </div>
            )}
          </div>

          <div className="p-3 p-md-4 bg-white border-top">
            <form onSubmit={handleSend} className="d-flex gap-2">
              <input
                type="text"
                className="form-control form-control-lg fs-6"
                placeholder="Ketik pertanyaan operasional Anda di sini (misal: SOP Manuver Kosambi, K3)..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={loading}
                autoFocus
                required
              />
              <button
                type="submit"
                className="btn btn-primary px-4 btn-custom"
                disabled={loading || !input.trim()}
              >
                <i className="fa-solid fa-paper-plane me-1"></i> Kirim
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
