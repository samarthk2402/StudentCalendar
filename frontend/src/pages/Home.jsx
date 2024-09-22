import React, { useState, useEffect, useRef } from "react";
import { Navbar, Container, Col, Row } from "react-bootstrap";
import "./Home.css";
import Dashboard from "../components/Dashboard";
import AddHomework from "../components/AddHomework";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const dashboardRef = useRef();

  const callGetCalendar = () => {
    if (dashboardRef.current) {
      dashboardRef.current.getCalendar();
    }
  };

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
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getGoogleProfile();
  }, []);

  return (
    <>
      <Navbar className="bg-body-secondary w-100">
        <Container fluid>
          <Navbar.Brand href="#home">Student Calendar</Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            <img src={profilePictureUrl} className="profilepicture" />
            <Navbar.Text>{name}</Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container fluid>
        <Row>
          {/* AddHomework takes up 3 columns (out of 12) */}
          <Col xs={12} md={4}>
            <AddHomework onAdd={callGetCalendar} />
          </Col>

          {/* Dashboard takes up 9 columns (out of 12) */}
          <Col xs={12} md={8}>
            <Dashboard ref={dashboardRef} />
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Home;
