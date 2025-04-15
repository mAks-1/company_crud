import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const CompaniesPage = () => {
  const { user: currentUser, token } = useAuth();
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await axios.get("/api/companies/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setCompanies(response.data);
      } catch (err) {
        console.error("Error:", err);
        setError(err.response?.data?.detail || "Failed to fetch companies");
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
  }, [token]);

  const handleDelete = async (companyId) => {
    if (window.confirm("Are you sure you want to delete this company?")) {
      try {
        await axios.delete(`/api/companies/${companyId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setCompanies(
          companies.filter((company) => company.company_id !== companyId),
        );
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to delete company");
      }
    }
  };

  if (loading) return <div className="loading">Loading companies...</div>;
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
          <h2>Companies Management</h2>
          {(currentUser?.role === "Company manager" ||
            currentUser?.role === "Admin") && (
            <button
              className="btn-success"
              onClick={() => navigate("/companies/new")}
            >
              Add New Company
            </button>
          )}
        </div>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Address</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Status</th>
              {(currentUser?.role === "Company manager" ||
                currentUser?.role === "Admin") && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {companies.map((company) => (
              <tr key={company.company_id}>
                <td>{company.company_id}</td>
                <td>{company.company_name}</td>
                <td>{company.company_address || "-"}</td>
                <td>{company.company_email || "-"}</td>
                <td>{company.company_phone || "-"}</td>
                <td>{company.active ? "Active" : "Inactive"}</td>
                {(currentUser?.role === "Company manager" ||
                  currentUser?.role === "Admin") && (
                  <td>
                    {/* Edit button - available for Admins and Company managers */}
                    <button
                      className="btn-edit"
                      onClick={() =>
                        navigate(`/companies/${company.company_id}`)
                      }
                    >
                      Edit
                    </button>

                    {/* Delete button - available for Admins and Company managers except for their own company if needed */}
                    <button
                      className="btn-danger"
                      onClick={() => handleDelete(company.company_id)}
                    >
                      Delete
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CompaniesPage;
