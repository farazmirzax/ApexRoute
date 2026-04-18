"use client"; // Required for React state and onClick events in Next.js App Router

import { useState } from "react";

export default function CommandCenter() {
  // State to hold our form inputs
  const [shipmentId, setShipmentId] = useState("REQ-774-ALPHA");
  const [currentLocation, setCurrentLocation] = useState("Miami Port");
  const [destination, setDestination] = useState("Rotterdam");

  // State to hold the API response and loading status
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // The function that talks to FastAPI
  const analyzeRoute = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze_route", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          shipment_id: shipmentId,
          current_location: currentLocation,
          destination: destination,
        }),
      });

      const data = await response.json();
      setResult(data.data); // Store the LangGraph state in our React state
    } catch (error) {
      console.error("Connection failed:", error);
      setResult({ error: "Failed to connect to Apex Route Engine." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-300 p-8 font-mono">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <h1 className="text-3xl font-bold text-white mb-2 tracking-widest">
          💀 APEX ROUTE <span className="text-emerald-500">COMMAND CENTER</span>
        </h1>
        <p className="text-slate-500 mb-8 border-b border-slate-800 pb-4">
          Autonomous Logistics AI // Team Requiem
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

          {/* Left Side: The Input Form */}
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-2xl">
            <h2 className="text-xl text-white mb-6">Initialize Scan</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-xs text-slate-500 mb-1 cursor-pointer">SHIPMENT ID</label>
                <input
                  type="text"
                  value={shipmentId}
                  onChange={(e) => setShipmentId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 p-2 text-emerald-400 focus:outline-none focus:border-emerald-500 rounded cursor-text"
                />
              </div>
              <div>
                <label className="block text-xs text-slate-500 mb-1 cursor-pointer">CURRENT COORDINATES</label>
                <input
                  type="text"
                  value={currentLocation}
                  onChange={(e) => setCurrentLocation(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 p-2 text-white focus:outline-none focus:border-emerald-500 rounded cursor-text"
                />
              </div>
              <div>
                <label className="block text-xs text-slate-500 mb-1 cursor-pointer">DESTINATION PORT</label>
                <input
                  type="text"
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 p-2 text-white focus:outline-none focus:border-emerald-500 rounded cursor-text"
                />
              </div>

              <button
                onClick={analyzeRoute}
                disabled={loading}
                className="w-full mt-6 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-4 rounded transition-all disabled:opacity-50 cursor-pointer disabled:cursor-not-allowed"
              >
                {loading ? "EXECUTING AI PROTOCOL..." : "ANALYZE ROUTE"}
              </button>
            </div>
          </div>

          {/* Right Side: The Output Screen */}
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-2xl relative overflow-hidden cursor-default">
            <h2 className="text-xl text-white mb-6">Live AI Telemetry</h2>

            {loading && (
              <div className="text-emerald-500 animate-pulse">
                [SYSTEM] Handshake established...<br />
                [AGENT] Scraping global intel...<br />
                [ORACLE] Calculating risk parameters...
              </div>
            )}

            {result && !result.error && (
              <div className="space-y-4 animate-in fade-in duration-500">
                <div className="p-3 bg-slate-950 border-l-2 border-slate-700">
                  <span className="text-slate-500 text-xs block mb-1">THREAT DETECTED:</span>
                  <span className="text-rose-400 text-sm">{result.news_data}</span>
                </div>

                <div className="p-3 bg-slate-950 border-l-2 border-slate-700">
                  <span className="text-slate-500 text-xs block mb-1">CALCULATED RISK LEVEL:</span>
                  {/* Dynamically color the risk level based on the float value */}
                  <span className={`text-2xl font-bold ${result.risk_level > 0.7 ? 'text-rose-500' : 'text-emerald-500'}`}>
                    {(result.risk_level * 100).toFixed(1)}%
                  </span>
                </div>

                <div className={`p-3 border rounded ${result.recommended_action ? 'bg-rose-950/30 border-rose-900' : 'bg-emerald-950/30 border-emerald-900'}`}>
                  <span className={`${result.recommended_action ? 'text-rose-500' : 'text-emerald-500'} text-xs block mb-1`}>
                    AGENTIC ACTION EXECUTED:
                  </span>
                  <span className="text-white text-sm leading-relaxed">
                    {result.recommended_action || "ROUTE CLEAR: No evasive maneuvers required. Proceed with standard logistics."}
                  </span>
                </div>
              </div>
            )}

            {result?.error && (
              <div className="text-rose-500">
                FATAL ERROR: {result.error}
              </div>
            )}
          </div>

        </div>
      </div>
    </main>
  );
}