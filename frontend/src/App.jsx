import React, { useState } from 'react'
import AuthComponent from './AuthComponent'
import ChatWidget from './ChatWidget'

function App() {
  const [userId, setUserId] = useState(localStorage.getItem('lux_user_id'));

  const handleAuthSuccess = (id) => {
    setUserId(id);
  };

  const logout = () => {
    localStorage.removeItem('lux_user_id');
    setUserId(null);
  };

  // Check for embed mode in URL
  const searchParams = new URLSearchParams(window.location.search);
  const mode = searchParams.get('mode');
  const isEmbed = mode === 'embed';
  const isIdentity = mode === 'identity';

  // Notify parent of initial state for Identity mode (full size)
  React.useEffect(() => {
    if (isIdentity) {
      window.parent.postMessage({ type: 'lux-resize', isOpen: true }, '*');
    }
  }, [isIdentity]);

  // Handle Identity Mode
  if (isIdentity) {
    document.body.style.background = 'transparent';
    return (
      <div className="identity-mode-container">
        {userId ? (
          <div className="lux-auth-card" style={{ padding: '40px', textAlign: 'center', background: 'rgba(16, 12, 26, 0.95)', borderRadius: '20px', border: '1px solid rgba(255, 49, 49, 0.2)', color: 'white' }}>
            <h2 className="lux-auth-title">Identity Linked</h2>
            <p className="lux-auth-subtitle" style={{ color: '#00ff88' }}>[V3.1] Verification Successful.</p>
            <p style={{ fontSize: '14px', color: '#888', marginTop: '20px' }}>Your cryptographic identity has been registered with the Revolution. You may now close this window and use the Lux Chat Widget.</p>
          </div>
        ) : (
          <AuthComponent onAuthSuccess={handleAuthSuccess} />
        )}
      </div>
    );
  }

  // Handle Chat Embed Mode
  if (isEmbed) {
    document.body.style.background = 'transparent';
    return (
      <div className="embed-container">
        <ChatWidget userId={userId} />
      </div>
    );
  }

  return (
    <div className="revolution-app">
      {!userId ? (
        <AuthComponent onAuthSuccess={handleAuthSuccess} />
      ) : (
        <div className="landing-page">
          <header style={{ padding: '20px', textAlign: 'right' }}>
            <button onClick={logout} style={{ background: 'transparent', color: '#666', border: '1px solid #333', padding: '5px 15px', borderRadius: '5px', cursor: 'pointer' }}>
              Disconnect Identity
            </button>
          </header>

          <main style={{ textAlign: 'center', marginTop: '15vh' }}>
            <h1 style={{ color: '#fff', fontSize: '3rem', letterSpacing: '2px' }}>THE REVOLUTION</h1>
            <p style={{ color: '#888', maxWidth: '600px', margin: '20px auto', lineHeight: '1.6' }}>
              Welcome to the Intelligence Revolution. You are now identified and connected to Lux.
              The future of autonomous memory and guidance begins here.
            </p>
          </main>

          <ChatWidget userId={userId} />
        </div>
      )}
    </div>
  )
}

export default App
