import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { useEvents } from "../../hooks/useEvents";
import { useWebSocket } from "../../hooks/useWebSocket";
import type { Event, Staff, Visitor, Incident } from "../../types";
import { Logo } from "../../components/Logo";
import { EventSelector } from "./EventSelector";
import { SimControls } from "./SimControls";
import { EventMap } from "./EventMap";
import { StaffPanel } from "./StaffPanel";
import { EventLog } from "./EventLog";
import { AiPanel } from "./AiPanel";
import { HelpModal } from "./HelpModal";

export function DashboardPage() {
  const { events, loading } = useEvents();
  const [helpOpen, setHelpOpen] = useState(false);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [event, setEvent] = useState<Event | null>(null);
  const [staff, setStaff] = useState<Staff[]>([]);
  const [visitors, setVisitors] = useState<Visitor[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const { messages, logs, connected } = useWebSocket(selectedEventId);

  useEffect(() => {
    if (events.length > 0 && !selectedEventId) setSelectedEventId(events[0].id);
  }, [events, selectedEventId]);

  useEffect(() => {
    if (!selectedEventId) return;
    Promise.all([
      api.getEvent(selectedEventId),
      api.getStaff(selectedEventId),
      api.getVisitors(selectedEventId),
      api.getEventIncidents(selectedEventId),
    ]).then(([ev, st, vis, inc]) => { setEvent(ev); setStaff(st); setVisitors(vis); setIncidents(inc); });
  }, [selectedEventId]);

  useEffect(() => {
    if (messages.length === 0) return;
    const msg = messages[messages.length - 1];
    if (msg.type === "position_update") {
      const d = msg.data as { entity_id: string; entity_type: string; lat: number; lng: number; zone_id: string | null };
      if (d.entity_type === "staff") setStaff((prev) => prev.map((s) => (s.id === d.entity_id ? { ...s, current_lat: d.lat, current_lng: d.lng, current_zone_id: d.zone_id } : s)));
      else setVisitors((prev) => prev.map((v) => (v.id === d.entity_id ? { ...v, current_lat: d.lat, current_lng: d.lng, current_zone_id: d.zone_id } : v)));
    }
    if (msg.type === "qod_update") {
      const d = msg.data as { entity_id: string; entity_type: string; qod_status: string; session_id?: string };
      if (d.entity_type === "staff") setStaff((prev) => prev.map((s) => (s.id === d.entity_id ? { ...s, qod_status: d.qod_status as "active" | "inactive", qod_session_id: d.session_id ?? null } : s)));
      else setVisitors((prev) => prev.map((v) => (v.id === d.entity_id ? { ...v, qod_status: d.qod_status as "active" | "inactive", qod_session_id: d.session_id ?? null } : v)));
    }
    if (msg.type === "zone_update" && event) {
      const d = msg.data as { zone_id: string; crowd_level: string };
      setEvent((prev) => prev ? { ...prev, zones: prev.zones.map((z) => (z.id === d.zone_id ? { ...z, crowd_level: d.crowd_level as any } : z)) } : prev);
    }
    if (msg.type === "incident") {
      const d = msg.data as unknown as Incident;
      setIncidents((prev) => { const idx = prev.findIndex((i) => i.id === d.id); if (idx >= 0) { const u = [...prev]; u[idx] = { ...u[idx], ...d }; return u; } return [...prev, d]; });
    }
  }, [messages]);

  if (loading) return <div className="bg-gray-900 min-h-screen text-white p-8">Loading...</div>;

  return (
    <div className="bg-gray-900 min-h-screen text-white">
      <div className="flex items-center justify-between px-6 py-3 border-b border-gray-700">
        <Logo />
        <div className="flex items-center gap-4">
          <EventSelector events={events} selectedId={selectedEventId} onSelect={setSelectedEventId} />
          {selectedEventId && <SimControls eventId={selectedEventId} />}
          <div className="flex items-center gap-1.5">
            <span className={`w-2 h-2 rounded-full ${connected ? "bg-green-400 animate-pulse" : "bg-red-400"}`} />
            <span className={`text-xs ${connected ? "text-green-400" : "text-red-400"}`}>{connected ? "Live" : "Disconnected"}</span>
          </div>
          <button onClick={() => setHelpOpen(true)} className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded text-sm">Help</button>
        </div>
      </div>
      <HelpModal open={helpOpen} onClose={() => setHelpOpen(false)} />
      <div className="flex h-[calc(100vh-65px)]">
        <div className="flex-1 p-4">{event && <EventMap event={event} staff={staff} visitors={visitors} incidents={incidents} />}</div>
        <div className="w-80 p-4 space-y-4 overflow-y-auto border-l border-gray-700">
          <StaffPanel staff={staff} visitors={visitors} eventId={selectedEventId ?? ""} />
          <AiPanel logs={logs} />
          <EventLog logs={logs} />
        </div>
      </div>
    </div>
  );
}
