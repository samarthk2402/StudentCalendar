import React, {
  useEffect,
  useState,
  useImperativeHandle,
  forwardRef,
} from "react";
import { Container, Row, Col, Card, Placeholder } from "react-bootstrap";

const Dashboard = forwardRef(({ homeworks }, ref) => {
  const apiUrl = import.meta.env.VITE_API_URL;

  const [week, setWeek] = useState({});
  const [daysOfWeek, setDaysOfWeek] = useState([]);
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

  const inHomeworks = (event) => {
    for (let homework of homeworks) {
      if (event.id === homework.event_id) {
        return true;
      } else if (homework.event_ids.includes(event.id)) {
        return true;
      }
    }
  };

  const getCalendar = async () => {
    setLoading(true);
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

      let updatedWeek = { ...week };

      for (let day of daysOfWeek) {
        updatedWeek[day] = updatedEvents.filter(
          (event) => event.dayOfWeek === day
        );
      }

      setWeek(updatedWeek);
      setLoading(false);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getCalendar();
  }, [daysOfWeek]);

  useImperativeHandle(ref, () => ({
    getCalendar,
  }));

  return (
    <Container fluid>
      <>
        <h5 style={{ marginTop: "10px", marginBottom: "10px" }}>Dashboard</h5>
        <Col>
          {Object.keys(week).map((day, index) => (
            <Row key={index} className="mb-3">
              <Col xs={12} md={12}>
                <Card
                  style={{
                    border: "1px solid #ddd", // Thin outline,
                    borderColor: "var(--bs-secondary)",
                    borderRadius: "10px", // Curved edges
                    padding: "10px", // Padding inside the card
                  }}
                >
                  {loading ? (
                    <>
                      <Placeholder as={Card.Title} animation="glow">
                        <Placeholder xs={1} style={{ borderRadius: "10px" }} />
                      </Placeholder>
                      <Placeholder as={Card.Text} animation="glow">
                        <Placeholder xs={12} style={{ borderRadius: "10px" }} />{" "}
                        <Placeholder xs={12} style={{ borderRadius: "10px" }} />
                      </Placeholder>
                    </>
                  ) : (
                    <>
                      <h5 style={{ fontSize: "18px" }}>{day}</h5>
                      <div className="text-secondary">
                        {week[day] && week[day].length > 0
                          ? week[day].map((event, index) => (
                              <Card
                                className={
                                  inHomeworks(event)
                                    ? "bg-secondary text-white"
                                    : "text-white"
                                }
                                style={{
                                  paddingLeft: "10px", // Increase padding
                                  borderRadius: "15px", // Increase border radius
                                  marginBottom: "10px",
                                }}
                                key={index}
                              >
                                {formatTime(event.start.dateTime) +
                                  " - " +
                                  formatTime(event.end.dateTime) +
                                  "   " +
                                  event.summary}
                              </Card>
                            ))
                          : "No events"}
                      </div>
                    </>
                  )}
                </Card>
              </Col>
            </Row>
          ))}
        </Col>
      </>
    </Container>
  );
});

export default Dashboard;
