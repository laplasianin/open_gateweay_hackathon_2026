export interface Event {
  id: string;
  name: string;
  description: string;
  city: string;
  country: string;
  bounds: { north: number; south: number; east: number; west: number };
  status: string;
  zones: Zone[];
}

export interface EventListItem {
  id: string;
  name: string;
  city: string;
  country: string;
  status: string;
}

export interface Zone {
  id: string;
  name: string;
  type: string;
  polygon: [number, number][];
  crowd_level: "low" | "medium" | "high" | "critical";
  color: string;
}

export interface Staff {
  id: string;
  name: string;
  phone: string;
  role: string;
  device_id: string;
  qod_status: "active" | "inactive";
  qod_session_id: string | null;
  current_lat: number | null;
  current_lng: number | null;
  current_zone_id: string | null;
}

export interface Visitor {
  id: string;
  name: string;
  phone: string;
  type: "vip" | "regular";
  device_id: string;
  qod_status: "active" | "inactive";
  qod_session_id: string | null;
  current_lat: number | null;
  current_lng: number | null;
  current_zone_id: string | null;
}

export interface Incident {
  id: string;
  event_id: string;
  type: string;
  status: "open" | "responding" | "resolved";
  reporter_id: string | null;
  responder_id: string | null;
  lat: number;
  lng: number;
  created_at: string;
  resolved_at: string | null;
}

export interface WsMessage {
  type: "position_update" | "qod_update" | "zone_update" | "incident" | "log";
  data: Record<string, unknown>;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  message: string;
  level: "info" | "warning" | "critical" | "success";
}
