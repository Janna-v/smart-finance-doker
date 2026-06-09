import React from 'react';
import type { Transaction } from '../types'; // Importa l'interfaccia Transaction da types.ts
 // Importa l'interfaccia Transaction da types.ts

type ListaSpeseProps = {
  spese: Transaction[];
  onElimina: (id: number) => void;
  onModifica: (s: Transaction) => void;
};

const ListaSpese: React.FC<ListaSpeseProps> = ({ spese, onElimina, onModifica }) => {
  return (
    <div style={{ flex: 1 }}>
      <h3>Elenco Spese</h3>
      {spese.map((s) => (
        <div key={s.id} style={{ marginBottom: 8, borderBottom: '1px solid rgb(38, 54, 148)' }}>
          {s.date} - {s.description}: <strong>{s.amount}€</strong> ({s.type})
          <button onClick={() => onModifica(s)} style={{ marginLeft: 10, background: "green" }}>Modifica</button>
          <button onClick={() => onElimina(s.id)} style={{ marginLeft: 10, background: "red" }}>Elimina</button>
        </div>
      ))}
    </div>
  );
};

export default ListaSpese;