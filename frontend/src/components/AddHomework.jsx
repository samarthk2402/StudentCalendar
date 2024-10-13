import React, { useState } from "react";
import { Spinner, Button, Form, Modal, Alert } from "react-bootstrap";
import { PlusLg, CheckCircleFill } from "react-bootstrap-icons";

const AddHomework = ({ onAdd }) => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const [show, setShow] = useState(false);
  const [showAlert, setShowAlert] = useState("");

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const [homeworkDescription, setHomeworkDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [completionTime, setCompletionTime] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const options = {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: homeworkDescription,
        estimated_completion_time: completionTime,
        due_date: dueDate,
      }),
    };

    console.log(options);

    try {
      const res = await fetch(apiUrl + "gcalendar/homework/add", options);
      const data = await res.json();
      onAdd();
      setShowAlert("success");
    } catch (err) {
      console.log(err);
      setShowAlert("danger");
    } finally {
      setLoading(false); // Set loading to false once the request completes (success or error)
      handleClose();
    }

    setHomeworkDescription("");
    setDueDate("");
    setCompletionTime("");
  };

  return (
    <>
      <div>
        <Button
          style={{ borderRadius: "100%", padding: "5px" }}
          variant="secondary"
          onClick={handleShow}
        >
          <PlusLg style={{ fontSize: "30px" }} />
        </Button>
        {showAlert !== "" ? (
          <Alert
            style={{
              marginTop: "20px",
            }}
            variant={showAlert}
            dismissible
            closeVariant="black"
          >
            <CheckCircleFill
              style={{
                color: "#28a745",
                marginRight: "10px",
                fontSize: "20px",
              }}
            />
            {showAlert === "success"
              ? "Homework added to calendar!"
              : "There was a problem adding this homework to your calendar!"}
          </Alert>
        ) : null}
      </div>

      <Modal show={show} onHide={handleClose} style={{ padding: "20px" }}>
        <Modal.Header style={{ marginTop: "10px", marginBottom: "10px" }}>
          New Homework
        </Modal.Header>

        <Form onSubmit={(e) => handleFormSubmit(e)}>
          <Modal.Body>
            <Form.Group
              controlId="description"
              style={{ marginBottom: "20px" }}
            >
              <Form.Label>Description</Form.Label>
              <Form.Control
                type="name"
                placeholder="E.g. Maths homework: Circle Theorems"
                required={true}
                value={homeworkDescription}
                onChange={(e) => setHomeworkDescription(e.target.value)}
              />
            </Form.Group>

            <Form.Group controlId="formDate" style={{ marginBottom: "20px" }}>
              <Form.Label>Select a Due Date</Form.Label>
              <Form.Control
                type="date"
                value={dueDate}
                required={true}
                onChange={(e) => setDueDate(e.target.value)}
              />
            </Form.Group>

            <Form.Group controlId="formTime" style={{ marginBottom: "20px" }}>
              <Form.Label>Estimated Completion Time (in minutes)</Form.Label>
              <Form.Control
                type="number"
                value={completionTime}
                placeholder="Enter time in minutes"
                min="1" // Ensure that user cannot input negative numbers
                required={true}
                onChange={(e) => setCompletionTime(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            {loading ? (
              <Spinner />
            ) : (
              <Button
                style={{ padding: "5px" }}
                variant="primary"
                type="submit"
              >
                Add to Calendar
              </Button>
            )}
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
};

export default AddHomework;
