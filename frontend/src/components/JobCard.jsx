function JobCard({ job, onSelect }) {
  return (
    <article
      className="rounded-lg border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/30"
      onClick={() => onSelect?.(job)}
      role={onSelect ? 'button' : undefined}
      tabIndex={onSelect ? 0 : undefined}
    >
      <header className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{job.ro_number}</h3>
        <span className="rounded bg-slate-800 px-2 py-1 text-xs uppercase tracking-wide text-slate-300">
          {job.status}
        </span>
      </header>
      <dl className="mt-3 grid grid-cols-2 gap-2 text-sm text-slate-300">
        <div>
          <dt className="text-slate-500">VIN</dt>
          <dd className="font-mono text-xs">{job.vin}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Client</dt>
          <dd>{job.client?.name ?? 'Unassigned'}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Technician</dt>
          <dd>{job.technician?.full_name ?? 'Pool'}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Scheduled</dt>
          <dd>{job.scheduled_start ?? 'TBD'}</dd>
        </div>
      </dl>
    </article>
  );
}

export default JobCard;
