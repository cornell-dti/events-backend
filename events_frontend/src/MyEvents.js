import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import Fab from '@material-ui/core/Fab';
import Icon from "@material-ui/core/Icon/Icon";
import CreateEvent from "./components/CreateEvent";
import EventCard from "./components/EventCard";
import GridList from "@material-ui/core/GridList/GridList";
import axios from "axios";
import PageNavigator from "./components/PageNavigator";
import routes from "./routes";
import ReactGA from "react-ga";

class MyEvents extends Component {
  state = {
    lastPage: 1,
    createEvent: false,
    selectedEvent: {},
    editEvent: false,
    events: [],
    deleteEvent: false
  };

  componentDidMount() {
    ReactGA.pageview(window.location.pathname + window.location.search);
    this.retrievePageEvents();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.match.params.id !== this.props.match.params.id) {
      this.retrievePageEvents();
    }
  }

  retrievePageEvents() {
    axios
      .get(`/api/get_events?page=${this.props.match.params.id || 1}`)
      .then(response => {
        // Response will tell you the page that was returned
        this.setState({
          events: response.data.events,
          lastPage: response.data.pages
        });
      })
      .catch(error => {
        if (error.response && error.response.status === 404)
          this.setState({
            errors: [
              "An error has occurred while retrieving your events. Please try again later."
            ]
          });
      });
  }
  formatTime(time) {
    const [hour, minute, second] = time.split(":");
    const hour12 = hour % 12 === 0 ? 12 : hour % 12; //0 o'clock = 12AM
    const am_pm = hour < 12 ? "AM" : "PM";
    return `${hour12}:${minute} ${am_pm}`;
  }
  formatMonth(date) {
    const [year, month, day] = date.split("-");
    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ];
    return `${months[month - 1]}`;
  }
  formatDay(date) {
    const [year, month, day] = date.split("-");
    return `${day}`;
  }
  onCancelCreate() {
    this.setState({ createEvent: false });
  }

  onEdit(event) {
    this.setState({ createEvent: true, selectedEvent: event, editEvent: true });
  }

  //have to dynamically update event since we are paginating
  onUpdate(event) {
    const url = event.pk ? "/api/edit_event/" : "/api/add_event/"
    axios
      .post(url, event)
      .then(response => {
        const updatedEvent = response.data;
        let events = this.state.events.slice();
        let edit = false;
        for (let i = 0; i < events.length; i++) {
          if (events[i].pk === updatedEvent.pk) {
            console.log(updatedEvent);
            console.log(event);
            events[i] = updatedEvent; // does not update fast enough with tags
            edit = true;
            break;
          }
        }
        if (edit) {
          this.setState({ events: events });
        } else {
          this.retrievePageEvents();
        }
        this.setState({
          createEvent: false,
          editEvent: false
        });
      })
      .catch(error => this.setState({ errors: error.response.data.messages }));
  }

  onDeleteEvent(event) {
    axios
      .post("/api/delete_event/" + event.pk + "/")
      .then(() => {
        this.retrievePageEvents();
        this.setState({ createEvent: false });
      })
      .catch(error => {
        if (
          error.response &&
          (error.response.status === 404 || error.response.status === 405)
        )
          this.setState({
            errors: [
              "An error has occurred while deleting your event. Please try again later."
            ]
          });
      });
  }

  render() {
    const { classes } = this.props;
    const currPage = parseInt(this.props.match.params.id) || 1;
    const newEvent = {
      image: null,
      name: "",
      location: {
        building: "",
        room: "",
        place_id: ""
      },
      start_date: "",
      end_date: "",
      start_time: "",
      end_time: "",
      description: "",
      tags: [],
      media: []
    };

    return (
      <div className={classes.root}>
        <Fab
          variant={"round"}
          color={"primary"}
          className={classes.fab}
          onClick={() =>
            this.setState({
              createEvent: true,
              editEvent: false,
              selectedEvent: newEvent
            })
          }
        >
          <Icon>add</Icon>
        </Fab>
        {this.state.events.length > 0 && (
          <GridList
            className={classes.cardsContainer}
            cellHeight={"auto"}
            cols={3}
            spacing={50}
          >
            {this.state.events.map(event => {
              let imageUrl =
                event.media.length > 0
                  ? event.media.sort(
                    (a, b) =>
                      Date.parse(b.uploaded_at) - Date.parse(a.uploaded_at)
                  )[0].link
                  : "";
              return (
                <div key={`${event.pk}`}>
                  <EventCard
                    name={event.name}
                    location={event.location}
                    numAttendees={event.num_attendees}
                    imageUrl={imageUrl} //for now take latest uploaded image
                    startTime={this.formatTime(event.start_time)}
                    startMonth={this.formatMonth(event.start_date)}
                    startDay={this.formatDay(event.start_date)}
                    onClick={() => this.onEdit(event)}
                  />
                </div>
              );
            })}
          </GridList>
        )}
        {this.state.lastPage !== 1 && currPage <= this.state.lastPage && (
          <PageNavigator
            currPage={currPage}
            lastPage={this.state.lastPage}
            prevPageLink={`${routes.auth.myEventsDefault.route}${currPage - 1}`}
            nextPageLink={`${routes.auth.myEventsDefault.route}${currPage + 1}`}
          />
        )}
        <CreateEvent
          open={this.state.createEvent}
          edit={this.state.editEvent}
          event={this.state.selectedEvent}
          onCancel={this.onCancelCreate.bind(this)}
          onUpdate={this.onUpdate.bind(this)}
          onDelete={this.onDeleteEvent.bind(this)}
        />
      </div>
    );
  }
}

const styles = theme => ({
  root: {
    padding: theme.spacing(4),
    marginBottom: "10vh",
    alignSelf: "stretch"
  },
  cardsContainer: {
    width: "98%"
  },
  fab: {
    position: "absolute",
    right: theme.spacing(4)
  }
});

export default withStyles(styles)(MyEvents);
