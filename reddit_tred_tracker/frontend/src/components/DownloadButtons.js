// src/components/DownloadButtons.js
import React from 'react';

const downloadCSV = (filename, rows) => {
  const csvContent = [
    Object.keys(rows[0]).join(","),
    ...rows.map(row => Object.values(row).join(","))
  ].join("\n");

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const DownloadButtons = ({ posts, subredditActivity }) => {
  return (
    <div style={{ marginTop: '20px' }}>
      <h4>Download Fetched Data</h4>
      {posts?.length > 0 && (
        <button onClick={() => downloadCSV("reddit_posts.csv", posts)}>
          Download Posts CSV
        </button>
      )}
      {subredditActivity?.length > 0 && (
        <button onClick={() => downloadCSV("subreddit_activity.csv", subredditActivity)} style={{ marginLeft: '10px' }}>
          Download Subreddit Activity CSV
        </button>
      )}
    </div>
  );
};

export default DownloadButtons;
