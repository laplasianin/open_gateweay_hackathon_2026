import { api } from "../../api/client";
import { useState } from "react";

interface Props { eventId: string; }

export function SimControls({ eventId }: Props) {
  const [running, setRunning] = useState(false);
  const handleStart = async () => { await api.startSimulation(eventId); setRunning(true); };
  const handleStop = async () => { await api.stopSimulation(eventId); setRunning(false); };

  return (
    <div className="flex gap-2">
      {!running ? (
        <button onClick={handleStart} className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm font-medium">Start Simulation</button>
      ) : (
        <button onClick={handleStop} className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm font-medium">Stop Simulation</button>
      )}
    </div>
  );
}
