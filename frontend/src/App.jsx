import { Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar.jsx';
import AdminPanel from './pages/AdminPanel.jsx';
import CMRDashboard from './pages/CMRDashboard.jsx';
import ClientPortal from './pages/ClientPortal.jsx';
import Login from './pages/Login.jsx';
import TechnicianDashboard from './pages/TechnicianDashboard.jsx';
import { useAuth } from './context/AuthContext.jsx';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Navbar />
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6">
        <Routes>
          <Route path="/" element={isAuthenticated ? <TechnicianDashboard /> : <Login />} />
          <Route path="/technician" element={<TechnicianDashboard />} />
          <Route path="/cmr" element={<CMRDashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/client" element={<ClientPortal />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
