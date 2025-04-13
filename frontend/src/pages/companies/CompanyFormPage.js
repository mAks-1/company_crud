import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../../context/AuthContext";
import { useNavigate, useParams } from "react-router-dom";

const CompanyFormPage = () => {
  const { user: currentUser, token } = useAuth();
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    company_name: "",
    company_address: "",
    company_email: "",
    company_phone: "",
    company_description: "",
  });

  const isEditMode = id && id !== "new";

  useEffect(() => {
    if (isEditMode) {
      const fetchCompany = async () => {
        setLoading(true);
        try {
          const response = await axios.get(`/api/companies/${id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          setFormData({
            company_name: response.data.company_name || "",
            company_address: response.data.company_address || "",
            company_email: response.data.company_email || "",
            company_phone: response.data.company_phone || "",
            company_description: response.data.company_description || "",
          });
        } catch (err) {
          handleApiError(err, "fetching company");
        } finally {
          setLoading(false);
        }
      };
      fetchCompany();
    }
  }, [id, token, isEditMode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleApiError = (err, context = "") => {
    console.error(`Error ${context}:`, err);
    if (err.response?.status === 422) {
      const errorData = err.response.data.detail;
      setError(
        Array.isArray(errorData)
          ? errorData.map((e) => e.msg).join(", ")
          : errorData.msg || "Validation error",
      );
    } else {
      setError(
        err.response?.data?.detail || `Error ${context}. Please try again.`,
      );
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      };

      if (isEditMode) {
        await axios.patch(`/api/companies/${id}`, formData, config);
      } else {
        await axios.post("/api/companies/", formData, config);
      }
      navigate("/companies");
    } catch (err) {
      handleApiError(err, "submitting form");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4">
          {isEditMode ? "Edit Company" : "Create New Company"}
        </h2>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Company Name - Always editable */}
          <div>
            <label className="block text-gray-700 mb-2">Company Name *</label>
            <input
              type="text"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
          </div>

          {/* Address - Editable in both modes */}
          <div>
            <label className="block text-gray-700 mb-2">Address</label>
            <input
              type="text"
              name="company_address"
              value={formData.company_address}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            />
          </div>

          {/* Contact Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-700 mb-2">Email</label>
              <input
                type="email"
                name="company_email"
                value={formData.company_email}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-gray-700 mb-2">Phone</label>
              <input
                type="tel"
                name="company_phone"
                value={formData.company_phone}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-gray-700 mb-2">Description</label>
            <textarea
              name="company_description"
              value={formData.company_description}
              onChange={handleChange}
              rows={3}
              className="w-full p-2 border rounded"
            />
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={() => navigate("/companies")}
              className="px-4 py-2 border rounded hover:bg-gray-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className={`px-4 py-2 rounded text-white ${loading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"}`}
            >
              {loading
                ? "Processing..."
                : isEditMode
                  ? "Update Company"
                  : "Create Company"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CompanyFormPage;
