import { useState } from 'react';

const defaultForm = {
  ro_number: '',
  vin: '',
  client_id: '',
  client_notes: '',
};

function JobForm({ onSubmit, initialValues = defaultForm }) {
  const [form, setForm] = useState(initialValues);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit?.(form);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-lg border border-slate-800 bg-slate-900/50 p-4 shadow"
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col text-sm">
          RO Number
          <input
            name="ro_number"
            value={form.ro_number}
            onChange={handleChange}
            className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            required
          />
        </label>
        <label className="flex flex-col text-sm">
          VIN
          <input
            name="vin"
            value={form.vin}
            onChange={handleChange}
            maxLength={17}
            minLength={11}
            className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
            required
          />
        </label>
        <label className="flex flex-col text-sm">
          Client ID
          <input
            name="client_id"
            value={form.client_id}
            onChange={handleChange}
            className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
          />
        </label>
        <label className="flex flex-col text-sm sm:col-span-2">
          Notes
          <textarea
            name="client_notes"
            value={form.client_notes}
            onChange={handleChange}
            rows={3}
            className="mt-1 rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
          />
        </label>
      </div>
      <div className="mt-4 flex justify-end">
        <button
          type="submit"
          className="rounded bg-brand px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-dark"
        >
          Save Job
        </button>
      </div>
    </form>
  );
}

export default JobForm;
