function Filters({ filters, onChange }) {
  const handleChange = (event) => {
    const { name, value } = event.target;
    onChange?.({ ...filters, [name]: value });
  };

  return (
    <section className="flex flex-wrap items-center gap-4 rounded-lg border border-slate-800 bg-slate-900/50 p-4 text-sm">
      <div className="flex flex-col">
        <label className="text-slate-400" htmlFor="status">
          Status
        </label>
        <select
          id="status"
          name="status"
          value={filters.status ?? ''}
          onChange={handleChange}
          className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
        >
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="assigned">Assigned</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      <div className="flex flex-col">
        <label className="text-slate-400" htmlFor="region">
          Region
        </label>
        <select
          id="region"
          name="region"
          value={filters.region ?? ''}
          onChange={handleChange}
          className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
        >
          <option value="">All</option>
          <option value="north">North</option>
          <option value="south">South</option>
          <option value="east">East</option>
          <option value="west">West</option>
        </select>
      </div>
      <div className="flex flex-col">
        <label className="text-slate-400" htmlFor="search">
          Search
        </label>
        <input
          id="search"
          name="search"
          value={filters.search ?? ''}
          onChange={handleChange}
          placeholder="Search VIN or RO…"
          className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white focus:border-brand focus:outline-none"
        />
      </div>
    </section>
  );
}

export default Filters;
