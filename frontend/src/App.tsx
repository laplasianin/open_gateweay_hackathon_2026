import { BrowserRouter, Routes, Route } from "react-router-dom";

function Dashboard() {
  return <div className="p-4 text-white bg-gray-900 min-h-screen">Dashboard</div>;
}

function Staff() {
  return <div className="p-4">Staff View</div>;
}

function Visitor() {
  return <div className="p-4">Visitor View</div>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/staff" element={<Staff />} />
        <Route path="/visitor" element={<Visitor />} />
      </Routes>
    </BrowserRouter>
  );
}
