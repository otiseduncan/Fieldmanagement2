import { useMemo, useState } from 'react';

import Filters from '../components/Filters.jsx';
import JobCard from '../components/JobCard.jsx';
import JobForm from '../components/JobForm.jsx';
import { useJobs } from '../context/JobContext.jsx';

function TechnicianDashboard() {
  const { jobs, isLoading } = useJobs();
  const [filters, setFilters] = useState({ status: 'pending' });
  const [selectedJob, setSelectedJob] = useState(null);

  const filteredJobs = useMemo(() => {
    return jobs.filter((job) => {
      if (filters.status && job.status !== filters.status) return false;
      if (filters.search) {
        const term = filters.search.toLowerCase();
        if (!job.vin.toLowerCase().includes(term) && !job.ro_number.toLowerCase().includes(term)) {
          return false;
        }
      }
      return true;
    });
  }, [jobs, filters]);

  return (
    <section className="space-y-6">
      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-semibold text-white">Technician Job Pool</h1>
        <p className="text-sm text-slate-400">
          Pull jobs from the pool, review ADAS requirements, and log completion status.
        </p>
      </header>

      <Filters filters={filters} onChange={setFilters} />

      {isLoading ? (
        <p className="text-sm text-slate-400">Loading jobs…</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {filteredJobs.map((job) => (
            <JobCard key={job.id} job={job} onSelect={setSelectedJob} />
          ))}
          {!filteredJobs.length ? (
            <p className="col-span-full text-sm text-slate-400">No jobs match the selected filters.</p>
          ) : null}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <div>
          <h2 className="text-lg font-semibold text-white">Create / Update Job</h2>
          <JobForm onSubmit={(values) => console.log('submit', values)} initialValues={selectedJob ?? undefined} />
        </div>
        <aside className="space-y-3 rounded-lg border border-slate-800 bg-slate-900/50 p-4 text-sm text-slate-300">
          <h3 className="text-base font-semibold text-white">VIN Intelligence</h3>
          <p>
            Pulls VIN + ADAS metadata to surface calibration requirements before a job begins. Hook into
            the backend `/api/v1/jobs/{id}` integration to display dynamic content here.
          </p>
        </aside>
      </div>
    </section>
  );
}

export default TechnicianDashboard;
