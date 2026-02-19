import { BASE } from "./base_api_url";
import { createContext, useEffect, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function rehydrate() {
      try {
        const refreshRes = await fetch(`${BASE}/api/token/refresh/`, {
          method: "POST",
          credentials: "include",
        });

        if (!refreshRes.ok) throw new Error("No valid refresh");

        const refreshData = await refreshRes.json();
        const newAccess = refreshData.access;

        setAccessToken(newAccess);

        const meRes = await fetch(`${BASE}/api/me/`, {
          headers: {
            Authorization: `Bearer ${newAccess}`,
          },
        });

        if (!meRes.ok) throw new Error("Failed to fetch user");

        const userData = await meRes.json();
        setUser(userData);
      } catch (err) {
        setUser(null);
        setAccessToken(null);
      } finally {
        setLoading(false);
      }
    }

    rehydrate();
  }, []);

  const login = async (credentials) => {
    const res = await fetch(`${BASE}/api/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(credentials),
    });

    if (!res.ok) throw new Error("Login failed");

    const data = await res.json();

    setAccessToken(data.access);

    const meRes = await fetch(`${BASE}/api/me/`, {
      headers: {
        Authorization: `Bearer ${data.access}`,
      },
    });

    const userData = await meRes.json();
    setUser(userData);
  };

  const logout = async () => {
    setUser(null);
    setAccessToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        accessToken,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
