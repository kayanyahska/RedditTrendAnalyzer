// src/components/DomainInput.js
import React, { useState } from 'react';

const DomainInput = ({ onSubmit }) => {
  const [domain, setDomain] = useState('');
  const [days, setDays] = useState(7);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(domain, days);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
      <input
        type="text"
        placeholder="Enter domain (e.g. finance)"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Days"
        value={days}
        onChange={(e) => setDays(parseInt(e.target.value))}
        min="1"
        max="30"
        style={{ marginLeft: '10px' }}
      />
      <button type="submit" style={{ marginLeft: '10px' }}>
        Analyze
      </button>
    </form>
  );
};

export default DomainInput;
