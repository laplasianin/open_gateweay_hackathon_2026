import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../../api/client";
import { useWebSocket } from "../../hooks/useWebSocket";
import { QodBadge } from "../../components/QodBadge";
import type { Staff } from "../../types";

interface IncidentAlert {
  lat: number;
  lng: number;
  zone_name: string;
}

function haversine(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 6371000;
  const toRad = (x: number) => (x * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function bearing(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const toRad = (x: number) => (x * Math.PI) / 180;
  const toDeg = (x: number) => (x * 180) / Math.PI;
  const dLng = toRad(lng2 - lng1);
  const y = Math.sin(dLng) * Math.cos(toRad(lat2));
  const x = Math.cos(toRad(lat1)) * Math.sin(toRad(lat2)) - Math.sin(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.cos(dLng);
  return (toDeg(Math.atan2(y, x)) + 360) % 360;
}

export function StaffPage() {
  const [searchParams] = useSearchParams();
  const staffId = searchParams.get("id");
  const eventId = searchParams.get("event");
  const [staff, setStaff] = useState<Staff | null>(null);
  const [incident, setIncident] = useState<IncidentAlert | null>(null);
  const { messages } = useWebSocket(eventId);

  useEffect(() => {
    if (!eventId || !staffId) return;
    api.getStaff(eventId).then((all) => { const me = all.find((s) => s.id === staffId); if (me) setStaff(me); });
    api.getActiveIncident(staffId).then((inc) => {
      if (inc && inc.status !== "resolved") {
        setIncident({ lat: inc.lat, lng: inc.lng, zone_name: "Active incident" });
      }
    }).catch(() => {});
  }, [eventId, staffId]);

  useEffect(() => {
    if (!messages.length || !staffId) return;
    const msg = messages[messages.length - 1];
    if (msg.type === "qod_update" && (msg.data as any).entity_id === staffId)
      setStaff((prev) => prev ? { ...prev, qod_status: (msg.data as any).qod_status } : prev);
    if (msg.type === "position_update" && (msg.data as any).entity_id === staffId) {
      const d = msg.data as any;
      setStaff((prev) => prev ? { ...prev, current_lat: d.lat, current_lng: d.lng } : prev);
    }
    if (msg.type === "incident") {
      const d = msg.data as any;
      if (d.responder_id === staffId && d.status !== "resolved") {
        setIncident({ lat: d.lat, lng: d.lng, zone_name: d.zone_name ?? "Unknown" });
      }
      if (d.status === "resolved") setIncident(null);
    }
  }, [messages, staffId]);

  if (!staff) return (
    <div className="p-6 min-h-screen bg-gray-50">
      <h1 className="text-xl font-bold mb-4">StageFlow — Staff</h1>
      <p className="text-gray-500">Add ?event=EVENT_ID&id=STAFF_ID to URL</p>
    </div>
  );

  const dist = (incident && staff.current_lat && staff.current_lng)
    ? Math.round(haversine(staff.current_lat, staff.current_lng, incident.lat, incident.lng))
    : null;
  const angle = (incident && staff.current_lat && staff.current_lng)
    ? bearing(staff.current_lat, staff.current_lng, incident.lat, incident.lng)
    : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-4 py-3"><h1 className="text-lg font-bold">StageFlow</h1></div>

      {incident && (
        <div className="bg-red-600 text-white p-4">
          <p className="font-bold text-center text-xl animate-pulse">EMERGENCY</p>

          {/* Compass arrow */}
          <div className="flex justify-center my-4">
            <div className="relative w-28 h-28 rounded-full border-4 border-red-300 flex items-center justify-center bg-red-700">
              <svg
                width="60" height="60" viewBox="0 0 60 60"
                style={{ transform: `rotate(${angle}deg)`, transition: "transform 0.5s ease" }}
              >
                <polygon points="30,5 40,45 30,38 20,45" fill="white" opacity="0.95" />
              </svg>
              <div className="absolute bottom-1 text-xs text-red-200 font-mono">
                {dist !== null ? `${dist}m` : "..."}
              </div>
            </div>
          </div>

          <div className="bg-red-700 rounded-lg p-3 space-y-2">
            <div className="flex justify-between">
              <span className="text-red-200 text-sm">Distance</span>
              <span className="font-bold text-lg">{dist !== null ? `${dist}m` : "calculating..."}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-red-200 text-sm">Location</span>
              <span className="font-semibold">{incident.zone_name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-red-200 text-sm">Coordinates</span>
              <span className="font-mono text-sm">{incident.lat.toFixed(4)}, {incident.lng.toFixed(4)}</span>
            </div>
          </div>
          <p className="text-center text-sm mt-3 text-red-200">Proceed to patient immediately</p>
        </div>
      )}

      <div className="p-4 space-y-4">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-xl font-semibold">{staff.name}</h2>
          <p className="text-gray-500 capitalize">{staff.role}</p>
        </div>
        <div className="bg-white rounded-xl shadow p-6 text-center">
          <p className="text-sm text-gray-500 mb-2">Network Status</p>
          <div className="text-2xl font-bold mb-2">
            {staff.qod_status === "active" ? <span className="text-green-600">Priority Active</span> : <span className="text-gray-400">Normal</span>}
          </div>
          <QodBadge active={staff.qod_status === "active"} />
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <p className="text-sm text-gray-500">Phone</p>
          <p className="font-medium">{staff.phone}</p>
        </div>
      </div>
    </div>
  );
}
