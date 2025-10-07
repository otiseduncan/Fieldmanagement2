import { createContext, useContext, useMemo, useState } from 'react';

const AuthContext = createContext(undefined);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => window.localStorage.getItem('fs2_token'));

  const login = (nextToken) => {
    setToken(nextToken);
    window.localStorage.setItem('fs2_token', nextToken);
  };

  const logout = () => {
    setToken(null);
    window.localStorage.removeItem('fs2_token');
  };

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      login,
      logout,
    }),
    [token],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
