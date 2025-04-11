import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <h2>Dashboard</h2>
          {/*<button onClick={handleLogout}>Logout</button>*/}
          {user && (
            <button
              onClick={handleLogout}
              style={{
                padding: '0.5rem 1rem',
                background: '#f44336',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          )}
        </div>
        {user && (
          <p>
            Welcome to the Business CRM system. You are logged in as {user.username}.
            You have access to manage users and companies in the system.
          </p>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;