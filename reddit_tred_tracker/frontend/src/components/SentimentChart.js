import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts';

const SentimentChart = ({ summary }) => {
  if (!summary || summary.positive === undefined) {
    return <p>No sentiment data available.</p>;
  }

  const data = [
    { name: 'Positive', value: summary.positive },
    { name: 'Neutral', value: summary.neutral },
    { name: 'Negative', value: summary.negative }
  ];

  const COLORS = ['#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div>
      <h3>Sentiment Distribution</h3>
      <PieChart width={300} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
          fill="#8884d8"
          label
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
};

export default SentimentChart;
