import { CircleMarker, Polyline, Tooltip } from "react-leaflet";
import { useEffect, useState } from "react";

interface Props { lat: number; lng: number; responderLat?: number; responderLng?: number; status: string; }

export function IncidentMarker({ lat, lng, responderLat, responderLng, status }: Props) {
  const [pulse, setPulse] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => setPulse((p) => !p), 800);
    return () => clearInterval(interval);
  }, []);

  if (status === "resolved") return null;
  return (
    <>
      {/* Outer pulse ring */}
      <CircleMarker
        center={[lat, lng]}
        radius={pulse ? 24 : 18}
        pathOptions={{ color: "#EF4444", fillColor: "#EF4444", fillOpacity: pulse ? 0.15 : 0.08, weight: 1 }}
      />
      {/* Inner SOS marker */}
      <CircleMarker
        center={[lat, lng]}
        radius={12}
        pathOptions={{ color: "#fff", fillColor: "#EF4444", fillOpacity: 0.9, weight: 2 }}
      >
        <Tooltip permanent direction="top" offset={[0, -15]}>
          <span className="font-bold text-red-600">SOS</span>
        </Tooltip>
      </CircleMarker>
      {responderLat && responderLng && (
        <Polyline positions={[[lat, lng], [responderLat, responderLng]]} pathOptions={{ color: "#EF4444", dashArray: "8 4", weight: 2 }} />
      )}
    </>
  );
}
