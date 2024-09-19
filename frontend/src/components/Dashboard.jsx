import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card } from "react-bootstrap";

const Dashboard = () => {
  const apiUrl = import.meta.env.VITE_API_URL;

  const [week, setWeek] = useState({});
  const [daysOfWeek, setDaysOfWeek] = useState([]);
  const [calEvents, setCalEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const formatTime = (dateTimeString) => {
    const date = new Date(dateTimeString);
    const hours = date.getHours();
    const minutes = date.getMinutes();
    return `${hours}:${minutes < 10 ? "0" : ""}${minutes}`;
  };

  // Initialize and reorder days of the week
  useEffect(() => {
    const originalDaysOfWeek = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ];

    const currentDayIndex = new Date().getDay();
    const reorderedDaysOfWeek = [
      ...originalDaysOfWeek.slice(currentDayIndex),
      ...originalDaysOfWeek.slice(0, currentDayIndex),
    ];

    setDaysOfWeek(reorderedDaysOfWeek);
  }, []);

  // Update the week state when daysOfWeek is set
  useEffect(() => {
    let updatedWeek = {};

    for (let day of daysOfWeek) {
      updatedWeek[day] = [];
    }

    setWeek(updatedWeek);
  }, [daysOfWeek]);

  const getDayOfWeek = (dateString) => {
    const date = new Date(dateString);
    const originalIndex = date.getDay(); // Get day index from Date object (0 for Sunday, 1 for Monday, etc.)

    // Calculate the offset based on the reordered days
    const daysOfWeekLength = daysOfWeek.length;
    const currentDayIndex = new Date().getDay(); // Index of current day in the reordered array
    const adjustedIndex =
      (originalIndex + daysOfWeekLength - currentDayIndex) % daysOfWeekLength;

    return daysOfWeek[adjustedIndex];
  };

  const getCalendar = async () => {
    const options = {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`, // Send the token
        "Content-Type": "application/json",
      },
    };

    try {
      const res = await fetch(apiUrl + "gcalendar/events", options);
      const data = await res.json();
      const updatedEvents = data.events.map((event) => ({
        ...event,
        dayOfWeek: getDayOfWeek(event.start.dateTime),
      }));
      setCalEvents(updatedEvents);

      let updatedWeek = { ...week };

      for (let day of daysOfWeek) {
        updatedWeek[day] = updatedEvents.filter(
          (event) => event.dayOfWeek === day
        );
      }

      setWeek(updatedWeek);
      console.log(updatedWeek);
      setLoading(false);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getCalendar();
  }, [daysOfWeek]);

  return (
    <Container fluid>
      {loading ? (
        <h5>Loading Calendar ...</h5>
      ) : (
        <>
          <h5 style={{ marginTop: "10px", marginBottom: "10px" }}>Dashboard</h5>
          <Col>
            {Object.keys(week).map((day, index) => (
              <Row key={index} className="mb-3">
                <Col xs={12} md={12}>
                  <Card
                    className="h-100"
                    style={{
                      border: "1px solid #ddd", // Thin outline
                      borderRadius: "10px", // Curved edges
                      padding: "10px", // Padding inside the card
                    }}
                  >
                    <h5 style={{ fontSize: "18px" }}>{day}</h5>
                    <div className="text-secondary">
                      {week[day] && week[day].length > 0
                        ? week[day].map((event, index) => (
                            <Card
                              className="bg-secondary text-white"
                              style={{
                                paddingLeft: "10px", // Increase padding
                                borderRadius: "15px", // Increase border radius
                              }}
                              key={index}
                            >
                              {formatTime(event.start.dateTime) +
                                " - " +
                                formatTime(event.end.dateTime) +
                                "  " +
                                event.summary}
                            </Card>
                          ))
                        : "No events"}
                    </div>
                  </Card>
                </Col>
              </Row>
            ))}
          </Col>
        </>
      )}
    </Container>
  );
};

export default Dashboard;
