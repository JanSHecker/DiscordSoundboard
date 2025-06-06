import React, { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:8000";

function App() {
  const [files, setFiles] = useState<FileList | null>(null);
  const [sounds, setSounds] = useState<string[]>([]);

  useEffect(() => {
    axios.get(`${API}/sounds`).then(res => setSounds(res.data));
  }, []);

  const upload = async () => {
    if (!files) return;
    const formData = new FormData();
    formData.append("file", files[0]);

    await axios.post(`${API}/upload`, formData);
    setFiles(null);

    const res = await axios.get(`${API}/sounds`);
    setSounds(res.data);
  };

  const play = async (name: string) => {
    const formData = new FormData();
    formData.append("name", name);
    await axios.post(`${API}/play`, formData);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Discord Soundboard</h1>

      <input type="file" onChange={(e) => setFiles(e.target.files)} />

      <button
        onClick={upload}
        className="ml-2 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>

      <ul className="mt-4">
        {sounds.map((s, i) => (
          <li key={i} className="my-2">
            {s}
            <button
              onClick={() => play(s)}
              className="ml-2 bg-green-500 text-white px-2 py-1 rounded"
            >
              ▶ Play
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
