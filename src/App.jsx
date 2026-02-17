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
  const isEmbed = searchParams.get('mode') === 'embed';

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
