import { useState } from 'react';
import axios from 'axios';

 function SpesaForm({ onSpesaAggiunta }: { onSpesaAggiunta: () => void }) {
  const [descrizione, setDescrizione] = useState('');
  const [importo, setImporto] = useState('');
  const [categoria, setCategoria] = useState('Cibo');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/transazioni', {
        data: new Date().toISOString().split('T')[0], // Data odierna
        descrizione,
        importo: parseFloat(importo),
        categoria
      });
      // Resetta il form e notifica la lista di aggiornarsi
      setDescrizione('');
      setImporto('');
      onSpesaAggiunta(); 
    } catch (err) {
      console.error("Errore nell'invio:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <input value={descrizione} onChange={e => setDescrizione(e.target.value)} placeholder="Descrizione" required />
      <input type="number" value={importo} onChange={e => setImporto(e.target.value)} placeholder="Importo" required />
      <select value={categoria} onChange={e => setCategoria(e.target.value)}>
        <option value="Cibo">Cibo</option>
        <option value="Svago">Svago</option>
        <option value="Casa">Casa</option>
      </select>
      <button type="submit">Aggiungi</button>
    </form>
  );
}

export default SpesaForm