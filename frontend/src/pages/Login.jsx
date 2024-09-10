import React from "react";
import { GoogleLogin } from "@react-oauth/google";

const Login = () => {
  return (
    <div style={{ textAlign: "center" }}>
      <h1>Login</h1>
      <GoogleLogin
        onSuccess={() => console.log("success")}
        onError={() => console.log("Login Failed")}
      />
    </div>
  );
};

export default Login;
