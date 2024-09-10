import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { GoogleOAuthProvider } from "@react-oauth/google";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <GoogleOAuthProvider clientId="1086056028133-gdsavhkbqdhnls4luen4ccteoaat7ogi.apps.googleusercontent.com">
    <App />
  </GoogleOAuthProvider>
);
