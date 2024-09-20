import React, { useState } from "react";
import { Container, Button, Form } from "react-bootstrap";
import { PlusLg } from "react-bootstrap-icons";

const AddHomework = () => {
  const [dueDate, setDueDate] = useState();
  const [completionTime, setCompletionTime] = useState();

  const validateDate = (date) => {
    // A simple check if the date is valid
    const isValidDate = !isNaN(new Date(date).getTime());
    setIsValid(isValidDate);
  };
  return (
    <Container fluid>
      <h5 style={{ marginTop: "10px", marginBottom: "10px" }}>Add Homework</h5>
      <Form>
        <Form.Group controlId="description" style={{ marginBottom: "20px" }}>
          <Form.Label>Description</Form.Label>
          <Form.Control
            type="email"
            placeholder="E.g. Maths homework: Circle Theorems"
          />
        </Form.Group>

        <Form.Group controlId="formDate" style={{ marginBottom: "20px" }}>
          <Form.Label>Select a Due Date</Form.Label>
          <Form.Control type="date" value={dueDate} />
        </Form.Group>

        <Form.Group controlId="formTime" style={{ marginBottom: "20px" }}>
          <Form.Label>Estimated Completion Time (in minutes)</Form.Label>
          <Form.Control
            type="number"
            value={completionTime}
            placeholder="Enter time in minutes"
            min="1" // Ensure that user cannot input negative numbers
          />
        </Form.Group>
        <div className="d-flex justify-content-end">
          <Button
            style={{ borderRadius: "100%", padding: "5px" }}
            variant="secondary"
          >
            <PlusLg style={{ fontSize: "30px" }} />
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default AddHomework;
