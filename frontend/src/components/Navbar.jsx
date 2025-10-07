import { NavLink } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';

const links = [
  { to: '/technician', label: 'Technician' },
  { to: '/cmr', label: 'CMR' },
  { to: '/admin', label: 'Admin' },
  { to: '/client', label: 'Client' },
];

function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-3">
        <NavLink to="/" className="text-lg font-semibold text-brand">
          FieldService 2
        </NavLink>
        <nav className="flex items-center gap-4 text-sm">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `rounded px-3 py-1 transition-colors ${isActive ? 'bg-brand text-white' : 'text-slate-300 hover:text-white'}`
              }
            >
              {link.label}
            </NavLink>
          ))}
          {isAuthenticated ? (
            <button
              type="button"
              onClick={logout}
              className="rounded bg-slate-800 px-3 py-1 text-sm text-slate-200 transition hover:bg-slate-700"
            >
              Sign out
            </button>
          ) : (
            <NavLink to="/login" className="text-slate-300 hover:text-white">
              Sign in
            </NavLink>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
