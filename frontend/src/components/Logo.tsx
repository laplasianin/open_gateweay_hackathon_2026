export function Logo({ size = 28 }: { size?: number }) {
  return (
    <div className="flex items-center gap-2">
      <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
        {/* Flower/burst shape inspired by StageFlow branding */}
        {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((angle) => (
          <ellipse
            key={angle}
            cx="50" cy="50" rx="8" ry="22"
            fill="#F87171"
            transform={`rotate(${angle} 50 50)`}
            opacity={0.85}
          />
        ))}
        <circle cx="50" cy="50" r="10" fill="#F87171" />
      </svg>
      <span className="font-bold text-lg tracking-tight">StageFlow</span>
    </div>
  );
}
