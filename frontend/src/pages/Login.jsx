import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext.jsx';
import { login } from '../services/auth.js';

function Login() {
  const navigate = useNavigate();
  const { login: setToken } = useAuth();
  const [form, setForm] = useState({ username: 'admin@example.com', password: 'admin123' });
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const token = await login(form);
      setToken(token.access_token);
      navigate('/technician');
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Unable to sign in');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="mx-auto w-full max-w-md rounded-lg border border-slate-800 bg-slate-900/60 p-6 shadow">
      <h1 className="text-xl font-semibold text-white">Welcome back</h1>
      <p className="mt-1 text-sm text-slate-400">Sign in with your FieldService 2 credentials.</p>
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <label className="flex flex-col text-sm">
          Email
          <input
            type="email"
            name="username"
            value={form.username}
            onChange={handleChange}
            className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            required
          />
        </label>
        <label className="flex flex-col text-sm">
          Password
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            required
          />
        </label>
        {error ? <p className="text-sm text-red-400">{error}</p> : null}
        <button
          type="submit"
          className="w-full rounded bg-brand px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-dark"
          disabled={isLoading}
        >
          {isLoading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </section>
  );
}

export default Login;
