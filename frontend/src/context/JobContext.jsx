import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import { fetchJobs } from '../services/api.js';
import { useAuth } from './AuthContext.jsx';

const JobContext = createContext(undefined);

export function JobProvider({ children }) {
  const { token } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) {
      setJobs([]);
      return;
    }

    let ignore = false;
    setIsLoading(true);
    fetchJobs(token)
      .then((data) => {
        if (!ignore) {
          setJobs(data);
        }
      })
      .catch((err) => {
        if (!ignore) {
          setError(err);
        }
      })
      .finally(() => {
        if (!ignore) {
          setIsLoading(false);
        }
      });

    return () => {
      ignore = true;
    };
  }, [token]);

  const value = useMemo(
    () => ({ jobs, setJobs, isLoading, error }),
    [jobs, isLoading, error],
  );

  return <JobContext.Provider value={value}>{children}</JobContext.Provider>;
}

export function useJobs() {
  const context = useContext(JobContext);
  if (!context) {
    throw new Error('useJobs must be used within a JobProvider');
  }
  return context;
}
