// src/components/TopicChart.js
import React from 'react';

const TopicChart = ({ topics }) => {
  if (!topics || topics.length === 0) {
    return <p>No topics to display yet.</p>;
  }

  return (
    <div>
      <h3>Trending Topics (Keywords per Topic)</h3>
      <ul>
        {topics.map((topic, index) => (
          <li key={index}>
            <strong>Topic {index + 1}:</strong> {topic.keywords.join(', ')}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TopicChart;
