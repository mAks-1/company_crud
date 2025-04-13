import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../../context/AuthContext";
import { useNavigate, useParams } from "react-router-dom";

const UserFormPage = () => {
  const { user: currentUser, token } = useAuth();
  // const { token } = useAuth();
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    role: "",
    active: "",
    password: "",
  });

  const isEditMode = id && id !== "new";

  useEffect(() => {
  if (isEditMode) {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`/api/users/${id}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        });
        console.log('API Response:', response.data); // Додайте логування
    if (!currentUser) return;

    if (isEditMode) {
      const fetchUser = async () => {
        setLoading(true);
        try {
          const response = await axios.get(`/api/users/${id}/`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          setFormData({
            first_name: response.data.first_name || "",
            last_name: response.data.last_name || "",
            username: response.data.username || "",
            email: response.data.email || "",
            password: "",
            role: response.data.role || "",
            active: response.data.active || "",
          });
        } catch (err) {
          console.error("Error fetching user:", err);
          setError(err.response?.data?.detail || "Failed to fetch user");
        } finally {
          setLoading(false);
        }
      };
      fetchUser();
    }
  }, [id, token, isEditMode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isEditMode) {
        await axios.patch(`/api/users/${id}/`, formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post('/api/users/', formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      navigate('/users');
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{isEditMode ? 'Edit User' : 'Create New User'}</h2>
        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div>
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          {/*<div>*/}
          {/*  <label>Role</label>*/}
          {/*  <select*/}
          {/*    name="role"*/}
          {/*    value={formData.role}*/}
          {/*    onChange={handleChange}*/}
          {/*    required*/}
          {/*  >*/}
          {/*    <option value="user">User</option>*/}
          {/*    <option value="admin">Admin</option>*/}
          {/*    <option value="manager">Manager</option>*/}
          {/*  </select>*/}
          {/*</div>*/}

          <div>
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required={!isEditMode}
              placeholder={isEditMode ? 'Leave blank to keep current' : ''}
            />
          </div>

          <button type="submit" disabled={loading}>
            {isEditMode ? 'Update User' : 'Create User'}
          </button>
          <button type="button" onClick={() => navigate('/users')}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
};

export default UserFormPage;