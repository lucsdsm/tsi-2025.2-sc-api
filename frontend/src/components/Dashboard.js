import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Dashboard = ({ token, onLogout }) => {
  const [extrato, setExtrato] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
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
      const response = await api.get('/extrato/');
      setExtrato(response.data);
    } catch (err) {
      console.error(err);
      setError('Não foi possível carregar o extrato.');
    }
  }, [api]);

  useEffect(() => {
    fetchExtrato();
  }, [fetchExtrato]);

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
      fetchExtrato(); // atualiza o extrato
      setFormData({ valor: '', descricao: '', destino: '' }); // limpa o formulário
    } catch (err) {
      setError(err.response?.data?.erro || 'Ocorreu um erro.');
      console.error(err);
    }
  };

  return (
    <div>
      <button onClick={onLogout} className="logout-button">Sair</button>
      <h2>Dashboard</h2>

      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}
      
      <div className="operations-container">
        <div className="form-container">
            <h3>Operações</h3>
            <input type="number" name="valor" placeholder="Valor (ex: 50.00)" value={formData.valor} onChange={handleChange} />
            <input type="text" name="descricao" placeholder="Descrição (para pagamento)" value={formData.descricao} onChange={handleChange} />
            <input type="number" name="destino" placeholder="ID da Conta Destino (para transferência)" value={formData.destino} onChange={handleChange} />
            <div className="button-group">
                <button onClick={() => handleOperation('depositar', { valor: formData.valor })}>Depositar</button>
                <button onClick={() => handleOperation('sacar', { valor: formData.valor })}>Sacar</button>
                <button onClick={() => handleOperation('pagar', { valor: formData.valor, descricao: formData.descricao })}>Pagar</button>
                <button onClick={() => handleOperation('transferir', { valor: formData.valor, correntista_destino_id: formData.destino })}>Transferir</button>
            </div>
        </div>
      </div>
      
      <div className="extrato-container">
        <h3>Extrato</h3>
        <table>
          <thead>
            <tr>
              <th>Data</th>
              <th>Operação</th>
              <th>Descrição</th>
              <th>Valor (R$)</th>
            </tr>
          </thead>
          <tbody>
            {extrato.map(mov => (
              <tr key={mov.id}>
                <td>{new Date(mov.data_operacao).toLocaleString('pt-BR')}</td>
                <td className={mov.tipo_operacao_display === 'Crédito' ? 'credito' : 'debito'}>
                  {mov.tipo_operacao_display}
                </td>
                <td>{mov.descricao}</td>
                <td>{parseFloat(mov.valor_operacao).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
