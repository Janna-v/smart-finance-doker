import React, { useState } from 'react';
import axios from 'axios';

type SpesaFormProps = { onSpesaAggiunta: () => void; };

const SpesaForm: React.FC<SpesaFormProps> = ({ onSpesaAggiunta }) => {
  const [descrizione, setDescrizione] = useState('');
  const [importo, setImporto] = useState('');
  const [categoria, setCategoria] = useState('Cibo');
  const [tipo, setTipo] = useState('Uscita'); // Nuovo stato per il tipo!

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8000/transazioni', {
      data: new Date().toISOString().split('T')[0],
      descrizione,
      importo: parseFloat(importo) || 0,
      categoria,
      tipo, // Inviamo anche il tipo
    }).then(() => {
      setDescrizione(''); setImporto(''); setCategoria('Cibo'); setTipo('Uscita');
      onSpesaAggiunta();
    });
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 20 }}>
      <input placeholder="Descrizione" value={descrizione} onChange={e => setDescrizione(e.target.value)} />
      <input placeholder="Importo" value={importo} onChange={e => setImporto(e.target.value)} />
      <select value={categoria} onChange={e => setCategoria(e.target.value)}>
        <option value="Cibo">Cibo</option><option value="Svago">Svago</option><option value="Casa">Casa</option>
      </select>
      {/* Menu a tendina per il tipo */}
      <select value={tipo} onChange={e => setTipo(e.target.value)}>
        <option value="Uscita">Uscita</option>
        <option value="Entrata">Entrata</option>
      </select>
      <button type="submit">Aggiungi</button>
    </form>
  );
};

export default SpesaForm;