"use client";

import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import L from "leaflet";

const icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

export default function Map({ isRerouted, coordinates }: { isRerouted: boolean, coordinates?: [number, number][] }) {
  
  // Dynamically set the start and end markers based on the AI's actual road data!
  const start: [number, number] = coordinates && coordinates.length > 0 ? coordinates[0] : [26.8467, 80.9462];
  const end: [number, number] = coordinates && coordinates.length > 0 ? coordinates[coordinates.length - 1] : [31.5, 34.4667];

  // If the AI gives us a road path, use it. Otherwise, fallback to the straight line.
  const pathPositions = coordinates && coordinates.length > 0 ? coordinates : [start, end];

  return (
    <div className="w-full h-[400px] rounded-lg overflow-hidden border border-slate-700 shadow-2xl relative z-0">
      <MapContainer 
        center={[28.0, 58.0]} 
        zoom={4} 
        style={{ height: "100%", width: "100%", background: "#020617" }}
      >
        <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='&copy; CartoDB' />

        <Marker position={start} icon={icon} />
        <Marker position={end} icon={icon} />

        <Polyline 
          key={pathPositions.length}
          positions={pathPositions} 
          color={isRerouted ? "#f43f5e" : "#10b981"} 
          weight={4}
          className={isRerouted ? "animate-pulse shadow-lg" : ""}
        />
      </MapContainer>

      <div className="absolute top-0 left-0 w-full h-full pointer-events-none shadow-[inset_0_0_50px_rgba(0,0,0,0.8)] z-10"></div>
    </div>
  );
}