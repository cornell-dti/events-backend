import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import Button from "@material-ui/core/Button/Button";
import Icon from "@material-ui/core/Icon/Icon";
import CreateEvent from "./components/CreateEvent";
import EventCard from "./components/EventCard";
import GridList from "@material-ui/core/GridList/GridList";
import PropTypes from 'prop-types';
import connect from "react-redux/es/connect/connect";
import axios from 'axios'

// let DEMO_EVENTS = [{
// 	pk: 42,
// 	name: "Night at the Johnson",
// 	description: "Experience the magic of an after-hours event at Cornell's wonderful Johnson Museum with art, music, food, desserts, and drinks. Dress up or dress down and get ready for a fun time!",
// 	location: "Eddy St, Ithaca NY 14850",
// 	start_date: "2018-01-21",
// 	end_date: "2018-01-21",
// 	start_time: "19:30:00",
// 	end_time: "22:00:00",
// 	num_attendees: 39,
// 	is_public: true,
// 	organizer: 3,
// 	event_tags: [1, 2]
// }];

class MyEvents extends Component {

	state = { createEvent: false, selectedEvent: {}, editEvent: false, events: [] };

	componentDidMount() {
		axios.get('/api/get_events/')
			.then(response => {
				let org_events = response.data;
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
		return `${months[month-1]}`;
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
		}

		return (
			<div className={classes.root}>
				<Button variant={"fab"} color={"primary"} className={classes.fab} onClick={() => this.setState({ createEvent: true, editEvent: false, selectedEvent: newEvent })}>
					<Icon>add</Icon>
				</Button>
				<GridList className={classes.cardsContainer} cellHeight={"auto"} cols={3} spacing={50}>
					{this.state.events.map(event => (
						<div key={`${event.pk}`}>
							<EventCard
								name={event.name}
								location={event.location}
								numAttendees={event.num_attendees}
								startTime={this.formatTime(event.start_time)}
								startMonth={this.formatMonth(event.start_date)}
								startDay={this.formatDay(event.start_date)}
								onClick={() => this.onEdit(event)} />
						</div>
					))}
				</GridList>
				<CreateEvent 
					open={this.state.createEvent}
					edit={this.state.editEvent}
					event={this.state.selectedEvent}
					onCancel={this.onCancelCreate.bind(this)}
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
