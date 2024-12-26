import { useState } from 'react';
import './App.css';

interface Trend {
  _id: string;
  IP: string;
  trends: string[];
  timestamp: number;
}

function App() {
  const [latestTrend, setLatestTrend] = useState<Trend | null>(null);
  const [isLoading, setIsLoading] = useState(false); // For showing the "Loading..." message
  const [isScriptRunning, setIsScriptRunning] = useState(false); // To prevent multiple API calls

  const fetchLatestData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5500/api/trending');
      if (!response.ok) throw new Error('Failed to fetch trending data');
      const data: Trend[] = await response.json();
      
      // Find the latest data by timestamp
      if (data && data.length > 0) {
        const latest = data.reduce((prev, current) =>
          prev.timestamp > current.timestamp ? prev : current
        );
        setLatestTrend(latest); // Update the state with the latest data
      } else {
        setLatestTrend(null); // No data available
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while fetching data. Please try again.');
    } finally {
      setIsLoading(false); // Hide the loading state
      setIsScriptRunning(false); // Allow the button to be clicked again
    }
  };

  const runScript = async () => {
    if (isScriptRunning) return; // Prevent multiple clicks
    setIsScriptRunning(true); // Mark the script as running
    setIsLoading(true); // Show the loading state

    try {
      const response = await fetch('http://127.0.0.1:5500/run_script');
      if (!response.ok) throw new Error('Failed to run the script');
      await response.json();

      // Fetch the latest data after the script has run successfully
      await fetchLatestData();
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while running the script. Please try again.');
    }
  };

  return (
    <div>
      <h1>Trending Topics from Twitter</h1>
      <button onClick={runScript} disabled={isScriptRunning}>
        {isScriptRunning ? 'Running Script...' : 'Click here to run the script'}
      </button>
      <div className="trending-list">
        <h2>Latest Trending Topics</h2>
        {isLoading ? (
          <p>Loading...</p>
        ) : latestTrend ? (
          <div className="latest-trend">
            <strong>IP Address:</strong> {latestTrend.IP}
            <br />
            <strong>Trending Topics:</strong>
            <ul>
              {latestTrend.trends.map((topic, idx) => (
                <li key={idx}>{topic}</li>
              ))}
            </ul>
            <strong>Timestamp:</strong> {new Date(latestTrend.timestamp * 1000).toLocaleString()}
          </div>
        ) : (
          <p>No trending topics found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
