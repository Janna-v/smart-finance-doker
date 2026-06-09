import React, { useState } from 'react';
import axios from 'axios';

type ExpenseFormProps = { onExpenseAdded: () => void; };

const ExpenseForm: React.FC<ExpenseFormProps> = ({ onExpenseAdded }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('Food');
  const [type, setType] = useState('Expense'); 

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8000/transactions', {
      date: new Date().toISOString().split('T')[0],
      description,
      amount: parseFloat(amount) || 0,
      category,
      type, 
    }).then(() => {
      setDescription(''); setAmount(''); setCategory('Food'); setType('Expense');
      onExpenseAdded();
    });
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 20 }}>
      <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
      <input placeholder="Amount" value={amount} onChange={e => setAmount(e.target.value)} />
      <select value={category} onChange={e => setCategory(e.target.value)}>
        <option value="Food">Food</option><option value="Leisure">Leisure</option><option value="Home">Home</option>
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