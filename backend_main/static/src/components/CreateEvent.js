import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Dialog from "@material-ui/core/Dialog/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle/DialogTitle";
import DialogActions from "@material-ui/core/DialogActions/DialogActions";
import Button from "@material-ui/core/Button/Button";
import DialogContent from "@material-ui/core/DialogContent/DialogContent";
import TextField from "@material-ui/core/TextField/TextField";
import { withStyles } from "@material-ui/core";
// import Select from 'react-select';
import ImageUploader from "./ImageUploader";
import TagField from "./TagField";
import Autocomplete from "./Autocomplete";
import connect from "react-redux/es/connect/connect";
import {
	SET_EVENT_NAME, SET_EVENT_DESCRIPTION, SET_EVENT_START_DATE, SET_EVENT_END_DATE, SET_EVENT_PUBLIC,
	SET_EVENT_ROOM, SET_EVENT_LOCATION
} from "../redux/event";

let google = null;
let mapCenter = null;
let placesService = null;
const radius = 5000;

class CreateEvent extends Component {
	state = {
		image: null, name: "", room: "", location: null,
		from: this.stringFromDate(this.defaultStartTime()),
		to: this.stringFromDate(this.defaultEndTime()), description: "", tags: [],
		roomSuggestions: [],
		locationSuggestions: [],
		visitedLocations: [] // JS Objects of API Call of All Locations
	};

	constructor(props) {
		super(props);
		google = window.google;
		//center at Day hall
		mapCenter = new google.maps.LatLng(42.44701, -76.48327);
		const map = new google.maps.Map(document.createElement('div'), {
			center: mapCenter,
			zoom: 15
		});
		placesService = new google.maps.places.PlacesService(map);

		// const url = 'http://cuevents-app.herokuapp.com/app/loc/all/';
		// fetch(url)
		// 	.then(res => res.json())
		// 	.then(json => {
		// 		this.setState({ visitedLocations: json.parse });
		// 	})
		// 	.catch((error) => {
		// 		console.log(error);
		// 	});
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
	autocompleteLocation(input) {
		if (input.length < 3)
			return;
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
	}
	autocompleteRoom(input) {
		if (input.length < 2)
			return;

		if (this.state.visitedLocations === undefined) {
			return;
		}

		const matchLocation = this.state.visitedLocations.filter(location => (location.building).includes(input));
		this.setState({
			roomSuggestions: matchLocation.map(loc => ({ name: loc.name, place_id: loc.place_id }))
		})
	}

	canPublish() {
		return this.props.event.eventName !== null && this.props.event.eventDesc !== undefined &&
			this.props.event.startDate !== undefined && this.props.event.endDate !== undefined &&
			this.props.event.room !== undefined && this.props.event.location !== undefined;
	}

	tryToPublish() {
		setTimeout(() => {
			console.log("try to publish");
			if (this.canPublish())
				this.props.onPublish();
			else
				this.tryToPublish();
		}, 20);
	}

	onPublishEvent() {
		this.props.setName(this.state.name);
		this.props.setDescription(this.state.description);
		this.props.setStartTime(this.state.to);
		this.props.setEndTime(this.state.from);
		this.props.setRoom(this.state.room);
		this.props.setLocation(this.state.location);

		this.tryToPublish();
		// this.props.onPublish();
	}
	render() {
		const { classes } = this.props;
		return (
			<Dialog open={this.props.open} scroll={"body"}>
				<DialogTitle>Create an Event</DialogTitle>
				<DialogContent className={classes.content}>
					<ImageUploader onImageChange={image => this.setState({ image })}
						shape={"rectangle"} />
					<TextField
						label="Event name"
						value={this.state.name}
						onChange={e => this.setState({ name: e.target.value })}
						margin={"normal"} />
					<Autocomplete
						label={"Room"}
						value={this.state.selected}
						data={this.state.roomSuggestions.map(loc =>
							({ value: loc.name, label: loc.name }))}
						onChange={this.autocompleteRoom.bind(this)}
						onUpdate={val => this.setState({ location: val })}
						placeholder={"Building + room to display (e.g. Gates G01)"}
						multiSelect={false}
						canCreate={true} />
					<Autocomplete
						label={"Google Maps location"}
						value={this.state.selected}
						data={this.state.locationSuggestions.map(loc =>
							({ value: loc.name, label: loc.name }))}
						onChange={this.autocompleteLocation.bind(this)}
						onUpdate={val => this.setState({ location: val })}
						placeholder={"Building to navigate to (e.g. Bill and Melinda Gates Hall)"}
						multiSelect={false}
						canCreate={false} />
					<TextField
						label="From"
						value={this.state.from}
						onChange={e => this.setState({ from: e.target.value })}
						type={"datetime-local"}
						margin={"normal"}
						InputLabelProps={{ shrink: true }} />
					<TextField
						label="To"
						value={this.state.to}
						onChange={e => this.setState({ to: e.target.value })}
						type={"datetime-local"}
						margin={"normal"}
						InputLabelProps={{ shrink: true }} />
					<TextField
						label="Description"
						value={this.state.description}
						onChange={e => this.setState({ description: e.target.value })}
						multiline={true}
						margin={"normal"} />
					<TagField onNewTags={(tags) => this.setState({ tags: tags })} />
				</DialogContent>
				<DialogActions>
					<Button onClick={this.props.onCancel} color="secondary">
						Cancel
					</Button>
					<Button onClick={this.onPublishEvent.bind(this)} color="primary">
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
	onPublish: PropTypes.func.isRequired,

	setName: PropTypes.func.isRequired,
	setDescription: PropTypes.func.isRequired,
	setStartTime: PropTypes.func.isRequired,
	setEndTime: PropTypes.func.isRequired,
	setPublic: PropTypes.func.isRequired,
	setRoom: PropTypes.func.isRequired,
	setLocation: PropTypes.func.isRequired
};

const styles = (theme) => ({
	content: {
		display: 'flex',
		flexDirection: 'column'
	}
});

function mapStateToProps(state) {
	return {
		event: state.event
	};
}

function mapDispatchToProps(dispatch) {
	return {
		setName: (name) => dispatch({ type: SET_EVENT_NAME, value: name }),
		setDescription: (description) => dispatch({ type: SET_EVENT_DESCRIPTION, value: description }),
		setStartTime: (startTime) => dispatch({ type: SET_EVENT_START_DATE, value: startTime }),
		setEndTime: (endTime) => dispatch({ type: SET_EVENT_END_DATE, value: endTime }),
		setPublic: (isPublic) => dispatch({ type: SET_EVENT_PUBLIC, value: isPublic }),
		setRoom: (room) => dispatch({ type: SET_EVENT_ROOM, value: room }),
		setLocation: (location) => dispatch({ type: SET_EVENT_LOCATION, value: location })
	}
}

CreateEvent = connect(mapStateToProps, mapDispatchToProps)(CreateEvent)
export default withStyles(styles)(CreateEvent);