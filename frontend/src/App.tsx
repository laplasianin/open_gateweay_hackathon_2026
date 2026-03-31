import { BrowserRouter, Routes, Route } from "react-router-dom";
import { DashboardPage } from "./pages/Dashboard/DashboardPage";
import { StaffPage } from "./pages/Staff/StaffPage";
import { VisitorPage } from "./pages/Visitor/VisitorPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/staff" element={<StaffPage />} />
        <Route path="/visitor" element={<VisitorPage />} />
      </Routes>
    </BrowserRouter>
  );
}
