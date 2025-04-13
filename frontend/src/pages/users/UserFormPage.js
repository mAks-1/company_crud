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
          // console.log("API Response:", response.data);
          // console.log("current user", currentUser);

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
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const dataToSend = isEditMode
        ? {
            ...formData,
            role: formData.role,
          }
        : formData;

      console.log("Sending PATCH:", dataToSend); // DEBUG ONLY

      if (isEditMode) {
        await axios.patch(`/api/users/${id}/`, dataToSend, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        await axios.post("/api/users/", dataToSend, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      navigate("/users");
    } catch (err) {
      setError(err.response?.data?.detail || "Operation failed");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{isEditMode ? "Edit User" : "Create New User"}</h2>
        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          {isEditMode ? null : (
            <div>
              <label>First name</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
              />
            </div>
          )}

          {isEditMode ? null : (
            <div>
              <label>Last name</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
              />
            </div>
          )}

          <div>
            <label>Username</label>
            {isEditMode ? (
              <p>{formData.username}</p>
            ) : (
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            )}
          </div>

          <div>
            <label>Email</label>
            {isEditMode ? (
              <p>{formData.email}</p>
            ) : (
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            )}
          </div>

          <div>
            <label>Role</label>
            {currentUser?.role === "Company manager" ||
            currentUser?.role === "Admin" ? (
              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                required
                // Забороняємо змінювати роль тільки для адмінів (якщо поточний користувач не адмін)
                disabled={
                  isEditMode &&
                  formData.role === "Admin" &&
                  currentUser?.role !== "Admin"
                }
              >
                <option value="Staff member">Staff member</option>
                <option value="Company manager">Company manager</option>
                {currentUser?.role === "Admin" && (
                  <option value="Admin">Admin</option>
                )}
              </select>
            ) : (
              <p>{formData.role}</p>
            )}
          </div>

          {!isEditMode && (
            <div>
              <label>Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          )}

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              {isEditMode ? "Update User" : "Create User"}
            </button>
            <button type="button" onClick={() => navigate("/users")}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserFormPage;
