import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../../api/client";
import { useWebSocket } from "../../hooks/useWebSocket";
import { QodBadge } from "../../components/QodBadge";
import type { Staff } from "../../types";

export function StaffPage() {
  const [searchParams] = useSearchParams();
  const staffId = searchParams.get("id");
  const eventId = searchParams.get("event");
  const [staff, setStaff] = useState<Staff | null>(null);
  const [alert, setAlert] = useState<string | null>(null);
  const { messages } = useWebSocket(eventId);

  useEffect(() => {
    if (!eventId || !staffId) return;
    api.getStaff(eventId).then((all) => { const me = all.find((s) => s.id === staffId); if (me) setStaff(me); });
  }, [eventId, staffId]);

  useEffect(() => {
    if (!messages.length || !staffId) return;
    const msg = messages[messages.length - 1];
    if (msg.type === "qod_update" && (msg.data as any).entity_id === staffId)
      setStaff((prev) => prev ? { ...prev, qod_status: (msg.data as any).qod_status } : prev);
    if (msg.type === "incident") {
      const d = msg.data as any;
      if (d.responder_id === staffId && d.status !== "resolved") setAlert(`Emergency! Patient ${d.distance_meters ?? "?"}m from you`);
      if (d.status === "resolved") setAlert(null);
    }
  }, [messages, staffId]);

  if (!staff) return (
    <div className="p-6 min-h-screen bg-gray-50">
      <h1 className="text-xl font-bold mb-4">StageFlow — Staff</h1>
      <p className="text-gray-500">Add ?event=EVENT_ID&id=STAFF_ID to URL</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-4 py-3"><h1 className="text-lg font-bold">StageFlow</h1></div>
      {alert && <div className="bg-red-600 text-white p-4 text-center font-bold animate-pulse">{alert}</div>}
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
