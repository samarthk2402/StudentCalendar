import React, { useState, useEffect } from "react";
import { Navbar, Container } from "react-bootstrap";
import "./Home.css";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [profilePictureUrl, setProfilePictureUrl] = useState(null);

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
      setProfilePictureUrl(data.picture_url);
      console.log(data.picture_url);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getGoogleProfile();
  }, []);

  return (
    <>
      <Navbar className="bg-body-tertiary">
        <Container fluid>
          <Navbar.Brand href="#home">Student Calendar</Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            <img src={profilePictureUrl} className="profilepicture" />
            <Navbar.Text>{name}</Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default Home;
