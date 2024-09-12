import React, { useState } from "react";
import { useSearchParams } from "react-router-dom";

const Home = () => {
  const [searchParams] = useSearchParams();
  const name = searchParams.get("name");
  const email = searchParams.get("email");

  return (
    <>
      <h1>Welcome to the home page {name}</h1>
      <h2>{email}</h2>
    </>
  );
};

export default Home;
