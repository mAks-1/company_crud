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

  const isEditMode = id && id !== 'new';

  useEffect(() => {
    if (isEditMode) {
      const fetchCompany = async () => {
        setLoading(true);
        try {
          const response = await axios.get(`/api/companies/${id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
          });

          if (response.data) {
            setFormData({
              company_name: response.data.company_name ?? '',
              company_address: response.data.company_address ?? '',
              company_email: response.data.company_email ?? '',
              company_phone: response.data.company_phone ?? '',
              company_description: response.data.company_description ?? '',
            });

          }
        } catch (err) {
          console.error('Error fetching company:', err);
          // Покращена обробка помилок
          if (err.response) {
            if (err.response.status === 422) {
              const errorData = err.response.data.detail;
              if (Array.isArray(errorData)) {
                setError(errorData.map(e => e.msg).join(', '));
              } else {
                setError(errorData.msg || 'Validation error');
              }
            } else {
              setError(err.response.data?.detail || 'Failed to fetch company');
            }
          } else {
            setError('Network error or server is not responding');
          }
        } finally {
          setLoading(false);
        }
      };
      fetchCompany();
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
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      };

      if (isEditMode) {
        await axios.patch(`/api/companies/${id}`, formData, config);
      } else {
        await axios.post('/api/companies/', formData, config);
      }
      navigate('/companies');
    } catch (err) {
      console.error('Error submitting form:', err);
      if (err.response?.status === 422) {
        const errorData = err.response.data.detail;
        if (Array.isArray(errorData)) {
          setError(errorData.map(e => e.msg).join(', '));
        } else {
          setError(errorData.msg || 'Validation failed');
        }
      } else {
        setError(err.response?.data?.detail || 'Operation failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <div className="card">
        <h2>{isEditMode ? 'Edit Company' : 'Create New Company'}</h2>
        {error && (
            <div className="error">
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </div>
        )}

        <form onSubmit={handleSubmit}>
          <div>
            <label>Company Name</label>
            <input
                type="text"
                name="company_name"
                value={formData.company_name || ''}
                onChange={handleChange}
                required
            />
          </div>

          <div>
            <label>Address</label>
            <input
                type="text"
                name="company_address"
                value={formData.company_address || ''}
                onChange={handleChange}
            />
          </div>

          <div>
            <label>Email</label>
            <input
                type="email"
                name="company_email"
                value={formData.company_email || ''}
                onChange={handleChange}
            />
          </div>

          <div>
            <label>Phone</label>
            <input
                type="tel"
                name="company_phone"
                value={formData.company_phone || ''}
                onChange={handleChange}
            />
          </div>

          <div>
            <label>Description</label>
            <textarea
                name="company_description"
                value={formData.company_description || ''}
                onChange={handleChange}
                rows={3}
            />
          </div>

          <button type="submit" className="px-4 py-2 mt-4 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            {isEditMode ? 'Update Company' : 'Create Company'}
          </button>
          <button type="button" onClick={() => navigate('/users')}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
};

export default CompanyFormPage;