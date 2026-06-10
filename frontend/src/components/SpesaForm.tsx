import React, { useState } from 'react';
import API from '../api'; // Importa l'istanza API configurata

type ExpenseFormProps = { onExpenseAdded: () => void; };

const ExpenseForm: React.FC<ExpenseFormProps> = ({ onExpenseAdded }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [categoryId, setCategoryId] = useState(1);
  const [type, setType] = useState('Expense'); 

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
   API.post('/transactions', {
  date: new Date().toISOString().split('T')[0],
  description,
  amount: parseFloat(amount) || 0,
  category_id: categoryId,
  type,
    })
    .then(() => {
      setDescription(''); setAmount(''); setCategoryId(1); setType('Expense');
      onExpenseAdded();
    });
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 20 }}>
      <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
      <input placeholder="Amount" value={amount} onChange={e => setAmount(e.target.value)} />
      <select value={categoryId} onChange={e => setCategoryId(1)}>
       <option value="1">Food</option>
<option value="2">Home</option>
<option value="3">Leisure</option>
      </select>
      {/* Dropdown for type */}
      <select value={type} onChange={e => setType(e.target.value)}>
        <option value="Expense">Expense</option>
        <option value="Income">Income</option>
      </select>
      <button type="submit">Add</button>
    </form>
  );
};

export default ExpenseForm;