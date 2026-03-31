import { MapContainer, TileLayer, useMap } from "react-leaflet";
import { useEffect } from "react";
import "leaflet/dist/leaflet.css";
import type { Event, Staff, Visitor, Incident } from "../../types";
import { ZonePolygon } from "./ZonePolygon";
import { EntityMarker } from "./EntityMarker";
import { IncidentMarker } from "./IncidentMarker";

function ChangeView({ center, zoom }: { center: [number, number]; zoom: number }) {
  const map = useMap();
  useEffect(() => { map.setView(center, zoom); }, [center[0], center[1], zoom]);
  return null;
}

interface Props { event: Event; staff: Staff[]; visitors: Visitor[]; incidents: Incident[]; }

export function EventMap({ event, staff, visitors, incidents }: Props) {
  const center: [number, number] = [(event.bounds.north + event.bounds.south) / 2, (event.bounds.east + event.bounds.west) / 2];
  return (
    <MapContainer center={center} zoom={16} className="h-full w-full rounded-lg" scrollWheelZoom>
      <ChangeView center={center} zoom={16} />
      <TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {event.zones.map((zone) => (<ZonePolygon key={zone.id} zone={zone} />))}
      {staff.filter((s) => s.current_lat && s.current_lng).map((s) => (
        <EntityMarker key={s.id} name={s.name} role={s.role} lat={s.current_lat!} lng={s.current_lng!} qodActive={s.qod_status === "active"} entityType="staff" />
      ))}
      {visitors.filter((v) => v.current_lat && v.current_lng).map((v) => (
        <EntityMarker key={v.id} name={v.name} role={v.type} lat={v.current_lat!} lng={v.current_lng!} qodActive={v.qod_status === "active"} entityType="visitor" />
      ))}
      {incidents.map((inc) => {
        const responder = staff.find((s) => s.id === inc.responder_id);
        return (<IncidentMarker key={inc.id} lat={inc.lat} lng={inc.lng} responderLat={responder?.current_lat ?? undefined} responderLng={responder?.current_lng ?? undefined} status={inc.status} />);
      })}
    </MapContainer>
  );
}
