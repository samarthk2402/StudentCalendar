import React, { useState, useEffect, useRef } from "react";
import { Navbar, Container, Col, Row } from "react-bootstrap";
import "./Home.css";
import Dashboard from "../components/Dashboard";
import AddHomework from "../components/AddHomework";
import HomeworkList from "../components/HomeworkList";
import ClassChartsLogin from "../components/ClassChartsLogin";

const Home = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const dashboardRef = useRef();

  const [homework, setHomework] = useState(null);

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

  const getHomeworks = async () => {
    const options = {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
        "Content-Type": "application/json",
      },
    };

    try {
      const res = await fetch(apiUrl + "gcalendar/homework", options);
      const data = await res.json();
      console.log(data);
      setHomework(data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getGoogleProfile();
    getHomeworks();
  }, []);

  return (
    <>
      <Navbar className="bg-body-secondary w-100">
        <Container fluid>
          <Navbar.Brand>Student Calendar</Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            <ClassChartsLogin />
            <img
              src={profilePictureUrl}
              className="profilepicture"
              onError={(event) => {
                event.target.classList.add("hidden");
                console.log("Error with profile picture");
              }}
            />
            <Navbar.Text>{name}</Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container fluid>
        <Row>
          {/* Dashboard takes up 9 columns (out of 12) */}
          <Col xs={12} md={8}>
            <Dashboard ref={dashboardRef} homeworks={homework} />
          </Col>

          {/* AddHomework takes up 3 columns (out of 12) */}
          <Col xs={12} md={4}>
            <Container>
              <HomeworkList
                homeworks={homework}
                onDelete={() => {
                  callGetCalendar();
                  getHomeworks();
                }}
              />
              <AddHomework
                onAdd={() => {
                  callGetCalendar();
                  getHomeworks();
                }}
              />
            </Container>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Home;
