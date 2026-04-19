"use client"; // Required for React state and onClick events in Next.js App Router

import { useState } from "react";
import dynamic from "next/dynamic";

// Dynamically import the map to prevent Next.js SSR crashes
const TacticalMap = dynamic(() => import("./components/Map"), {
  ssr: false,
  loading: () => <div className="w-full h-[400px] bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-center text-slate-500 animate-pulse">BOOTING SATELLITE UPLINK...</div>
});

export default function CommandCenter() {
  // State to hold our form inputs
  const [shipmentId, setShipmentId] = useState("REQ-774-ALPHA");
  const [currentLocation, setCurrentLocation] = useState("Lucknow");
  const [destination, setDestination] = useState("Gaza");

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
          📍 APEX ROUTE <span className="text-emerald-500">COMMAND CENTER</span>
        </h1>
        <p className="text-slate-500 mb-8 border-b border-slate-800 pb-4">
          Autonomous Logistics AI // Team Requiem
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

          {/* Left Side: Inputs + Map */}
          <div className="space-y-8">
            
            {/* The Input Form */}
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

            {/* THE NEW TACTICAL MAP */}
            <div className="bg-slate-900 border border-slate-800 p-2 rounded-lg shadow-2xl">
               <TacticalMap 
                  isRerouted={result?.risk_level >= 0.7} 
                  coordinates={result?.route_coordinates} 
               />
            </div>

          </div>

          {/* Right Side: The Output Screen */}
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg shadow-2xl relative overflow-hidden cursor-default h-fit">
            <h2 className="text-xl text-white mb-6">Live AI Telemetry</h2>

            {loading && (
              <div className="text-emerald-500 animate-pulse">
                [SYSTEM] Handshake established...<br />
                [AGENT] Scraping global intel...<br />
                [ORACLE] Calculating risk parameters...
              </div>
            )}

            {result && !result.error && (
              <div className="space-y-6 animate-in fade-in duration-500">
                
                {/* 1. UPGRADED THREAT INTELLIGENCE */}
                <div className="p-4 bg-slate-950 border-l-2 border-rose-900 rounded-r-md shadow-inner">
                  <span className="text-slate-500 text-xs block mb-3 font-semibold tracking-wider">
                    THREAT INTELLIGENCE DETECTED:
                  </span>
                  <ul className="space-y-3">
                    {result.news_data?.replace("Recent Intel: ", "").split("|").map((headline: string, idx: number) => {
                      const cleanHeadline = headline.replace("HEADLINE:", "").trim();
                      if (!cleanHeadline) return null;
                      return (
                        <li key={idx} className="text-rose-400 text-sm flex items-start leading-snug">
                          <span className="mr-2 mt-1.5 w-1.5 h-1.5 bg-rose-500 rounded-full flex-shrink-0 shadow-[0_0_8px_rgba(244,63,94,0.8)]"></span>
                          <span>{cleanHeadline}</span>
                        </li>
                      );
                    })}
                  </ul>
                </div>
                
                {/* 2. THE RISK GAUGE */}
                <div className="p-4 bg-slate-950 border-l-2 border-slate-700 rounded-r-md">
                  <span className="text-slate-500 text-xs block mb-1 font-semibold tracking-wider">
                    CALCULATED RISK LEVEL:
                  </span>
                  <span className={`text-4xl font-black tracking-tighter ${result.risk_level >= 0.7 ? 'text-rose-500 drop-shadow-[0_0_10px_rgba(244,63,94,0.4)]' : 'text-emerald-500 drop-shadow-[0_0_10px_rgba(16,185,129,0.4)]'}`}>
                    {(result.risk_level * 100).toFixed(1)}%
                  </span>
                </div>

                {/* 3. UPGRADED AGENTIC ACTION (THE TACTICAL GRID) */}
                {result.recommended_action ? (
                  <div className="p-5 bg-rose-950/20 border border-rose-900/50 rounded-lg backdrop-blur-sm">
                    <span className="text-rose-500 text-xs block mb-3 font-semibold tracking-wider flex items-center">
                      <span className="w-2 h-2 bg-rose-500 animate-pulse rounded-full mr-2"></span>
                      EVASIVE MANEUVER EXECUTED
                    </span>
                    
                    <div className="text-white text-sm leading-relaxed">
                      <p className="font-medium text-rose-100 mb-4 pb-4 border-b border-rose-900/40">
                        {result.recommended_action.split('. ')[0].replace(/^(REROUTE INITIATED:\s*|ALTERNATIVE ROUTE LOCKED:\s*)+/g, '')}
                      </p>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-slate-950/50 p-3 rounded border border-rose-900/30">
                          <span className="block text-[10px] text-rose-500/70 uppercase font-bold tracking-widest mb-1">New Distance</span>
                          <span className="font-mono text-lg text-rose-200">
                            {/* Force it to just grab the numbers, append 'km' manually */}
                            {result.recommended_action.match(/Distance:\s*([\d\.]+)/)?.[1] || "--"} <span className="text-sm text-rose-400/70">km</span>
                          </span>
                        </div>
                        <div className="bg-slate-950/50 p-3 rounded border border-rose-900/30">
                          <span className="block text-[10px] text-rose-500/70 uppercase font-bold tracking-widest mb-1">New ETA</span>
                          <span className="font-mono text-lg text-rose-200">
                            {/* Force it to just grab the numbers, append 'hours' manually */}
                            {result.recommended_action.match(/ETA:\s*([\d\.]+)/)?.[1] || "--"} <span className="text-sm text-rose-400/70">hours</span>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="p-5 bg-emerald-950/20 border border-emerald-900/50 rounded-lg backdrop-blur-sm">
                    <span className="text-emerald-500 text-xs block mb-2 font-semibold tracking-wider flex items-center">
                      <span className="w-2 h-2 bg-emerald-500 rounded-full mr-2 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
                      ROUTE SECURE
                    </span>
                    <span className="text-emerald-100/80 text-sm">
                      No evasive maneuvers required. Proceed with standard logistics.
                    </span>
                  </div>
                )}

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