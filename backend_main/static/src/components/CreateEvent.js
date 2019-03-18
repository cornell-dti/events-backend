import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Dialog from "@material-ui/core/Dialog/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle/DialogTitle";
import DialogActions from "@material-ui/core/DialogActions/DialogActions";
import Button from "@material-ui/core/Button/Button";
import DialogContent from "@material-ui/core/DialogContent/DialogContent";
import TextField from "@material-ui/core/TextField/TextField";
import { withStyles } from "@material-ui/core";
import ImageUploader from "./ImageUploader";
import TagField from "./TagField";
import Autocomplete from "./Autocomplete";
import axios from 'axios';

let google = null;
let mapCenter = null;
let placesService = null;
const radius = 5000;

class CreateEvent extends Component {
	state = {
		pk: -1,
		image: null,
		name: "",
		room: "",
		location: null,
		placeid: "",
		from: this.stringFromDate(this.defaultStartTime()),
		to: this.stringFromDate(this.defaultEndTime()),
		description: "",
		tags: [],
		errors: [],
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

		// will this update ?? check
		const editEvent = this.props.edit

		if (editEvent !== null) {
			this.setState({
				pk: this.editEvent.pk,
				name: this.editEvent.name,
				room: this.editEvent.room,
				location: this.editEvent.location,
				place_id: this.editEvent.place_id,
				from: this.editEvent.start_date + 'T' + this.editEvent.start_time,
				to: this.editEvent.end_date + 'T' + this.editEvent.end_time,
				description: this.editEvent.description,
				tags: this.editEvent.tags
			})
		}
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

	onPublishEvent() {
		const eventData = {
			pk: this.state.pk,
			name: this.state.name,
			room: this.state.room,
			location: this.state.location,
			place_id: this.state.place_id,
			start_date: this.state.from.split('T')[0],
			end_date: this.state.to.split('T')[0],
			start_time: this.state.from.split('T')[1],
			end_time: this.state.to.split('T')[1],
			description: this.state.description
		}

		if (this.state.pk === -1) {
			axios.post('/api/add_event/', eventData)
				.then(response => window.location.href = "/app/events/")
				.catch(error => this.setState({ errors: error.response.data.messages }));
		}
		else {
			axios.post('/api/edit_event/', eventData)
				.then(response => window.location.href = "/app/events/")
				.catch(error => this.setState({ errors: error.response.data.messages }));
		}
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
					{/* <Autocomplete
						label={"Room"}
						value={this.state.selected}
						data={this.state.roomSuggestions.map(loc =>
							({ value: loc.name, label: loc.name }))}
						onChange={this.autocompleteRoom.bind(this)}
						onUpdate={val => this.setState({ location: val })}
						placeholder={"Building + room to display (e.g. Gates G01)"}
						multiSelect={false}
						canCreate={true} /> */}
					<TextField
						label={"Room"}
						value={this.state.room}
						onChange={e => this.setState({ room: e.target.value })}
						margin={"normal"} />
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
	// edit: PropTypes.func.isRequired
};

const styles = (theme) => ({
	content: {
		display: 'flex',
		flexDirection: 'column'
	}
});

export default withStyles(styles)(CreateEvent);