import { useState } from "react";
import type { Staff, Visitor } from "../../types";
import { QodBadge } from "../../components/QodBadge";
import { VipTimer } from "../../components/VipTimer";

interface Props { staff: Staff[]; visitors: Visitor[]; eventId: string; }

export function StaffPanel({ staff, visitors, eventId }: Props) {
  const [qrId, setQrId] = useState<{ type: string; id: string } | null>(null);

  const openMobileView = (type: "staff" | "visitor", id: string) => {
    window.open(`/${type}?event=${eventId}&id=${id}`, "_blank");
  };

  const showQr = (e: React.MouseEvent, type: string, id: string) => {
    e.stopPropagation();
    setQrId(qrId?.id === id ? null : { type, id });
  };

  const qrUrl = qrId ? `${window.location.origin}/${qrId.type}?event=${eventId}&id=${qrId.id}` : "";

  return (
    <div className="bg-gray-800 rounded-lg p-3 overflow-y-auto max-h-[400px]">
      <h3 className="text-white font-semibold mb-2 text-sm">Staff</h3>
      {staff.map((s) => (
        <div key={s.id}>
          <div
            className="flex items-center gap-2 py-1.5 border-b border-gray-700/50 cursor-pointer hover:bg-gray-700/50 rounded px-1"
            onClick={() => openMobileView("staff", s.id)}
          >
            <span className={`shrink-0 w-1.5 h-1.5 rounded-full ${s.current_lat ? "bg-green-400" : "bg-gray-500"}`} />
            <span className="text-white text-xs truncate flex-1">{s.name}</span>
            <span className="text-gray-500 text-xs shrink-0">{s.role}</span>
            <QodBadge active={s.qod_status === "active"} />
            <button onClick={(e) => showQr(e, "staff", s.id)} className="text-gray-500 hover:text-white text-xs shrink-0">QR</button>
          </div>
          {qrId?.id === s.id && (
            <div className="bg-gray-900 p-3 rounded mb-1">
              <img src={`https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(qrUrl)}`} alt="QR" className="mx-auto rounded" width={140} height={140} />
              <p className="text-gray-400 text-xs mt-2 text-center break-all">{qrUrl}</p>
            </div>
          )}
        </div>
      ))}
      <h3 className="text-white font-semibold mb-2 mt-3 text-sm">Visitors</h3>
      {visitors.map((v) => (
        <div key={v.id}>
          <div
            className="flex items-center gap-2 py-1.5 border-b border-gray-700/50 cursor-pointer hover:bg-gray-700/50 rounded px-1"
            onClick={() => openMobileView("visitor", v.id)}
          >
            <span className={`shrink-0 w-1.5 h-1.5 rounded-full ${v.current_lat ? "bg-green-400" : "bg-gray-500"}`} />
            <span className="text-white text-xs truncate flex-1">{v.name}</span>
            <span className="text-gray-500 text-xs shrink-0">{v.type}</span>
            {v.type === "vip" ? <VipTimer active={v.qod_status === "active"} /> : <QodBadge active={v.qod_status === "active"} />}
            <button onClick={(e) => showQr(e, "visitor", v.id)} className="text-gray-500 hover:text-white text-xs shrink-0">QR</button>
          </div>
          {qrId?.id === v.id && (
            <div className="bg-gray-900 p-3 rounded mb-1">
              <img src={`https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(qrUrl)}`} alt="QR" className="mx-auto rounded" width={140} height={140} />
              <p className="text-gray-400 text-xs mt-2 text-center break-all">{qrUrl}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
