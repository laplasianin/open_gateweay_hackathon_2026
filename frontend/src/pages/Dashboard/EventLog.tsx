import type { LogEntry } from "../../types";

interface Props { logs: LogEntry[]; }

const LEVEL_STYLES: Record<string, string> = { info: "text-blue-400", success: "text-green-400", warning: "text-yellow-400", critical: "text-red-400" };

export function EventLog({ logs }: Props) {
  return (
    <div className="bg-gray-800 rounded-lg p-4 overflow-y-auto max-h-[300px]">
      <h3 className="text-white font-semibold mb-3">Event Log</h3>
      <div className="space-y-1">
        {[...logs].reverse().map((log) => (
          <div key={log.id} className="text-xs font-mono">
            <span className="text-gray-500">{new Date(log.timestamp).toLocaleTimeString()}</span>{" "}
            <span className={LEVEL_STYLES[log.level] ?? "text-gray-300"}>{log.message}</span>
          </div>
        ))}
        {logs.length === 0 && <div className="text-gray-500 text-xs">No events yet. Start simulation.</div>}
      </div>
    </div>
  );
}
