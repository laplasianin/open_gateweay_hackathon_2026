import { useEffect, useState } from "react";

interface Props {
  active: boolean;
  durationSeconds?: number; // default 900 (15 min)
}

export function VipTimer({ active, durationSeconds = 900 }: Props) {
  const [remaining, setRemaining] = useState(durationSeconds);

  useEffect(() => {
    if (!active) { setRemaining(durationSeconds); return; }
    setRemaining(durationSeconds);
    const interval = setInterval(() => {
      setRemaining((r) => Math.max(0, r - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [active, durationSeconds]);

  if (!active) return null;

  const min = Math.floor(remaining / 60);
  const sec = remaining % 60;

  return (
    <span className="text-xs px-2 py-1 rounded-full font-mono bg-pink-600 text-white">
      {min}:{sec.toString().padStart(2, "0")}
    </span>
  );
}
