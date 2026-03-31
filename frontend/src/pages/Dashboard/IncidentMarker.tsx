import { CircleMarker, Polyline, Tooltip } from "react-leaflet";

interface Props { lat: number; lng: number; responderLat?: number; responderLng?: number; status: string; }

export function IncidentMarker({ lat, lng, responderLat, responderLng, status }: Props) {
  if (status === "resolved") return null;
  return (
    <>
      <CircleMarker center={[lat, lng]} radius={14} pathOptions={{ color: "#EF4444", fillColor: "#EF4444", fillOpacity: 0.6, weight: 3 }}>
        <Tooltip>SOS — {status}</Tooltip>
      </CircleMarker>
      {responderLat && responderLng && (
        <Polyline positions={[[lat, lng], [responderLat, responderLng]]} pathOptions={{ color: "#EF4444", dashArray: "8 4", weight: 2 }} />
      )}
    </>
  );
}
