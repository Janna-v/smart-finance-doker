import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api'; // Importiamo l'istanza configurata di Axios
import './../App.css'; // O '../App.css' in base a dove si trova la cartella components

import SpesaForm from './SpesaForm';
import ListaSpese from './ListaSpese'; 
import GraficoSpese from './GraficoSpese';
import type { Transaction, ReportItem } from '../types'; // Importa i tipi da types.ts
 // Importa i tipi da types.ts

export default function Dashboard() {
  const [spese, setSpese] = useState<Transaction[]>([]);
  const [report, setReport] = useState<ReportItem[]>([]);
  const navigate = useNavigate();

  // Controlliamo che l'intercettore possa mandare il token, 
  // altrimenti rimandiamo al login per sicurezza
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  // Sostituito axios.get con API.get (che aggiunge automaticamente l'header Authorization)
  const fetchReport = () => API.get('/transactions/summary').then(res => setReport(res.data));
  
  const fetchSpese = () => API.get('/transactions').then(res => { 
    setSpese(res.data); 
    fetchReport(); 
  });
  
  const eliminaSpesa = async (id: number) => {
    if (window.confirm("Eliminare questa spesa?")) { 
      await API.delete(`/transactions/${id}`); 
      fetchSpese(); 
    }
  };
  
  const modificaSpesa = async (s: Transaction) => {
    const nuovoImporto = prompt("Nuovo importo:", s.amount.toString());
    if (nuovoImporto) { 
      // Nota: sul backend la rotta put richiede il transaction_id
      await API.put(`/transactions/${s.id}`, { amount: parseFloat(nuovoImporto) }); 
      fetchSpese(); 
    }
  };
  
  const saldoTotale = useMemo(() => {
    return spese.reduce((acc, s) => {
      return s.type === 'Income' ? acc + s.amount : acc - s.amount;
    }, 0);
  }, [spese]);
  
  useEffect(() => { 
    fetchSpese(); 
  }, []);
  
  const dataConPercentuali = useMemo(() => {
    const totaleComplessivo = report.reduce((sum, item) => sum + item.total, 0);
    return report.map((item) => ({
      ...item,
      percentage: totaleComplessivo > 0 ? ((item.total / totaleComplessivo) * 100).toFixed(1) + "%" : "0%"
    }));
  }, [report]);
  
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ 
        padding: '20px', 
        backgroundColor: saldoTotale >= 0 ? '#099a7d' : '#075726', 
        borderRadius: '10px',
        marginBottom: '20px',
        border: '1px solid #ccc',
        textAlign: 'center'
      }}>
        <h2>Saldo Attuale: {saldoTotale.toFixed(2)}€</h2>
      </div>

      <h1>Le mie Spese</h1>
      
      <SpesaForm onExpenseAdded={fetchSpese} />
      
      <div style={{ display: 'flex', gap: '50px', marginTop: '20px' }}>
        <ListaSpese 
            spese={spese} 
            onElimina={eliminaSpesa} 
            onModifica={modificaSpesa} 
        />
        <GraficoSpese data={dataConPercentuali} />
      </div>
    </div>
  );
}