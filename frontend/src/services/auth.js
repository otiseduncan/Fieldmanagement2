import axios from 'axios';

const authClient = axios.create({
  // Always use Vite dev server proxy in local/dev
  baseURL: '/api',
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
