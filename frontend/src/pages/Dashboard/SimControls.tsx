import { api } from "../../api/client";
import { useState, useEffect } from "react";

interface Props { eventId: string; }

export function SimControls({ eventId }: Props) {
  const [running, setRunning] = useState(false);

  useEffect(() => {
    api.simulationStatus(eventId).then((s) => setRunning(s.running)).catch(() => {});
  }, [eventId]);

  const handleStart = async () => { await api.startSimulation(eventId); setRunning(true); };
  const handleStop = async () => { await api.stopSimulation(eventId); setRunning(false); };
  const handleReset = async () => {
    await api.resetSimulation(eventId);
    setRunning(false);
    window.location.reload();
  };

  return (
    <div className="flex gap-2">
      {!running ? (
        <button onClick={handleStart} className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm font-medium">Start Simulation</button>
      ) : (
        <button onClick={handleStop} className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded text-sm font-medium">Stop Simulation</button>
      )}
      <button onClick={handleReset} className="bg-gray-600 hover:bg-gray-500 text-white px-3 py-2 rounded text-sm" title="Reset everything">
        Reset
      </button>
    </div>
  );
}
