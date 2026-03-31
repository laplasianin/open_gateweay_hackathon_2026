import type { Staff, Visitor } from "../../types";
import { QodBadge } from "../../components/QodBadge";

interface Props { staff: Staff[]; visitors: Visitor[]; }

export function StaffPanel({ staff, visitors }: Props) {
  return (
    <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto max-h-[400px]">
      <h3 className="text-white font-semibold mb-3">Staff</h3>
      {staff.map((s) => (
        <div key={s.id} className="flex items-center justify-between py-2 border-b border-gray-700">
          <div><span className="text-white text-sm">{s.name}</span><span className="text-gray-400 text-xs ml-2">{s.role}</span></div>
          <QodBadge active={s.qod_status === "active"} />
        </div>
      ))}
      <h3 className="text-white font-semibold mb-3 mt-4">Visitors</h3>
      {visitors.map((v) => (
        <div key={v.id} className="flex items-center justify-between py-2 border-b border-gray-700">
          <div><span className="text-white text-sm">{v.name}</span><span className="text-gray-400 text-xs ml-2">{v.type}</span></div>
          <QodBadge active={v.qod_status === "active"} />
        </div>
      ))}
    </div>
  );
}
