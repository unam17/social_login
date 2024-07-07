// src/components/Detail.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const Detail = () => {
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
    }
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>회원 상세정보</h1>
      <p>이름: {user.name}</p>
      <p>이메일: {user.email}</p>
      <p>휴대전화: {user.phone_number}</p>
    </div>
  );
};

export default Detail;
