import { Polygon, Tooltip } from "react-leaflet";
import type { Zone } from "../../types";

const CROWD_COLORS: Record<string, string> = { low: "#22C55E", medium: "#EAB308", high: "#F97316", critical: "#EF4444" };

interface Props { zone: Zone; }

export function ZonePolygon({ zone }: Props) {
  const positions = zone.polygon.map(([lng, lat]) => [lat, lng] as [number, number]);
  const fillColor = zone.crowd_level !== "low" ? CROWD_COLORS[zone.crowd_level] : zone.color;
  return (
    <Polygon positions={positions} pathOptions={{ color: zone.color, fillColor, fillOpacity: zone.crowd_level === "critical" ? 0.5 : 0.25, weight: 2 }}>
      <Tooltip sticky><strong>{zone.name}</strong><br />Crowd: {zone.crowd_level.toUpperCase()}</Tooltip>
    </Polygon>
  );
}
