// src/components/ClusterChart.js
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const ClusterChart = ({ posts, clusters }) => {
  if (!clusters || !posts || clusters.length !== posts.length) {
    return <p>No clustering data available.</p>;
  }

  const clusterMap = {};

  clusters.forEach((clusterId, index) => {
    if (!clusterMap[clusterId]) {
      clusterMap[clusterId] = [];
    }
    clusterMap[clusterId].push(posts[index]);
  });

  const clusterData = Object.keys(clusterMap).map((clusterId) => ({
    cluster: `Cluster ${clusterId}`,
    count: clusterMap[clusterId].length,
  }));

  return (
    <div>
      <h3>Post Distribution by Cluster</h3>
      <BarChart width={500} height={300} data={clusterData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="cluster" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#8884d8" />
      </BarChart>
    </div>
  );
};

export default ClusterChart;