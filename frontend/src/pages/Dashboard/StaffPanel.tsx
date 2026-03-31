import type { Staff, Visitor } from "../../types";
import { QodBadge } from "../../components/QodBadge";

interface Props { staff: Staff[]; visitors: Visitor[]; eventId: string; }

export function StaffPanel({ staff, visitors, eventId }: Props) {
  const openMobileView = (type: "staff" | "visitor", id: string) => {
    window.open(`/${type}?event=${eventId}&id=${id}`, "_blank");
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto max-h-[400px]">
      <h3 className="text-white font-semibold mb-3">Staff</h3>
      {staff.map((s) => (
        <div key={s.id} className="flex items-center justify-between py-2 border-b border-gray-700 cursor-pointer hover:bg-gray-700 rounded px-1" onClick={() => openMobileView("staff", s.id)}>
          <div className="flex items-center gap-1.5">
            <span className={`inline-block w-2 h-2 rounded-full ${s.current_lat ? "bg-green-400" : "bg-gray-500"}`} title={s.current_lat ? "Online" : "No location"} />
            <span className="text-white text-sm">{s.name}</span><span className="text-gray-400 text-xs ml-1">{s.role}</span>
          </div>
          <QodBadge active={s.qod_status === "active"} />
        </div>
      ))}
      <h3 className="text-white font-semibold mb-3 mt-4">Visitors</h3>
      {visitors.map((v) => (
        <div key={v.id} className="flex items-center justify-between py-2 border-b border-gray-700 cursor-pointer hover:bg-gray-700 rounded px-1" onClick={() => openMobileView("visitor", v.id)}>
          <div className="flex items-center gap-1.5">
            <span className={`inline-block w-2 h-2 rounded-full ${v.current_lat ? "bg-green-400" : "bg-gray-500"}`} title={v.current_lat ? "Online" : "No location"} />
            <span className="text-white text-sm">{v.name}</span><span className="text-gray-400 text-xs ml-1">{v.type}</span>
          </div>
          <QodBadge active={v.qod_status === "active"} />
        </div>
      ))}
    </div>
  );
}
