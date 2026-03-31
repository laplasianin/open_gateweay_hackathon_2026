interface Props { active: boolean; }

export function QodBadge({ active }: Props) {
  return (
    <span className={`text-xs px-2 py-1 rounded-full font-medium ${active ? "bg-green-600 text-white" : "bg-gray-600 text-gray-300"}`}>
      {active ? "Priority Active" : "Normal"}
    </span>
  );
}
