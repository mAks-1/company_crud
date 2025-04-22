//UserPage
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const UsersPage = () => {
  const { user: currentUser, token } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get("/api/users/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsers(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to fetch users");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [token]);

  const handleDelete = async (userId) => {
    if (window.confirm("Are you sure you want to delete this user?")) {
      try {
        await axios.delete(`/api/users/${userId}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUsers(users.filter((user) => user.user_id !== userId));
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to delete user");
      }
    }
  };

  if (loading) return <div className="loading">Loading users...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="container">
      <div className="card">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <h2>Users Management</h2>
          {(currentUser?.role === "Company manager" ||
            currentUser?.role === "Admin") && (
            <button
              className="btn-success"
              onClick={() => navigate("/users/new")}
            >
              Add New User
            </button>
          )}
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              {(currentUser?.role === "Company manager" ||
                currentUser?.role === "Admin") && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.user_id}>
                <td>{user.user_id}</td>
                <td>{user.username}</td>
                <td>{user.email || "-"}</td>
                <td>{user.role}</td>
                <td>{user.active ? "Online" : "Offline"}</td>
                <td>
                  {(currentUser?.role === "Admin" ||
                    (currentUser?.role === "Company manager" &&
                      user.role !== "Admin")) && (
                    <button
                      onClick={() => navigate(`/users/${user.user_id}/`)}
                      className="btn-edit"
                    >
                      Edit
                    </button>
                  )}

                  {(currentUser?.role === "Company manager" &&
                    user.role !== "Admin") ||
                  (currentUser?.role === "Admin" &&
                    user.user_id !== currentUser?.user_id) ? (
                    <button
                      className="btn-danger"
                      onClick={() => handleDelete(user.user_id)}
                    >
                      Delete
                    </button>
                  ) : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UsersPage;
