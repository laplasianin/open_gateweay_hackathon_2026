const API_BASE = "/api";

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  getEvents: () => fetchJson<import("../types").EventListItem[]>("/events"),
  getEvent: (id: string) => fetchJson<import("../types").Event>(`/events/${id}`),
  getStaff: (eventId: string) => fetchJson<import("../types").Staff[]>(`/events/${eventId}/staff`),
  getVisitors: (eventId: string) => fetchJson<import("../types").Visitor[]>(`/events/${eventId}/visitors`),
  startSimulation: (eventId: string) => fetchJson(`/simulation/start/${eventId}`, { method: "POST" }),
  stopSimulation: (eventId: string) => fetchJson(`/simulation/stop/${eventId}`, { method: "POST" }),
  triggerSos: (visitorId: string, lat: number, lng: number) =>
    fetchJson<import("../types").Incident>("/emergency/sos", {
      method: "POST",
      body: JSON.stringify({ visitor_id: visitorId, lat, lng }),
    }),
  resolveIncident: (incidentId: string) =>
    fetchJson<import("../types").Incident>(`/emergency/${incidentId}/resolve`, { method: "POST" }),
  getActiveIncident: (staffId: string) =>
    fetchJson<import("../types").Incident | null>(`/emergency/active/${staffId}`),
};
