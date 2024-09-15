import React, { useEffect } from "react";
import "./Login.css";

const Login = () => {
  return (
    <div className="login-container">
      <h1>Login</h1>
      <a
        href="https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/google/callback/&prompt=consent&response_type=code&client_id=1086056028133-gdsavhkbqdhnls4luen4ccteoaat7ogi.apps.googleusercontent.com&scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar&access_type=offline
"
      >
        <button className="google-signin-button">
          <span className="google-icon"></span>
          Sign in with Google
        </button>
      </a>
    </div>
  );
};

export default Login;
