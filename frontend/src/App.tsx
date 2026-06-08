import { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LabelList } from 'recharts';
import './App.css';

type SpesaFormProps = { onSpesaAggiunta?: () => void; };
type ReportItem = { categoria: string; totale: number; percentuale?: string };

const SpesaForm: React.FC<SpesaFormProps> = ({ onSpesaAggiunta }) => {
  const [descrizione, setDescrizione] = useState('');
  const [importo, setImporto] = useState('');
  const [categoria, setCategoria] = useState('Cibo');

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8000/transazioni', {
      data: new Date().toISOString().split('T')[0],
      descrizione,
      importo: parseFloat(importo) || 0,
      categoria,
    }).then(() => {
      setDescrizione(''); setImporto(''); setCategoria('Cibo');
      onSpesaAggiunta && onSpesaAggiunta();
    });
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 20 }}>
      <input placeholder="Descrizione" value={descrizione} onChange={e => setDescrizione(e.target.value)} />
      <input placeholder="Importo" value={importo} onChange={e => setImporto(e.target.value)} />
      <select value={categoria} onChange={e => setCategoria(e.target.value)}>
        <option value="Cibo">Cibo</option><option value="Svago">Svago</option><option value="Casa">Casa</option>
      </select>
      <button type="submit">Aggiungi</button>
    </form>
  );
};

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

  useEffect(() => { fetchSpese(); }, []);

  // Calcolo dati per il grafico (usiamo useMemo per ottimizzare)
  const dataConPercentuali = useMemo(() => {
    const totaleComplessivo = report.reduce((sum, item) => sum + item.totale, 0);
    return report.map((item) => ({
      ...item,
      percentuale: totaleComplessivo > 0 ? ((item.totale / totaleComplessivo) * 100).toFixed(1) + "%" : "0%"
    }));
  }, [report]);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Le mie Spese</h1>
      
      <SpesaForm onSpesaAggiunta={() => { fetchSpese(); }} />

      <div style={{ display: 'flex', gap: '50px', marginTop: '20px' }}>
        {/* Lista Spese */}
        <div style={{ flex: 1 }}>
          <h3>Elenco Spese</h3>
          {spese.map((s: any) => (
            <div key={s.id} style={{ marginBottom: 8, borderBottom: '1px solid #ccc' }}>
              {s.data} - {s.descrizione}: <strong>{s.importo}€</strong> ({s.categoria})
              <button onClick={() => modificaSpesa(s)} style={{ marginLeft: 10 }}>Modifica</button>
              <button onClick={() => eliminaSpesa(s.id)}>Elimina</button>
            </div>
          ))}
        </div>

        {/* Grafico */}
        <div style={{ flex: 1 }}>
          <h2>Distribuzione (Rettangoli)</h2>
          {report.length > 0 ? (
            <BarChart width={500} height={300} data={dataConPercentuali} margin={{ top: 30 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="categoria" />
              <YAxis />
              <Tooltip formatter={(value: number) => `${value}€`} />
              <Legend />
              <Bar dataKey="totale" fill="#8884d8">
                <LabelList dataKey="percentuale" position="top" />
              </Bar>
            </BarChart>
          ) : (
            <p>Nessun dato per il grafico</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;