import axios from 'axios';

const storageClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

export async function uploadJobAsset({ jobId, file }) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('job_id', jobId);

  const response = await storageClient.post('/v1/jobs/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}
