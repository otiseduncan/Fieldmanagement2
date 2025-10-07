import axios from 'axios';

const authClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

authClient.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

authClient.interceptors.request.use((config) => {
  config.transformRequest = [
    (data) =>
      new URLSearchParams(
        Object.entries(data).map(([key, value]) => [key, value?.toString() ?? '']),
      ).toString(),
  ];
  return config;
});

export async function login({ username, password }) {
  const response = await authClient.post('/v1/auth/login', {
    username,
    password,
  });
  return response.data;
}
