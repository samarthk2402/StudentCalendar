import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const apiUrl = import.meta.env.VITE_API_URL;
  console.log(apiUrl);
  const navigate = useNavigate();

  const [authenticated, setAuthenticated] = useState(null);

  useEffect(() => {
    const checkIfAuthenticated = async () => {
      const res = await fetch(apiUrl + "is-authenticated");
      if (res.ok) {
        setAuthenticated(true);
      } else {
        navigate("/login");
      }
    };

    checkIfAuthenticated();
  }, []);

  return authenticated ? children : <div>Loading</div>;
};

export default ProtectedRoute;
