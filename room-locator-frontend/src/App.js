import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setResponse('');
    try {
      const res = await axios.get(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
      setResponse(res.data);
    } catch (error) {
      setResponse('Failed to fetch data. Make sure the backend is running.');
    }
    setLoading(false);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-96">
        <h1 className="text-xl font-bold mb-4 text-center">Room Locator Chatbot</h1>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter room code or description"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          {loading ? 'Searching...' : 'Find Room'}
        </button>
        {response && (
          <div className="mt-4 p-3 bg-green-100 border border-green-400 rounded">
            <p>{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
