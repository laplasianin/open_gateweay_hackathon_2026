import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../../api/client";
import { useWebSocket } from "../../hooks/useWebSocket";
import { QodBadge } from "../../components/QodBadge";
import { SosButton } from "../../components/SosButton";
import type { Visitor } from "../../types";

export function VisitorPage() {
  const [searchParams] = useSearchParams();
  const visitorId = searchParams.get("id");
  const eventId = searchParams.get("event");
  const [visitor, setVisitor] = useState<Visitor | null>(null);
  const [sosSent, setSosSent] = useState(false);
  const [sosStatus, setSosStatus] = useState<string | null>(null);
  const { messages } = useWebSocket(eventId);

  useEffect(() => {
    if (!eventId || !visitorId) return;
    api.getVisitors(eventId).then((all) => { const me = all.find((v) => v.id === visitorId); if (me) setVisitor(me); });
  }, [eventId, visitorId]);

  useEffect(() => {
    if (!messages.length || !visitorId) return;
    const msg = messages[messages.length - 1];
    if (msg.type === "qod_update" && (msg.data as any).entity_id === visitorId)
      setVisitor((prev) => prev ? { ...prev, qod_status: (msg.data as any).qod_status } : prev);
    if (msg.type === "incident") {
      const d = msg.data as any;
      if (d.status === "responding") setSosStatus("Help is on the way!");
      if (d.status === "resolved") { setSosStatus("Incident resolved"); setSosSent(false); }
    }
  }, [messages, visitorId]);

  const handleSos = async () => {
    if (!visitor || !visitor.current_lat || !visitor.current_lng) return;
    setSosSent(true); setSosStatus("Sending SOS...");
    await api.triggerSos(visitor.id, visitor.current_lat, visitor.current_lng);
  };

  if (!visitor) return (
    <div className="p-6 min-h-screen bg-gray-50">
      <h1 className="text-xl font-bold mb-4">StageFlow</h1>
      <p className="text-gray-500">Add ?event=EVENT_ID&id=VISITOR_ID to URL</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-4 py-3"><h1 className="text-lg font-bold">StageFlow</h1></div>
      <div className="p-4 space-y-4">
        <div className="bg-white rounded-xl shadow p-6 text-center">
          <p className="text-sm text-gray-500 mb-2">Welcome, {visitor.name}</p>
          {visitor.type === "vip" && (
            <>
              <p className="text-sm text-gray-500 mb-2">Network Status</p>
              <div className="text-2xl font-bold mb-2">
                {visitor.qod_status === "active" ? <span className="text-green-600">Internet Boost Active</span> : <span className="text-gray-400">Standard</span>}
              </div>
              <QodBadge active={visitor.qod_status === "active"} />
            </>
          )}
        </div>
        {sosStatus && (
          <div className={`rounded-xl p-4 text-center font-semibold ${sosStatus.includes("way") ? "bg-blue-100 text-blue-700" : sosStatus.includes("resolved") ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>
            {sosStatus}
          </div>
        )}
        <SosButton onPress={handleSos} disabled={sosSent} />
      </div>
    </div>
  );
}
