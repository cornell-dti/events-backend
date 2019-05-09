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
import Cookies from 'js-cookie';
import FormError from './FormError'

let google = null;
let mapCenter = null;
let placesService = null;
const radius = 5000;

axios.defaults.headers.post['X-CSRFToken'] = Cookies.get('csrftoken') //get CSRF-token for POST requests

class CreateEvent extends Component {
	state = {
		selected: {},
		pk: undefined,
		name: "",
		room: "",
		location: "",
		place_id: "",
		from: this.stringFromDate(this.defaultStartTime()),
		to: this.stringFromDate(this.defaultEndTime()),
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
			try { event.tags = event.tags.map(tag => ({ value: tag.id, label: tag.name })) } catch (err) { }

			this.setState({
				pk: event.pk,
				name: event.name,
				room: event.location.room,
				location: event.location.building,
				place_id: event.location.place_id,
				from: event.start_date === "" || event.start_time === "" ? this.stringFromDate(this.defaultStartTime()) : event.start_date + 'T' + event.start_time.slice(0, 5),
				to: event.end_date === "" || event.end_time === "" ? this.stringFromDate(this.defaultEndTime()) : event.end_date + 'T' + event.end_time.slice(0, 5),
				description: event.description,
				tags: event.tags,
				imageUrl: event.media.length > 0 ? event.media.sort((a,b) => Date.parse(b.uploaded_at) - Date.parse(a.uploaded_at))[0].link : "",
				selected: { value: event.location.place_id, label: event.location.building }
			});
		}
	}
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
	}

	formComplete() {
		return this.state.name !== undefined && this.state.name !== "" &&
			this.state.room !== undefined && this.state.room !== "" &&
			this.state.location !== undefined && this.state.location !== "" &&
			this.state.from !== undefined && this.state.from !== "" &&
			this.state.to !== undefined && this.state.to !== ""
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
		});
	}

	uploadImage(callback){
		const file = this.state.image;
		const self = this;
		let xhr = new XMLHttpRequest();
		xhr.open("GET", "/api/sign_s3/?file_name="+file.name+"&file_type="+file.type);
		xhr.onreadystatechange = function(){
		    if(xhr.readyState === 4){
			    if(xhr.status === 200){
			    	console.log(xhr)
		        	const response = JSON.parse(xhr.responseText);
		        	
					xhr = new XMLHttpRequest();
					xhr.open("POST", response.data.url);

					let postData = new FormData();
					for(let key in response.data.fields){
					    postData.append(key, response.data.fields[key]);
					}
					postData.append('file', file);

					xhr.onreadystatechange = function() {
					    if(xhr.readyState === 4){
						    if(xhr.status === 200 || xhr.status === 204){
					        	console.log("File uploaded!");
					        	callback(response.url.split("/").slice(3).join("/"));
					      	}
					    	else{
						       	alert("Could not upload file.");
						    }
					 	}
					};
					xhr.send(postData);
		        	//self.uploadFile(file, response.data, response.url);
		      	}
		      	else{
		        	alert("Could not get signed URL.");
		      	}
		    }
		};
		xhr.send();
	}
	
	async onPublishEvent() {
		let imageUrl = ""
		const location = {
			building: this.state.location,
			room: this.state.room,
			place_id: this.state.place_id
		};

		if(this.state.imageChanged){
			let promise = new Promise((res, req) => this.uploadImage(url => res(url)))
			imageUrl = await promise;
		}
		
		const eventData = {
			pk: this.state.pk,
			name: this.state.name,
			location: location,
			start_date: this.state.from.split('T')[0],
			end_date: this.state.to.split('T')[0],
			start_time: this.state.from.split('T')[1],
			end_time: this.state.to.split('T')[1],
			description: this.state.description,
			tags: this.state.tags
			imageUrl: this.state.imageChanged ? imageUrl : ""
		};

		this.setState({ imageChanged: false });
		this.props.onUpdate(eventData);
	}

	onDeleteEvent() {
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
				{this.props.edit ? <DialogTitle>Edit an Event</DialogTitle> :
					<DialogTitle>Create an Event</DialogTitle>}
				<DialogContent className={classes.content}>
					<ImageUploader image_url={this.state.imageUrl} onImageChange={image => this.setState({ image: image, imageChanged: true })}
						shape={"rectangle"} />
					<TextField
						label="Event name *"
						value={this.state.name}
						onChange={e => this.setState({ name: e.target.value })}
						margin={"normal"} />
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
						margin={"normal"} />
					<Autocomplete
						label={"Google Maps location *"}
						value={this.state.selected}
						data={this.state.locationSuggestions.map(loc =>
							({ value: loc.place_id, label: loc.name }))}
						onChange={this.autocompleteLocation.bind(this)}
						onUpdate={data => this.setState({ location: data.label, place_id: data.value })}
						placeholder={"Building to navigate to (e.g. Bill and Melinda Gates Hall)"}
						multiSelect={false}
						canCreate={false} />
					<TextField
						label="From *"
						value={this.state.from}
						onChange={e => this.setState({ from: e.target.value })}
						type={"datetime-local"}
						margin={"normal"}
						InputLabelProps={{ shrink: true }} />
					<TextField
						label="To *"
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
					<TagField
						tags={this.state.tags}
						onNewTags={tags => this.setState({ tags: tags })}
					/>
				</DialogContent>
				<DialogActions>
					{this.props.edit ? <Button onClick={this.onDeleteEvent.bind(this)} color="primary"> Delete	</Button> : null}
					<Button onClick={this.props.onCancel} color="secondary">
						Cancel
					</Button>
					<Button onClick={this.onPublishEvent.bind(this)} disabled={!this.formComplete()} color="primary">
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

const styles = (theme) => ({
	content: {
		display: 'flex',
		flexDirection: 'column'
	}
});

export default withStyles(styles)(CreateEvent);