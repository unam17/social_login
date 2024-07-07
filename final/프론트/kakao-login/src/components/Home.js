// src/components/Home.js

import React from 'react';

const Home = () => {
  const handleKakaoLogin = () => {
    window.location.href = 'http://localhost:8000/accounts/kakao/login/';
  };

  return (
    <div>
      <h1>Homepage</h1>
      <button onClick={handleKakaoLogin}>카카오 소셜 로그인</button>
    </div>
  );
};

export default Home;
