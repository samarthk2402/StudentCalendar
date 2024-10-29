import React from "react";
import { Button, Modal, Form, Spinner, Alert } from "react-bootstrap";
import classchartslogo from "../assets/classchartslogo.png";
import { useState, useEffect } from "react";
import { CheckCircleFill } from "react-bootstrap-icons";

const ClassChartsLogin = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const [show, setShow] = useState(false);
  const [loadingLogin, setLoadingLogin] = useState(false);

  const [linked, setLinked] = useState(false);
  const [loading, setLoading] = useState(true);

  const [code, setCode] = useState(null);
  const [dob, setDOB] = useState(null);

  const [alert, setAlert] = useState("");

  const checkIfLinked = async () => {
    try {
      const res = await fetch(apiUrl + "classcharts/verify", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
          "Content-Type": "application/json",
        },
      });

      const data = await res.json();
      console.log(data);
      if (res.ok) {
        setLinked(true);
      } else {
        setLinked(false);
      }
    } catch (error) {
      console.log(error);
      setLinked(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkIfLinked();
  });

  const handleLogin = async (e) => {
    console.log(dob);
    e.preventDefault();
    setLoadingLogin(true);
    try {
      const res = await fetch(apiUrl + "classcharts/login", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: code,
          dob: dob,
        }),
      });

      const data = await res.json();
      if (data.error) {
        setAlert(data.error);
      } else {
        setAlert(data.message);
      }
      console.log(data);
    } catch (error) {
      const data = await res.json();
      console.log(error);
    } finally {
      setLoadingLogin(false);
      setCode(null);
      setDOB(null);
      setShow(false);
    }
  };
  return (
    <div style={{ marginRight: "20px" }}>
      {loading ? null : linked ? (
        <div>
          <img
            style={{ width: "30px", marginRight: "10px" }}
            src={classchartslogo}
            alt="ClassCharts Logo"
          />
          Account Synced
        </div>
      ) : (
        <Button
          variant="dark"
          style={{ padding: "5px" }}
          onClick={() => {
            setShow(true);
            setAlert("");
          }}
        >
          <div>
            <img
              style={{ width: "30px", marginRight: "10px" }}
              src={classchartslogo}
              alt="ClassCharts Logo"
            />
            Sync with classcharts
          </div>
        </Button>
      )}

      <Modal
        show={show}
        onHide={() => setShow(false)}
        style={{ padding: "20px" }}
      >
        <Modal.Header style={{ marginTop: "10px", marginBottom: "10px" }}>
          Login to Classcharts account
        </Modal.Header>
        <Form onSubmit={(e) => handleLogin(e)}>
          <Modal.Body>
            <Form.Group controlId="code" style={{ marginBottom: "20px" }}>
              <Form.Label>Code</Form.Label>
              <Form.Control
                type="name"
                placeholder="ABCD123"
                required={true}
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </Form.Group>
            <Form.Group controlId="dob" style={{ marginBottom: "20px" }}>
              <Form.Label>Date of Birth</Form.Label>
              <Form.Control
                type="date"
                value={dob}
                required={true}
                onChange={(e) => setDOB(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            {loadingLogin ? (
              <Spinner />
            ) : (
              <Button
                style={{ padding: "5px" }}
                variant="primary"
                type="submit"
              >
                Link
              </Button>
            )}
            {alert === "" ? null : <Alert>{alert}</Alert>}
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
};

export default ClassChartsLogin;
