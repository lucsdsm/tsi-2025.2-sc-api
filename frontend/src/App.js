import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [token, setToken] = useState(null);

  // tenta pegar o token do localStorage ao iniciar
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const handleLogin = (newToken) => {
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
  };

  return (
    <div className="App">
      <main>
        {!token ? (
          <Login onLogin={handleLogin} />
        ) : (
          <Dashboard token={token} onLogout={handleLogout} />
        )}
      </main>
    </div>
  );
}

export default App;
