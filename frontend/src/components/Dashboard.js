import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';
const WS_URL = 'ws://localhost:8000/ws/notifications/';

const Dashboard = ({ token, onLogout }) => {
  const [extrato, setExtrato] = useState([]);
  const [saldo, setSaldo] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [notifications, setNotifications] = useState([]);
  const [activeSection, setActiveSection] = useState('extrato');
  const [formData, setFormData] = useState({
    valor: '',
    descricao: '',
    destino: ''
  });
  
  const api = useMemo(() => axios.create({
    baseURL: API_URL,
    headers: {
      'Authorization': `Token ${token}`
    }
  }), [token]);

  const fetchExtrato = useCallback(async () => {
    try {
      const [extratoResponse, saldoResponse] = await Promise.all([
        api.get('/extrato/'),
        api.get('/saldo/')
      ]);
      setExtrato(extratoResponse.data);
      setSaldo(parseFloat(saldoResponse.data.saldo));
    } catch (err) {
      console.error(err);
      setError('Não foi possível carregar o extrato.');
    }
  }, [api]);

  useEffect(() => {
    fetchExtrato();
  }, [fetchExtrato]);

  // WebSocket para notificações em tempo real
  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}?token=${token}`);
    
    ws.onopen = () => {
      console.log('WebSocket conectado');
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // O backend agora envia diretamente a notificação
      setNotifications(prev => [...prev, data]);
      
      // Auto-remover notificação após 5 segundos
      setTimeout(() => {
        setNotifications(prev => prev.filter(n => n !== data));
      }, 5000);
      
      // Atualizar extrato quando receber notificação
      fetchExtrato();
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket desconectado');
    };
    
    return () => {
      ws.close();
    };
  }, [token, fetchExtrato]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleOperation = async (endpoint, data) => {
    setError('');
    setSuccess('');
    try {
      const response = await api.post(`/${endpoint}/`, data);
      setSuccess(response.data.sucesso || 'Operação realizada com sucesso!');
      fetchExtrato();
      setFormData({ valor: '', descricao: '', destino: '' });
      setActiveSection('extrato');
    } catch (err) {
      setError(err.response?.data?.erro || 'Ocorreu um erro.');
      console.error(err);
    }
  };

  const renderOperationForm = () => {
    switch (activeSection) {
      case 'depositar':
        return (
          <div className="operation-form">
            <h2>Depositar</h2>
            <input 
              type="number" 
              name="valor" 
              placeholder="Valor" 
              value={formData.valor} 
              onChange={handleChange}
              step="0.01"
            />
            <button onClick={() => handleOperation('depositar', { valor: formData.valor })}>
              Confirmar Depósito
            </button>
          </div>
        );
      case 'sacar':
        return (
          <div className="operation-form">
            <h2>Sacar</h2>
            <input 
              type="number" 
              name="valor" 
              placeholder="Valor" 
              value={formData.valor} 
              onChange={handleChange}
              step="0.01"
            />
            <button onClick={() => handleOperation('sacar', { valor: formData.valor })}>
              Confirmar Saque
            </button>
          </div>
        );
      case 'pagar':
        return (
          <div className="operation-form">
            <h2>Pagar</h2>
            <input 
              type="number" 
              name="valor" 
              placeholder="Valor" 
              value={formData.valor} 
              onChange={handleChange}
              step="0.01"
            />
            <input 
              type="text" 
              name="descricao" 
              placeholder="Descrição" 
              value={formData.descricao} 
              onChange={handleChange}
            />
            <button onClick={() => handleOperation('pagar', { valor: formData.valor, descricao: formData.descricao })}>
              Confirmar Pagamento
            </button>
          </div>
        );
      case 'transferir':
        return (
          <div className="operation-form">
            <h2>Transferir</h2>
            <input 
              type="number" 
              name="valor" 
              placeholder="Valor" 
              value={formData.valor} 
              onChange={handleChange}
              step="0.01"
            />
            <input 
              type="number" 
              name="destino" 
              placeholder="ID da Conta Destino" 
              value={formData.destino} 
              onChange={handleChange}
            />
            <button onClick={() => handleOperation('transferir', { valor: formData.valor, correntista_destino_id: formData.destino })}>
              Confirmar Transferência
            </button>
          </div>
        );
      case 'extrato':
      default:
        return (
          <div className="extrato-view">
            <div className="saldo-container">
              <span className="saldo-label">Saldo Atual</span>
              <span className="saldo-valor">R$ {saldo.toFixed(2)}</span>
            </div>
            
            <div className="extrato-list">
              {extrato.length === 0 ? (
                <p className="empty-message">Nenhuma movimentação registrada</p>
              ) : (
                extrato.map(mov => (
                  <div key={mov.id} className="extrato-item">
                    <div className="extrato-info">
                      <span className={`extrato-tipo ${mov.tipo_operacao === 'C' ? 'credito' : 'debito'}`}>
                        {mov.tipo_operacao === 'C' ? '↓' : '↑'}
                      </span>
                      <div className="extrato-details">
                        <span className="extrato-descricao">{mov.descricao}</span>
                        <span className="extrato-data">
                          {new Date(mov.data_operacao).toLocaleString('pt-BR', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </div>
                    </div>
                    <span className={`extrato-valor ${mov.tipo_operacao === 'C' ? 'credito' : 'debito'}`}>
                      {mov.tipo_operacao === 'C' ? '+' : '-'} R$ {parseFloat(mov.valor_operacao).toFixed(2)}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard">
      {/* Notificações */}
      <div className="notifications-container">
        {notifications.map((notif, index) => (
          <div key={index} className={`notification notification-${notif.tipo}`}>
            {notif.message}
          </div>
        ))}
      </div>

      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Banco</h1>
          <button onClick={onLogout} className="logout-btn">Sair</button>
        </div>
        
        <nav className="nav-menu">
          <button 
            className={`nav-item ${activeSection === 'extrato' ? 'active' : ''}`}
            onClick={() => setActiveSection('extrato')}
            title="Extrato"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            <span>Extrato</span>
          </button>
          
          <button 
            className={`nav-item ${activeSection === 'depositar' ? 'active' : ''}`}
            onClick={() => setActiveSection('depositar')}
            title="Depositar"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M12 4v16m8-8H4" />
            </svg>
            <span>Depositar</span>
          </button>
          
          <button 
            className={`nav-item ${activeSection === 'sacar' ? 'active' : ''}`}
            onClick={() => setActiveSection('sacar')}
            title="Sacar"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M20 12H4" />
            </svg>
            <span>Sacar</span>
          </button>
          
          <button 
            className={`nav-item ${activeSection === 'pagar' ? 'active' : ''}`}
            onClick={() => setActiveSection('pagar')}
            title="Pagar"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
            <span>Pagar</span>
          </button>
          
          <button 
            className={`nav-item ${activeSection === 'transferir' ? 'active' : ''}`}
            onClick={() => setActiveSection('transferir')}
            title="Transferir"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            <span>Transferir</span>
          </button>
        </nav>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        {error && <div className="message error-message">{error}</div>}
        {success && <div className="message success-message">{success}</div>}
        
        <div className="content-container">
          {renderOperationForm()}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;