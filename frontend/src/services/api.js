import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

client.interceptors.request.use((config) => {
  const token = window.localStorage.getItem('fs2_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function fetchJobs(token) {
  const response = await client.get('/v1/jobs', {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  return response.data;
}

export async function createJob(payload) {
  const response = await client.post('/v1/jobs', payload);
  return response.data;
}

export async function fetchClients() {
  const response = await client.get('/v1/clients');
  return response.data;
}

export async function fetchReports(jobId) {
  const response = await client.get(`/v1/reports/${jobId}/export`, {
    responseType: 'text',
  });
  return response.data;
}
