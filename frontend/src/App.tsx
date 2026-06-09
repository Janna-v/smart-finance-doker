import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard.tsx';
import Transactions from './components/Transactions'; 

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/transactions" element={<Transactions />} /> {/* Add this route */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* Se l'utente va alla radice "/", lo mandiamo al login */}
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}