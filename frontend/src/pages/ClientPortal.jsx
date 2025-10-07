import { useEffect, useState } from 'react';

import { createJob, fetchClients } from '../services/api.js';

const defaultRequest = {
  ro_number: '',
  vin: '',
  client_notes: '',
  client_id: '',
};

function ClientPortal() {
  const [form, setForm] = useState(defaultRequest);
  const [status, setStatus] = useState(null);
  const [clients, setClients] = useState([]);
  const [isLoadingClients, setIsLoadingClients] = useState(false);
  const [clientsError, setClientsError] = useState(null);

  useEffect(() => {
    let ignore = false;
    setIsLoadingClients(true);
    setClientsError(null);
    fetchClients()
      .then((data) => {
        if (!ignore) {
          setClients(data);
          if (data?.length && !form.client_id) {
            setForm((prev) => ({ ...prev, client_id: String(data[0].id) }));
          }
        }
      })
      .catch((err) => {
        if (!ignore) setClientsError(err);
      })
      .finally(() => {
        if (!ignore) setIsLoadingClients(false);
      });
    return () => {
      ignore = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
      // eslint-disable-next-line no-console
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
            Client
            <select
              name="client_id"
              value={form.client_id}
              onChange={handleChange}
              required
              className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            >
              {isLoadingClients ? (
                <option value="" disabled>
                  Loading clients...
                </option>
              ) : null}
              {!isLoadingClients && clients?.length === 0 ? (
                <option value="" disabled>
                  No clients found
                </option>
              ) : null}
              {clients?.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} (ID {c.id})
                </option>
              ))}
            </select>
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
        {clientsError ? (
          <p className="text-sm text-red-400">Unable to load clients. Refresh and try again.</p>
        ) : null}
      </form>
    </section>
  );
}

export default ClientPortal;

