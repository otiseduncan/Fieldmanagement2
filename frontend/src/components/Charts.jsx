function Charts({ data }) {
  return (
    <section className="rounded-lg border border-slate-800 bg-slate-900/60 p-6">
      <h2 className="text-lg font-semibold text-white">Performance Snapshot</h2>
      <p className="mt-2 text-sm text-slate-400">
        Charts will render here once analytics integration is connected. Current jobs completed this
        week: <span className="text-white">{data?.jobsCompleted ?? 0}</span>
      </p>
    </section>
  );
}

export default Charts;
