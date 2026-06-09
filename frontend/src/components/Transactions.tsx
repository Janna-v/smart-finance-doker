import React, { useEffect, useState } from 'react';
import API from '../api';
import type { Transaction } from '../types'; // Importa l'interfaccia Transaction da types.ts
 // Importa l'interfaccia Transaction da types.ts

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await API.get<Transaction[]>('/transactions'); 
        setTransactions(response.data);
      } catch (err) {
        console.error("Errore di caricamento o non autorizzato", err);
      }
    };
    fetchTransactions();
  }, []);

  return (
    <div>
      <h3>Le mie transazioni</h3>
      <ul>
        {transactions.map((t) => (
          <li key={t.id}>{t.description} - {t.amount}€</li>
        ))}
      </ul>
    </div>
  );
}
