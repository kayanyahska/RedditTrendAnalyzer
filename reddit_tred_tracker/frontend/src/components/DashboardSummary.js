// src/components/DashboardSummary.js
import React from 'react';

const DashboardSummary = ({ totalPosts, totalComments }) => {
  return (
    <div style={{ marginBottom: '20px' }}>
      <h3>Summary of Fetched Data</h3>
      <ul>
        <li><strong>Total Posts:</strong> {totalPosts}</li>
        <li><strong>Total Comments:</strong> {totalComments}</li>
      </ul>
    </div>
  );
};

export default DashboardSummary;