import React, { useState, useEffect } from "react";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const getGoogleProfile = async () => {
    const options = {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
        "Content-Type": "application/json",
      },
    };

    const res = await fetch(apiUrl + "user/google/profile", options);

    try {
      const data = await res.json();
      setName(data.name);
      setEmail(data.email);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getGoogleProfile();
  }, []);

  return (
    <>
      <h1>Welcome to the home page {name}</h1>
      <h2>{email}</h2>
    </>
  );
};

export default Home;
