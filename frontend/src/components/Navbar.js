import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { logout, user, loading } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (window.confirm('Are you sure you want to logout?')) {
      try {
        await logout();
        navigate('/login', { replace: true });
      } catch (error) {
        console.error('Logout failed:', error);
        alert('Logout failed. Please try again.');
      }
    }
  };

  return (
    <nav style={{
      display: 'flex',
      padding: '1rem',
      background: '#333',
      color: 'white'
    }}>
      <Link style={{ color: 'white', marginRight: '1rem' }} to="/">Dashboard</Link>
      <Link style={{ color: 'white', marginRight: '1rem' }} to="/users">Users</Link>
      <Link style={{ color: 'white', marginRight: '1rem' }} to="/companies">Companies</Link>

      {user && (
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center' }}>
          <span style={{ marginRight: '1rem' }}>
            Welcome, {user.username} ({user.role})
          </span>
          <button
            onClick={handleLogout}
            disabled={loading}
            style={{
              padding: '0.5rem 1rem',
              background: '#d9534f',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {loading ? 'Logging out...' : 'Logout'}
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;