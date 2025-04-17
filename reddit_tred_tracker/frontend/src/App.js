import React, { useState } from 'react';
import axios from 'axios';
import DomainInput from './components/DomainInput';
import TopicChart from './components/TopicChart';
import SentimentChart from './components/SentimentChart';
import SubredditChart from './components/SubredditChart';
import DashboardSummary from './components/DashboardSummary';
import DownloadButtons from './components/DownloadButtons';
import RegressionCard from './components/RegressionCard';
import ClusterChart from './components/ClusterChart';
function App() {
  const [data, setData] = useState(null);
  const [subredditData, setSubredditData] = useState(null);

  const fetchAll = async (domain, days) => {
    try {
      const trendRes = await axios.post('http://localhost:8000/trending', { domain });
      const subredditRes = await axios.get(`http://localhost:8000/subreddit-activity/${domain}`);
      console.log("Trending response:", trendRes.data);
      console.log("Subreddit activity:", subredditRes.data);
      setData(trendRes.data);
      setSubredditData(subredditRes.data);
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>Reddit Trend Tracker</h1>
      <DomainInput onSubmit={fetchAll} />

      {data && (
        <>
          <DashboardSummary
            totalPosts={data.total_posts}
            totalComments={data.total_comments}
          />

          <TopicChart topics={data.topics} />
          <SentimentChart summary={data.sentiment_summary} />
          <ClusterChart posts={data.raw_posts} clusters={data.clusters} />
          <RegressionCard regression={data.regression} />
        </>
      )}

      {subredditData && (
        <>
          <SubredditChart data={subredditData} />
        </>
      )}

      {data && (
        <DownloadButtons
          posts={data.raw_posts}
          subredditActivity={subredditData}
        />
      )}
    </div>
  );
}

export default App;
