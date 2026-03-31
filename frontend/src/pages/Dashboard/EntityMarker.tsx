import { CircleMarker, Tooltip } from "react-leaflet";

interface Props { name: string; role: string; lat: number; lng: number; qodActive: boolean; entityType: "staff" | "visitor"; }

const ROLE_COLORS: Record<string, string> = { security: "#3B82F6", medical: "#EF4444", logistics: "#F59E0B", operations: "#8B5CF6", comms: "#06B6D4", vip: "#EC4899", regular: "#9CA3AF" };

export function EntityMarker({ name, role, lat, lng, qodActive, entityType }: Props) {
  const color = ROLE_COLORS[role] ?? "#6B7280";
  return (
    <CircleMarker center={[lat, lng]} radius={qodActive ? 10 : 7}
      pathOptions={{ color: qodActive ? "#22C55E" : color, fillColor: color, fillOpacity: 0.8, weight: qodActive ? 3 : 1 }}>
      <Tooltip><strong>{name}</strong><br />{entityType === "staff" ? `Role: ${role}` : `Type: ${role}`}<br />QoD: {qodActive ? "ACTIVE" : "inactive"}</Tooltip>
    </CircleMarker>
  );
}
