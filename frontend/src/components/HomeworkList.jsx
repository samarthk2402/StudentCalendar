import React, { useEffect, useState } from "react";
import { Container, ListGroup, Button, Spinner } from "react-bootstrap";

const HomeworkList = ({ homeworks, onDelete }) => {
  const apiUrl = import.meta.env.VITE_API_URL;

  const markAsCompleted = async (homework) => {
    const options = {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: homework.id,
      }),
    };

    try {
      const res = await fetch(apiUrl + "gcalendar/homework/delete", options);
      if (res.ok) {
        onDelete();
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <h5 style={{ marginTop: "10px", marginBottom: "10px" }}>Homeworks</h5>
      <ListGroup style={{ marginTop: "10px", marginBottom: "10px" }}>
        {homeworks !== null ? (
          homeworks.length > 0 ? (
            homeworks.map((homework, index) => (
              <ListGroup.Item
                key={index}
                style={{
                  textDecoration: homework.completed ? "line-through" : "none",
                }}
              >
                {homework.name}
                <Button
                  variant="outline-secondary"
                  size="sm"
                  style={{ float: "right" }}
                  onClick={() => markAsCompleted(homework)}
                  onMouseOver={(e) => {
                    e.currentTarget.parentElement.style.textDecoration =
                      "line-through";
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.parentElement.style.textDecoration =
                      homework.completed ? "line-through" : "none";
                  }}
                >
                  {homework.completed ? "Undo" : "Mark as completed"}
                </Button>
              </ListGroup.Item>
            ))
          ) : (
            <p>No homework</p>
          )
        ) : (
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        )}
      </ListGroup>
    </>
  );
};

export default HomeworkList;
