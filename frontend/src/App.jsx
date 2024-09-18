import React, { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";

function App() {
  return (
    <div className="app-container" data-bs-theme="dark">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
