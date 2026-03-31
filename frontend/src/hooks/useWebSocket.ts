import { useEffect, useRef, useState } from "react";
import type { WsMessage, LogEntry } from "../types";

interface UseWebSocketReturn {
  messages: WsMessage[];
  logs: LogEntry[];
  connected: boolean;
}

export function useWebSocket(eventId: string | null): UseWebSocketReturn {
  const wsRef = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<WsMessage[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!eventId) return;
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/events/${eventId}`);
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (event) => {
      const msg: WsMessage = JSON.parse(event.data);
      setMessages((prev) => [...prev.slice(-200), msg]);
      if (msg.type === "log") {
        const entry: LogEntry = {
          id: crypto.randomUUID(),
          timestamp: new Date().toISOString(),
          message: (msg.data as Record<string, string>).message,
          level: (msg.data as Record<string, string>).level as LogEntry["level"],
        };
        setLogs((prev) => [...prev.slice(-100), entry]);
      }
    };
    return () => { ws.close(); setConnected(false); };
  }, [eventId]);

  return { messages, logs, connected };
}
