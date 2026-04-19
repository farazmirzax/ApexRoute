"use client";

import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";

const icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function FitMapToRoute({
  coordinates,
  isRerouted,
}: {
  coordinates: [number, number][];
  isRerouted: boolean;
}) {
  const map = useMap();

  useEffect(() => {
    if (!coordinates.length) {
      return;
    }

    if (coordinates.length === 1) {
      map.setView(coordinates[0], 6);
      return;
    }

    const bounds = L.latLngBounds(coordinates);
    map.fitBounds(bounds, {
      paddingTopLeft: [48, isRerouted ? 48 : 72],
      paddingBottomRight: [48, isRerouted ? 48 : 120],
      maxZoom: 6,
    });
  }, [coordinates, isRerouted, map]);

  return null;
}

export default function Map({ isRerouted, coordinates }: { isRerouted: boolean, coordinates?: [number, number][] }) {
  const hasRoute = !!coordinates && coordinates.length > 0;
  const start: [number, number] | null = hasRoute ? coordinates[0] : null;
  const end: [number, number] | null = hasRoute ? coordinates[coordinates.length - 1] : null;
  const pathPositions = hasRoute ? coordinates : [];

  return (
    <div className="w-full h-[360px] md:h-[420px] xl:h-[460px] rounded-lg overflow-hidden border border-slate-700 shadow-2xl relative z-0">
      <MapContainer 
        center={[24.0, 68.0]} 
        zoom={4}
        scrollWheelZoom={false}
        style={{ height: "100%", width: "100%", background: "#020617" }}
      >
        <FitMapToRoute coordinates={pathPositions} isRerouted={isRerouted} />
        <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" attribution='&copy; CartoDB' />

        {start && <Marker position={start} icon={icon} />}
        {end && <Marker position={end} icon={icon} />}

        {hasRoute && (
          <Polyline 
            key={JSON.stringify(pathPositions)}
            positions={pathPositions} 
            color={isRerouted ? "#f43f5e" : "#10b981"} 
            weight={5}
            opacity={0.9}
            className={isRerouted ? "animate-pulse shadow-lg" : ""}
          />
        )}
      </MapContainer>

      {!hasRoute && (
        <div className="absolute inset-0 z-20 flex items-center justify-center pointer-events-none">
          <div className="rounded-xl border border-slate-700/80 bg-slate-950/80 px-5 py-4 text-center backdrop-blur-sm shadow-2xl">
            <div className="text-sm font-semibold tracking-[0.2em] text-slate-300">AWAITING ROUTE ANALYSIS</div>
            <div className="mt-2 text-xs tracking-wider text-slate-500">
              Enter an origin and destination to project the tactical path.
            </div>
          </div>
        </div>
      )}

      <div className="absolute top-0 left-0 w-full h-full pointer-events-none shadow-[inset_0_0_50px_rgba(0,0,0,0.8)] z-10"></div>
    </div>
  );
}
