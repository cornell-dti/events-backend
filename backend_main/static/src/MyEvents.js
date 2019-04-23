import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import Button from "@material-ui/core/Button/Button";
import Icon from "@material-ui/core/Icon/Icon";
import CreateEvent from "./components/CreateEvent";
import EventCard from "./components/EventCard";
import GridList from "@material-ui/core/GridList/GridList";
import PropTypes from 'prop-types';
import connect from "react-redux/es/connect/connect";
import axios from 'axios';
import Cookies from 'js-cookie';

class MyEvents extends Component {

	state = { createEvent: false, selectedEvent: {}, editEvent: false, events: [], deleteEvent: false };

	componentDidMount() {
		axios.get('/api/get_events/')
			.then(response => {
				let org_events = response.data;
				console.log(org_events)
				this.setState({ events: org_events })
			})
			.catch(error => {
				if (error.response && error.response.status === 404)
					this.setState({ errors: ['An error has occurred while retrieving your events. Please try again later.'] })
			})
	}
	formatTime(time) {
		const [hour, minute, second] = time.split(":");
		const hour12 = hour % 12 === 0 ? 12 : hour % 12; //0 o'clock = 12AM
		const am_pm = hour < 12 ? 'AM' : 'PM';
		return `${hour12}:${minute} ${am_pm}`;
	}
	formatMonth(date) {
		const [year, month, day] = date.split("-");
		const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Oct", "Nov", "Dec"]
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

	/*updateEvent(origEvent, updatedEvent) {
		origEvent.name = updatedEvent.name;
		// origEvent.image = updatedEvent.image
		origEvent.location = updatedEvent.location;
		origEvent.start_date = updatedEvent.start_date;
		origEvent.end_date = updatedEvent.end_date;
		origEvent.start_time = updatedEvent.start_time;
		origEvent.end_time = updatedEvent.end_time;
		origEvent.description = updatedEvent.description;
		// origEvent.tags = updatedEvent.tags

		return origEvent
	}*/

	onUpdate(event) {
		axios.post('/api/add_or_edit_event/', event)
			.then(response => {
				const updatedEvent = response.data
				let events = this.state.events.slice()
				let edit = false;
				for (let i = 0; i < events.length; i++){
					if (events[i].pk === updatedEvent.pk){
						events[i] = updatedEvent	
						edit = true;
						break;
					}
				}
				this.setState({ createEvent: false, editEvent: false, events: edit ? events: [...this.state.events, updatedEvent]})
			})
			.catch(error => this.setState({ errors: error.response.data.messages }))
	}
	
	onDeleteEvent(event) {
		let modifiedEvents = this.state.events.filter(e => { return e.pk !== event.pk });
		this.setState({ events: modifiedEvents, createEvent: false });
		axios.post('/api/delete_event/' + event.pk + '/')
			.catch(error => {
				if (error.response && (error.response.status === 404 || error.response.status === 405))
					this.setState({ errors: ['An error has occurred while deleting your event. Please try again later.'] })
			})
	}

	render() {
		const { classes } = this.props;
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
			tags: []
		};


		return (
			<div className={classes.root}>
				<Button variant={"fab"} color={"primary"} className={classes.fab} onClick={() => this.setState({ createEvent: true, editEvent: false, selectedEvent: newEvent })}>
					<Icon>add</Icon>
				</Button>
				<GridList className={classes.cardsContainer} cellHeight={"auto"} cols={3} spacing={50}>
					{this.state.events.map(event => 
						<div key={`${event.pk}`}>
							<EventCard
								name={event.name}
								location={event.location}
								numAttendees={event.num_attendees}
								imageUrl={"https://***REMOVED***.s3.amazonaws.com/" + event.media[event.media.length- 1].link}
								startTime={this.formatTime(event.start_time)}
								startMonth={this.formatMonth(event.start_date)}
								startDay={this.formatDay(event.start_date)}
								onClick={() => this.onEdit(event)} />
						</div>
					)}
				</GridList>
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

const styles = (theme) => ({
	root: {
		padding: theme.spacing.unit * 4,
		alignSelf: 'stretch'
	},
	cardsContainer: {
		width: '100%'
	},
	fab: {
		position: 'absolute',
		right: theme.spacing.unit * 4
	}
});

export default withStyles(styles)(MyEvents);
