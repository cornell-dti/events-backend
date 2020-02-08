import React, { Component } from "react";
import PropTypes from "prop-types";
import Dialog from "@material-ui/core/Dialog/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle/DialogTitle";
import DialogActions from "@material-ui/core/DialogActions/DialogActions";
import Button from "@material-ui/core/Button/Button";
import DialogContent from "@material-ui/core/DialogContent/DialogContent";
import TextField from "@material-ui/core/TextField/TextField";

import DateFnsUtils from '@date-io/date-fns';
import { MuiPickersUtilsProvider, DateTimePicker } from '@material-ui/pickers';

import { withStyles } from "@material-ui/core";
import ImageUploader from "./ImageUploader";
import TagField from "./TagField";
import Autocomplete from "./Autocomplete";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";
import ReactGA from "react-ga";

let google = null;
let mapCenter = null;
let placesService = null;
const radius = 5000;

axios.defaults.headers.post["X-CSRFToken"] = Cookies.get("csrftoken"); //get CSRF-token for POST requests

class CreateEvent extends Component {
  state = {
    selected: {},
    pk: undefined,
    name: "",
    room: "",
    location: "",
    place_id: "",
    from: this.defaultStartTime(),
    to: this.defaultEndTime(),
    description: "",
    tags: [],
    imageUrl: "",

    errors: [],
    roomSuggestions: [],
    locationSuggestions: [],
    visitedLocations: [], // JS Objects of API Call of All Locations

    image: null,
    imageChanged: false
  };

  componentDidUpdate(prevProps) {
    var event = this.props.event;

    if (prevProps.event !== event && event !== {}) {
      try {
        event.tags = event.tags.map(tag => ({
          value: tag.id,
          label: tag.name
        }));
      } catch (err) {}

      this.setState({
        pk: event.pk,
        name: event.name,
        room: event.location.room,
        location: event.location.building,
        place_id: event.location.place_id,
        from:
          event.start_date === "" || event.start_time === ""
            ? this.defaultStartTime()
            : new Date((event.start_date + " " + event.start_time).replace(/-/g, "/")),
        to:
          event.end_date === "" || event.end_time === ""
            ? this.defaultEndTime()
            : new Date((event.end_date + " " + event.end_time).replace(/-/g, "/")),
        description: event.description,
        tags: event.tags,
        imageUrl:
          event.media.length > 0
            ? event.media.sort(
                (a, b) => Date.parse(b.uploaded_at) - Date.parse(a.uploaded_at)
              )[0].link
            : "",
        selected: {
          value: event.location.place_id,
          label: event.location.building
        }
      });
    }
  }
  constructor(props) {
    super(props);
    google = window.google;
    //center at Day hall
    mapCenter = new google.maps.LatLng(42.44701, -76.48327);
    const map = new google.maps.Map(document.createElement("div"), {
      center: mapCenter,
      zoom: 15
    });
    placesService = new google.maps.places.PlacesService(map);
  }

  formComplete() {
    return (
      this.state.name !== undefined &&
      this.state.name !== "" &&
      this.state.room !== undefined &&
      this.state.room !== "" &&
      this.state.location !== undefined &&
      this.state.location !== "" &&
      this.state.from !== undefined &&
      this.state.from !== "" &&
      this.state.to !== undefined &&
      this.state.to !== "" &&
      new Date(this.state.from) <= new Date(this.state.to)
    );
  }

  //tomorrow, same hour, 0 minutes
  defaultStartTime() {
    let now = new Date();
    now.setDate(now.getDate() + 1);
    now.setMinutes(0);
    return now;
  }
  //start time + 1 hour
  defaultEndTime() {
    let start = this.defaultStartTime();
    start.setHours(start.getHours() + 1);
    return start;
  }
  stringFromDate(date) {
    return date.toISOString().slice(0, 16);
  }

  autocompleteLocation = _.debounce(input => {
    if (input.length < 2) return;
    const request = { name: input, location: mapCenter, radius: radius };
    placesService.nearbySearch(request, (res, status) => {
      if (status !== google.maps.places.PlacesServiceStatus.OK) {
        console.log("Place services error");
        return;
      }

      this.setState({
        locationSuggestions: res.map(loc => ({
          name: loc.name,
          place_id: loc.place_id
        }))
      });
    });
  }, 1000);

  autocompleteRoom(input) {
    if (input.length < 2) return;

    if (this.state.visitedLocations === undefined) {
      return;
    }

    const matchLocation = this.state.visitedLocations.filter(location =>
      location.building.includes(input)
    );
    this.setState({
      roomSuggestions: matchLocation.map(loc => ({
        name: loc.name,
        place_id: loc.place_id
      }))
    });
  }

  uploadImage(callback) {
    const file = this.state.image;
    const fileType = file.type.replace("image/", "");


    if (fileType.length == file.type.length) {
      alert("Could not upload image. Please use a different file type");
    }

    
    const data = new FormData();
    data.append("file", file);

    console.log(file);
    axios.post(`/api/upload_image_s3/?file_name=${file.name}&file_type=${fileType}`, data, {
    }).then(res => {
        console.log(res.data);
        callback(res.data.url.split("/").slice(3).join("/"));
    }).catch(err => {
        alert(`Could not upload image! Reason: ${err}`);
    });
  }

  async onPublishEvent() {
    let imageUrl = "";
    const location = {
      building: this.state.location,
      room: this.state.room,
      place_id: this.state.place_id
    };

    if (this.state.imageChanged) {
      let promise = new Promise((res, req) =>
        this.uploadImage(url => res(url))
      );
      imageUrl = await promise;
    }

    // Changing the Type
    const isFromDate = this.state.from instanceof Date;
    const isToDate = this.state.to instanceof Date;

    const formattedFromDate = new Date(this.state.from);
    const formattedToDate = new Date(this.state.to);
    
    const eventData = {
      pk: this.state.pk,
      name: this.state.name,
      location: location,
      start_date: isFromDate ? this.state.from.toLocaleDateString() : formattedFromDate.toLocaleDateString(), 
      end_date: isFromDate ? this.state.to.toLocaleDateString() : formattedToDate.toLocaleTimeString(),
      start_time: isToDate ? this.state.from.toLocaleTimeString() : formattedFromDate.toLocalTimeString(), 
      end_time: isToDate ? this.state.to.toLocaleTimeString() : formattedToDate.toLocaleTimeString(),
      description: this.state.description,
      tags: this.state.tags,
      imageUrl: imageUrl
    };

    ReactGA.event({
      category: 'User',
      action: 'Added an Event'
    });

    this.setState({ imageChanged: false });
    this.props.onUpdate(eventData);
  }

  onDeleteEvent() {
    ReactGA.event({
      category: 'User',
      action: 'Deleted an Event'
    });
    const event = this.props.event;
    this.props.onDelete(event);
  }

  onCancelEvent() {
    // restore to old value
  }

  render() {
    const { classes } = this.props;

    return (
      <Dialog open={this.props.open} scroll={"body"}>
        {this.props.edit ? (
          <DialogTitle>Edit an Event</DialogTitle>
        ) : (
          <DialogTitle>Create an Event</DialogTitle>
        )}
        <DialogContent className={classes.content}>
          <ImageUploader
            image_url={this.state.imageUrl}
            onImageChange={image =>
              this.setState({ image: image, imageChanged: true })
            }
            shape={"rectangle"}
          />
          <TextField
            label="Event name *"
            value={this.state.name}
            onChange={e => this.setState({ name: e.target.value })}
          />
          {/* <Autocomplete
						label={"Room"}
						value={this.state.selected}
						data={this.state.roomSuggestions.map(loc =>
							({ value: loc.name, label: loc.name }))}
						onChange={this.autocompleteRoom.bind(this)}
						onUpdate={val => this.setState({ room: val })}
						placeholder={"Building + room to display (e.g. Gates G01)"}
						multiSelect={false}
						canCreate={true} /> */}
          <TextField
            label={"Room *"}
            value={this.state.room}
            placeholder={"Building + room to display (e.g. Gates G01)"}
            onChange={e => this.setState({ room: e.target.value })}
            margin={"normal"}
          />
          <Autocomplete
            label={"Google Maps location *"}
            value={this.state.selected}
            data={this.state.locationSuggestions.map(loc => ({
              value: loc.place_id,
              label: loc.name
            }))}
            onChange={this.autocompleteLocation.bind(this)}
            onUpdate={data =>
              this.setState({ location: data.label, place_id: data.value })
            }
            placeholder={"Building to navigate to (e.g. Bill and Melinda Gates Hall)"}
            multiSelect={false}
            canCreate={false}
            margin={"normal"}
          />
          <MuiPickersUtilsProvider utils={DateFnsUtils}>
            <DateTimePicker
                label="From *"
                margin={"normal"}
                minDate={new Date()}
                value={this.state.from}
                onChange={e => {
                  this.setState({from : e})
              }}
            />
            <DateTimePicker
                label="To *"
                margin={"normal"}
                minDate={this.state.from}
                value={this.state.to}
                onChange={e => this.setState({to : e})}
            />
          </MuiPickersUtilsProvider>
          <TextField
            label="Description"
            value={this.state.description}
            onChange={e => this.setState({ description: e.target.value })}
            multiline={true}
            margin={"normal"}
          />
          <TagField
            tags={this.state.tags}
            onNewTags={tags => this.setState({ tags: tags })}
          />
        </DialogContent>
        <DialogActions>
          {this.props.edit ? (
            <Button onClick={this.onDeleteEvent.bind(this)} color="primary">
              {" "}
              Delete{" "}
            </Button>
          ) : null}
          <Button onClick={this.props.onCancel} color="secondary">
            Cancel
          </Button>
          <Button
            onClick={this.onPublishEvent.bind(this)}
            disabled={!this.formComplete()}
            color="primary"
          >
            Publish Event
          </Button>
        </DialogActions>
      </Dialog>
    );
  }
}

CreateEvent.propTypes = {
  open: PropTypes.bool.isRequired,
  onCancel: PropTypes.func.isRequired,
  edit: PropTypes.bool.isRequired,
  event: PropTypes.object.isRequired
};

const styles = theme => ({
  content: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-around",
    width: '36vw',
    padding: theme.spacing(4)
  }
});

export default withStyles(styles)(CreateEvent);
