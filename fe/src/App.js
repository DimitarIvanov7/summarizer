import React, { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [method, setMethod] = useState("textrank");
  const [nSentences, setNSentences] = useState(3);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    setLoading(true);
    setResult(null);
    const res = await fetch("http://localhost:8000/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, method, n_sentences: Number(nSentences) }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <div className="bg-white shadow-md rounded p-6 w-full max-w-xl">
        <h1 className="text-2xl font-bold mb-4 text-center">
          Резюматор на Уикипедия статии
        </h1>
        <textarea
          className="w-full border rounded p-2 mb-4"
          rows={8}
          placeholder="Paste your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="flex items-center mb-4 gap-4">
          <label className="font-semibold">Алгоритъм:</label>
          <select
            className="border rounded p-1"
            value={method}
            onChange={(e) => setMethod(e.target.value)}
          >
            <option value="textrank">TextRank</option>
            <option value="lsa">LSA</option>
          </select>
          <label className="font-semibold ml-4">Брой на изречения:</label>
          <input
            type="number"
            min={1}
            className="border rounded p-1 w-16"
            value={nSentences}
            onChange={(e) => setNSentences(e.target.value)}
          />
        </div>
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
          onClick={handleSummarize}
          disabled={loading || !text.trim()}
        >
          {loading ? "Резюмиране..." : "Резюмирай"}
        </button>
        {result && (
          <div className="mt-6">
            <h2 className="text-lg font-bold mb-2">Резюме</h2>
            <div className="bg-gray-50 border rounded p-3 mb-4">
              {result.summary}
            </div>
            <h2 className="text-lg font-bold mb-2">Оценка</h2>
            <div className="space-y-2">
              {Object.entries(result.evaluation).map(([metric, vals]) => (
                <div key={metric} className="bg-gray-50 border rounded p-2">
                  <div className="font-semibold">{metric}</div>
                  <div className="text-sm">
                    Precision:{" "}
                    <span className="font-mono">
                      {vals.precision.toFixed(3)}
                    </span>
                    {" | "}
                    Recall:{" "}
                    <span className="font-mono">{vals.recall.toFixed(3)}</span>
                    {" | "}
                    F-measure:{" "}
                    <span className="font-mono">
                      {vals.f_measure.toFixed(3)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      <footer className="mt-8"></footer>
    </div>
  );
}

export default App;
