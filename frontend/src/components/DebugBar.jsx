import { useAuth } from '../context/AuthContext.jsx';
import { useJobs } from '../context/JobContext.jsx';

function DebugBar() {
  let jobsInfo = 'n/a';
  try {
    const { jobs, isLoading } = useJobs();
    jobsInfo = isLoading ? 'loading' : `${jobs?.length ?? 0}`;
  } catch {
    // useJobs not available on unauthenticated routes
  }
  const { isAuthenticated } = useAuth();
  return (
    <div className="w-full bg-slate-900/80 px-4 py-1 text-xs text-slate-300">
      Debug • auth={String(isAuthenticated)} • jobs={jobsInfo}
    </div>
  );
}

export default DebugBar;

