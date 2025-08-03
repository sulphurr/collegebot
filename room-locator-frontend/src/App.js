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
<<<<<<< HEAD
      <div className="bg-white p-6 rounded-lg shadow-md w-96 text-center">
        <h1 className="text-2xl font-bold mb-6">Room Locator Chatbot</h1>
=======
      <div className="bg-white p-6 rounded-lg shadow-md w-96">
        <h1 className="text-xl font-bold mb-4 text-center">Room Locator Chatbot</h1>
>>>>>>> bf42b29b3b7bfee0ad8ae6cd2fb5bd03564054c6
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter room code or description"
<<<<<<< HEAD
          className="w-full p-3 border border-gray-300 rounded mb-4 text-center"
=======
          className="w-full p-2 border border-gray-300 rounded mb-4"
>>>>>>> bf42b29b3b7bfee0ad8ae6cd2fb5bd03564054c6
        />
        <button
          onClick={handleSearch}
          disabled={loading}
<<<<<<< HEAD
          className="w-full bg-blue-500 text-white py-3 rounded hover:bg-blue-600 transition"
=======
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
>>>>>>> bf42b29b3b7bfee0ad8ae6cd2fb5bd03564054c6
        >
          {loading ? 'Searching...' : 'Find Room'}
        </button>
        {response && (
<<<<<<< HEAD
          <div className="mt-6 p-4 bg-green-100 border border-green-500 rounded text-left">
=======
          <div className="mt-4 p-3 bg-green-100 border border-green-400 rounded">
>>>>>>> bf42b29b3b7bfee0ad8ae6cd2fb5bd03564054c6
            <p>{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
