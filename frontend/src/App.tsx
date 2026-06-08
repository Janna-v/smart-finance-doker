import { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import './App.css';

// Importiamo i nostri componenti separati
import SpesaForm from './components/SpesaForm';
import ListaSpese from './components/ListaSpese';
import GraficoSpese from './components/GraficoSpese';

type ReportItem = { categoria: string; totale: number; percentuale?: string };

function App() {
  const [spese, setSpese] = useState<any[]>([]);
  const [report, setReport] = useState<ReportItem[]>([]);
  
  const fetchReport = () => axios.get('http://127.0.0.1:8000/report').then(res => setReport(res.data));
  const fetchSpese = () => axios.get('http://127.0.0.1:8000/transazioni').then(res => { setSpese(res.data); fetchReport(); });
  
  const eliminaSpesa = async (id: number) => {
    if (window.confirm("Eliminare questa spesa?")) { await axios.delete(`http://127.0.0.1:8000/transazioni/${id}`); fetchSpese(); }
  };
  
  const modificaSpesa = async (s: any) => {
    const nuovoImporto = prompt("Nuovo importo:", s.importo);
    if (nuovoImporto) { await axios.patch(`http://127.0.0.1:8000/transazioni/${s.id}`, { importo: parseFloat(nuovoImporto) }); fetchSpese(); }
  };
  
  const saldoTotale = useMemo(() => {
    return spese.reduce((acc, s) => {
      return s.tipo === 'Entrata' ? acc + s.importo : acc - s.importo;
    }, 0);
  }, [spese]);
  
  useEffect(() => { fetchSpese(); }, []);
  
  const dataConPercentuali = useMemo(() => {
    const totaleComplessivo = report.reduce((sum, item) => sum + item.totale, 0);
    return report.map((item) => ({
      ...item,
      percentuale: totaleComplessivo > 0 ? ((item.totale / totaleComplessivo) * 100).toFixed(1) + "%" : "0%"
    }));
  }, [report]);
  
  return (
    <div style={{ padding: '20px' }}>
      
      {/* Box del Saldo */}
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
      
      <SpesaForm onSpesaAggiunta={fetchSpese} />
      
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

export default App;