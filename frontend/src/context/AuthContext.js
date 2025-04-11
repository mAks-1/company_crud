import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // useEffect для завантаження даних користувача при старті
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          setLoading(true);
          const userResponse = await axios.get('/api/jwt/users/me/', {
            headers: { Authorization: `Bearer ${token}` },
          });
          setUser(userResponse.data);
        } catch (err) {
          console.error('Failed to load user', err);
          logout(); // токен недійсний - виходимо
        } finally {
          setLoading(false);
        }
      }
    };

    loadUser();
  }, [token]);

  const login = async (username, password) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post('/api/users/login/', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      localStorage.setItem('token', response.data.access_token);
      setToken(response.data.access_token);

      // Отримуємо дані користувача після входу
      const userResponse = await axios.get('/api/jwt/users/me/', {
        headers: { Authorization: `Bearer ${response.data.access_token}` },
      });
      setUser(userResponse.data);

      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout, loading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);