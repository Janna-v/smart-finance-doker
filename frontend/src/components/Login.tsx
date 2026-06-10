import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';

export default function Login() {
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [error, setError] = useState('');
const navigate = useNavigate();

const handleLogin = async (e: React.FormEvent) => {
e.preventDefault();

try {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await API.post(
    '/auth/token',
    formData,
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );

  localStorage.setItem(
    'token',
    response.data.access_token
  );

  navigate('/dashboard');
} catch (err) {
  console.error(err);
  setError('Credenziali non valide o errore del server');
}

};

return (
<div
style={{
maxWidth: 400,
margin: '50px auto',
textAlign: 'center',
}}
>
Login

  {error && (
    <p style={{ color: 'red' }}>
      {error}
    </p>
  )}

  <form onSubmit={handleLogin}>
    <input
      type="email"
      placeholder="Email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      required
      style={{
        display: 'block',
        width: '100%',
        padding: 10,
        margin: '10px 0',
      }}
    />

    <input
      type="password"
      placeholder="Password"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      required
      style={{
        display: 'block',
        width: '100%',
        padding: 10,
        margin: '10px 0',
      }}
    />

    <button
      type="submit"
      style={{
        padding: 10,
        width: '100%',
      }}
    >
      Accedi
    </button>
  </form>
</div>

);
}