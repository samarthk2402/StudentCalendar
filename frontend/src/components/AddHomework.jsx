import React, { useState } from "react";
import { Container, Button, Form, Spinner } from "react-bootstrap";
import { PlusLg } from "react-bootstrap-icons";

const AddHomework = ({ onAdd }) => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const [homeworkDescription, setHomeworkDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [completionTime, setCompletionTime] = useState("");

  const handleFormSubmit = async (e) => {
    e.preventDefault();

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

    try {
      const res = await fetch(apiUrl + "gcalendar/homework/add", options);
      const data = await res.json();
      window.alert(data.message);
      onAdd();
    } catch (err) {
      console.log(err);
    }

    setHomeworkDescription("");
    setDueDate("");
    setCompletionTime("");
  };

  return (
    <Container fluid>
      <h5 style={{ marginTop: "10px", marginBottom: "10px" }}>Add Homework</h5>
      <Form onSubmit={(e) => handleFormSubmit(e)}>
        <Form.Group controlId="description" style={{ marginBottom: "20px" }}>
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
        <div className="d-flex justify-content-end">
          <Button
            style={{ borderRadius: "100%", padding: "5px" }}
            variant="secondary"
            type="submit"
          >
            <PlusLg style={{ fontSize: "30px" }} />
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default AddHomework;
