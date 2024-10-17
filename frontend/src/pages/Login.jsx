import React from "react";
import { Container, Button } from "react-bootstrap";
import { Google } from "react-bootstrap-icons";
import "./Login.css";

const Login = () => {
  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <div style={{ textAlign: "center" }}>
        <h1 style={{ marginBottom: "20px" }}>Welcome</h1>
        <a href="https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/google/callback/&prompt=consent&response_type=code&client_id=1086056028133-gdsavhkbqdhnls4luen4ccteoaat7ogi.apps.googleusercontent.com&scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar&access_type=offline">
          <Button
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              textDecoration: "none",
            }}
          >
            <Google style={{ marginRight: "10px" }} />
            Sign in with Google
          </Button>
        </a>
      </div>
    </Container>
  );
};

export default Login;
