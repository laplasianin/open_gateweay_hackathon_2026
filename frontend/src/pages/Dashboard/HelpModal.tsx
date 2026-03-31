interface Props { open: boolean; onClose: () => void; }

export function HelpModal({ open, onClose }: Props) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/60 z-[9999] flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-gray-800 rounded-xl max-w-2xl w-full max-h-[85vh] overflow-y-auto p-6 text-white" onClick={(e) => e.stopPropagation()}>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">StageFlow Demo Guide</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-2xl leading-none">&times;</button>
        </div>

        <div className="space-y-5 text-sm">
          <Section title="1. Priority QoD for Staff" color="blue">
            <p>Staff members automatically receive priority network access when entering event zones.</p>
            <Steps steps={[
              "Click \"Start Simulation\" — staff markers begin moving on the map",
              "Watch Juan Garcia (security) enter Main Stage A zone",
              "Event log shows \"QoD activated\" — his badge turns green",
              "When he exits the zone, QoD is deactivated automatically",
            ]} />
          </Section>

          <Section title="2. VIP Internet Boost" color="pink">
            <p>VIP visitors receive a 15-minute internet boost when entering VIP Area.</p>
            <Steps steps={[
              "With simulation running, watch Anna Berg (VIP) move toward VIP Area",
              "When she enters, a countdown timer appears next to her name (15:00)",
              "Click on her name to open her mobile view — shows \"Internet Boost Active\"",
            ]} />
          </Section>

          <Section title="3. Crowd Density Monitoring" color="yellow">
            <p>AI monitors crowd density and alerts when zones become overcrowded.</p>
            <Steps steps={[
              "Start simulation and wait ~30 seconds",
              "Main Stage A zone turns orange (HIGH density)",
              "At ~45 seconds it turns red (CRITICAL)",
              "AI Decision panel shows analysis and recommendations",
            ]} />
          </Section>

          <Section title="4. Emergency SOS" color="red">
            <p>Visitors can trigger SOS. System finds nearest medic, gives them QoD boost, and guides them to patient.</p>
            <Steps steps={[
              "Start simulation, wait ~10 seconds for positions to initialize",
              "In the Staff panel, click on \"Visitor X\" — opens visitor mobile view",
              "Press the red \"SOS Emergency\" button",
              "On the dashboard: pulsing SOS marker appears, dashed line to medic",
              "Dr. Maria Lopez starts moving toward patient automatically",
              "Click on Dr. Maria Lopez to see her compass navigation view",
              "When medic reaches patient (<20m), incident auto-resolves",
            ]} />
          </Section>

          <Section title="5. Multi-Event Support" color="purple">
            <p>Same platform works for different event types.</p>
            <Steps steps={[
              "Use the event dropdown to switch to \"World Cup 2026\"",
              "Map flies to Estadio Azteca in Mexico City",
              "Different zones (stands, pitch, VIP box) and staff",
            ]} />
          </Section>

          <Section title="Tips" color="gray">
            <Steps steps={[
              "QR button next to each person — scan with phone to open their mobile view",
              "Green dot = person has location, Gray dot = no location yet",
              "\"Reset\" button clears everything — positions, incidents, QoD statuses",
              "Nokia QoD API calls are logged in Event Log (currently in mock mode)",
            ]} />
          </Section>
        </div>
      </div>
    </div>
  );
}

function Section({ title, color, children }: { title: string; color: string; children: React.ReactNode }) {
  const colors: Record<string, string> = {
    blue: "border-blue-500/40",
    pink: "border-pink-500/40",
    yellow: "border-yellow-500/40",
    red: "border-red-500/40",
    purple: "border-purple-500/40",
    gray: "border-gray-500/40",
  };
  return (
    <div className={`border-l-2 ${colors[color] ?? colors.gray} pl-4`}>
      <h3 className="font-semibold mb-1">{title}</h3>
      {children}
    </div>
  );
}

function Steps({ steps }: { steps: string[] }) {
  return (
    <ol className="mt-2 space-y-1 text-gray-300">
      {steps.map((step, i) => (
        <li key={i} className="flex gap-2">
          <span className="text-gray-500 shrink-0">{i + 1}.</span>
          <span>{step}</span>
        </li>
      ))}
    </ol>
  );
}
