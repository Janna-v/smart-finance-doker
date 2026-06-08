import React from 'react';

type ListaSpeseProps = {
  spese: any[];
  onElimina: (id: number) => void;
  onModifica: (s: any) => void;
};

const ListaSpese: React.FC<ListaSpeseProps> = ({ spese, onElimina, onModifica }) => {
  return (
    <div style={{ flex: 1 }}>
      <h3>Elenco Spese</h3>
      {spese.map((s: any) => (
        <div key={s.id} style={{ marginBottom: 8, borderBottom: '1px solid rgb(38, 54, 148)' }}>
          {s.data} - {s.descrizione}: <strong>{s.importo}€</strong> ({s.tipo || 'Uscita'})
          <button onClick={() => onModifica(s)} style={{ marginLeft: 10, background: "green" }}>Modifica</button>
          <button onClick={() => onElimina(s.id)} style={{ marginLeft: 10, background: "red" }}>Elimina</button>
        </div>
      ))}
    </div>
  );
};

export default ListaSpese;