import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LabelList } from 'recharts';
import type { ReportItem } from '../types'; // Importa l'interfaccia ReportItem
 // Importa l'interfaccia ReportItem

type GraficoSpeseProps = { data: ReportItem[] };

const GraficoSpese: React.FC<GraficoSpeseProps> = ({ data }) => {
  if (data.length === 0) return <p>Nessun dato per il grafico</p>;

  return (
    <div style={{ flex: 1 }}>
      <h2>Distribuzione (Rettangoli)</h2>
      <BarChart width={500} height={300} data={data} margin={{ top: 30, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip formatter={(value: number) => `${value}€`} />
        <Legend verticalAlign="top" wrapperStyle={{ lineHeight: '40px' }} />
        <Bar dataKey="total" fill="#03461f">
          <LabelList dataKey="percentage" position="top" />
        </Bar>
      </BarChart>
    </div>
  );
};

export default GraficoSpese;