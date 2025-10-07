import { useMemo } from 'react';

import Charts from '../components/Charts.jsx';
import { useJobs } from '../context/JobContext.jsx';

function AdminPanel() {
  const { jobs } = useJobs();

  const stats = useMemo(() => {
    const total = jobs.length;
    const completed = jobs.filter((job) => job.status === 'completed').length;
    const completionRate = total ? Math.round((completed / total) * 100) : 0;
    return {
      total,
      completed,
      completionRate,
    };
  }, [jobs]);

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold text-white">Admin Control Center</h1>
        <p className="text-sm text-slate-400">
          Review platform performance, manage permissions, and coordinate regional operations.
        </p>
      </header>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-5">
          <p className="text-sm text-slate-400">Total Jobs</p>
          <p className="mt-2 text-2xl font-semibold text-white">{stats.total}</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-5">
          <p className="text-sm text-slate-400">Completed</p>
          <p className="mt-2 text-2xl font-semibold text-white">{stats.completed}</p>
        </div>
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-5">
          <p className="text-sm text-slate-400">Completion Rate</p>
          <p className="mt-2 text-2xl font-semibold text-white">{stats.completionRate}%</p>
        </div>
      </div>

      <Charts data={{ jobsCompleted: stats.completed }} />

      <section className="rounded-lg border border-slate-800 bg-slate-900/50 p-6">
        <h2 className="text-lg font-semibold text-white">Security & Compliance</h2>
        <ul className="mt-3 list-disc space-y-2 pl-6 text-sm text-slate-300">
          <li>Ensure all technician devices have the latest FieldService mobile app build.</li>
          <li>Rotate admin JWT secrets quarterly and audit accounts monthly.</li>
          <li>Enable region-based access policies in Google Cloud IAM.</li>
        </ul>
      </section>
    </section>
  );
}

export default AdminPanel;
