import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post('/auth/register', { email, password });
      alert('Registrazione avvenuta con successo! Ora puoi effettuare il login.');
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Errore durante la registrazione');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '50px auto', textAlign: 'center' }}>
      <h2>Registrati</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleRegister}>
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          required 
          style={{ display: 'block', width: '100%', padding: 10, margin: '10px 0' }}
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
          style={{ display: 'block', width: '100%', padding: 10, margin: '10px 0' }}
        />
        <button type="submit" style={{ padding: 10, width: '100%' }}>Registrati</button>
      </form>
    </div>
  );
}