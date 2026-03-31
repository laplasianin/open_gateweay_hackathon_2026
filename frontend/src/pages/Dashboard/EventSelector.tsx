import type { EventListItem } from "../../types";

interface Props { events: EventListItem[]; selectedId: string | null; onSelect: (id: string) => void; }

export function EventSelector({ events, selectedId, onSelect }: Props) {
  return (
    <select className="bg-gray-800 text-white border border-gray-600 rounded px-3 py-2 text-sm"
      value={selectedId ?? ""} onChange={(e) => onSelect(e.target.value)}>
      <option value="" disabled>Select event...</option>
      {events.map((ev) => (<option key={ev.id} value={ev.id}>{ev.name} — {ev.city}, {ev.country}</option>))}
    </select>
  );
}
