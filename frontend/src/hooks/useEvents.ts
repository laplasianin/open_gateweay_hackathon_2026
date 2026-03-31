import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { EventListItem } from "../types";

export function useEvents() {
  const [events, setEvents] = useState<EventListItem[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    api.getEvents().then((data) => { setEvents(data); setLoading(false); });
  }, []);
  return { events, loading };
}
