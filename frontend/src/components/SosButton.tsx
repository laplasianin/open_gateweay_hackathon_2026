interface Props { onPress: () => void; disabled?: boolean; }

export function SosButton({ onPress, disabled }: Props) {
  return (
    <button onClick={onPress} disabled={disabled}
      className="w-full py-6 rounded-2xl text-white text-2xl font-bold bg-red-600 hover:bg-red-700 active:bg-red-800 disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg transition-all">
      {disabled ? "SOS Sent" : "SOS Emergency"}
    </button>
  );
}
