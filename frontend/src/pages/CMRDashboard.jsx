import Charts from '../components/Charts.jsx';
import JobCard from '../components/JobCard.jsx';
import { useJobs } from '../context/JobContext.jsx';

function CMRDashboard() {
  const { jobs } = useJobs();

  const queue = jobs.filter((job) => job.status === 'pending');
  const assigned = jobs.filter((job) => job.status === 'assigned');

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold text-white">CMR Dispatch Center</h1>
        <p className="text-sm text-slate-400">
          Balance technician workloads, respond to escalations, and keep clients informed.
        </p>
      </header>

      <Charts data={{ jobsCompleted: jobs.filter((job) => job.status === 'completed').length }} />

      <div className="grid gap-6 md:grid-cols-2">
        <section className="space-y-3">
          <h2 className="text-lg font-semibold text-white">Job Pool</h2>
          {queue.length ? (
            queue.map((job) => <JobCard key={job.id} job={job} />)
          ) : (
            <p className="text-sm text-slate-400">No jobs currently awaiting assignment.</p>)
          }
        </section>
        <section className="space-y-3">
          <h2 className="text-lg font-semibold text-white">Assigned</h2>
          {assigned.length ? (
            assigned.map((job) => <JobCard key={job.id} job={job} />)
          ) : (
            <p className="text-sm text-slate-400">No active assignments.</p>)
          }
        </section>
      </div>
    </section>
  );
}

export default CMRDashboard;
