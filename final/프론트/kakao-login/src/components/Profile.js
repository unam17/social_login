// src/components/Profile.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      axios.get('http://localhost:8000/accounts/profile/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        setUser(response.data);
      })
      .catch(error => {
        console.error(error);
      });
    } else {
      navigate('/');
    }
  }, [navigate]);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.name}님 환영합니다.</h1>
      <button onClick={() => navigate('/detail')}>상세정보</button>
    </div>
  );
};

export default Profile;
