import React, { useEffect } from "react";
import "./App.css";

function App() {
  useEffect(() => {
    // Ensure the Google Sign-In library is loaded before initializing
    if (window.google) {
      window.google.accounts.id.initialize({
        client_id:
          "1086056028133-2spjauti06ulp0gnp79u7rv030d1cgoc.apps.googleusercontent.com",
        callback: handleCredentialResponse,
      });

      // Render the Google Sign-In button
      window.google.accounts.id.renderButton(
        document.getElementById("buttonDiv"),
        {
          theme: "filled_black",
          size: "large",
          shape: "pill",
          text: "continue_with",
          logo_alignment: "left",
        }
      );
    }
  }, []);

  const handleCredentialResponse = (response) => {
    console.log("Encoded JWT ID token: " + response.credential);
    // Handle the response (e.g., send it to your server for verification)
  };

  return (
    <div className="app-container">
      <h1>Homework Scheduler</h1>
      {/* Div where the Google Sign-In button will be rendered */}
      <div id="buttonDiv"></div>
    </div>
  );
}

export default App;
