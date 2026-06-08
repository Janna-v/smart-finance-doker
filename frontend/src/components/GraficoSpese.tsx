import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LabelList } from 'recharts';

type GraficoSpeseProps = { data: any[] };

const GraficoSpese: React.FC<GraficoSpeseProps> = ({ data }) => {
  if (data.length === 0) return <p>Nessun dato per il grafico</p>;

  return (
    <div style={{ flex: 1 }}>
      <h2>Distribuzione (Rettangoli)</h2>
      <BarChart width={500} height={300} data={data} margin={{ top: 30 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="categoria" />
        <YAxis />
        <Tooltip formatter={(value: number) => `${value}€`} />
        <Legend />
        <Bar dataKey="totale" fill="#03461f">
          <LabelList dataKey="percentuale" position="top" />
        </Bar>
      </BarChart>
    </div>
  );
};

export default GraficoSpese;