import type { LogEntry } from "../../types";

interface Props { logs: LogEntry[]; }

export function AiPanel({ logs }: Props) {
  const aiLogs = logs.filter((l) => l.message.startsWith("AI Alert") || l.message.startsWith("SOS") || l.message.includes("Medic"));

  return (
    <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto max-h-[250px] border border-purple-500/30">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse" />
        <h3 className="text-purple-300 font-semibold text-sm">AI Decision Engine</h3>
      </div>
      <div className="space-y-2">
        {[...aiLogs].reverse().map((log) => (
          <div key={log.id} className="bg-gray-900 rounded p-2">
            <div className="flex items-start gap-2">
              <span className="text-purple-400 text-xs mt-0.5">&#9670;</span>
              <div>
                <p className="text-sm text-gray-200">{formatAiMessage(log.message)}</p>
                <p className="text-xs text-gray-500 mt-1">{new Date(log.timestamp).toLocaleTimeString()}</p>
              </div>
            </div>
          </div>
        ))}
        {aiLogs.length === 0 && (
          <div className="text-gray-500 text-xs font-mono">
            <p>Monitoring crowd density...</p>
            <p className="mt-1">No anomalies detected</p>
          </div>
        )}
      </div>
    </div>
  );
}

function formatAiMessage(msg: string): string {
  if (msg.includes("crowd density")) {
    return msg.replace("AI Alert:", "Analysis:") + " | Action: Notify organizer, prepare staff reallocation";
  }
  if (msg.includes("SOS received")) {
    return "Emergency protocol activated. " + msg;
  }
  if (msg.includes("Medic") && msg.includes("reached")) {
    return "Incident resolved. " + msg + " | Deactivating emergency protocol.";
  }
  return msg;
}
