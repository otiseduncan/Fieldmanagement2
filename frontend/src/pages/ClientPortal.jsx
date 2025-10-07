import { useState } from 'react';

import { createJob } from '../services/api.js';

const defaultRequest = {
  ro_number: '',
  vin: '',
  client_notes: '',
  client_id: '',
};

function ClientPortal() {
  const [form, setForm] = useState(defaultRequest);
  const [status, setStatus] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await createJob({ ...form, client_id: Number(form.client_id) });
      setStatus('submitted');
      setForm(defaultRequest);
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold text-white">Client Job Requests</h1>
        <p className="text-sm text-slate-400">Submit repair orders and track progress in real time.</p>
      </header>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-lg border border-slate-800 bg-slate-900/50 p-6 shadow"
      >
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="flex flex-col text-sm">
            RO Number
            <input
              name="ro_number"
              value={form.ro_number}
              onChange={handleChange}
              required
              className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            />
          </label>
          <label className="flex flex-col text-sm">
            VIN
            <input
              name="vin"
              value={form.vin}
              onChange={handleChange}
              required
              className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            />
          </label>
          <label className="flex flex-col text-sm">
            Client ID
            <input
              name="client_id"
              value={form.client_id}
              onChange={handleChange}
              required
              className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            />
          </label>
          <label className="flex flex-col text-sm sm:col-span-2">
            Notes
            <textarea
              name="client_notes"
              value={form.client_notes}
              onChange={handleChange}
              rows={4}
              className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            />
          </label>
        </div>
        <button
          type="submit"
          className="rounded bg-brand px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-dark"
        >
          Submit Request
        </button>
        {status === 'submitted' ? (
          <p className="text-sm text-green-400">Request submitted! The team will confirm shortly.</p>
        ) : null}
        {status === 'error' ? (
          <p className="text-sm text-red-400">Unable to submit. Please retry in a moment.</p>
        ) : null}
      </form>
    </section>
  );
}

export default ClientPortal;
