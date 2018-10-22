import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import Button from "@material-ui/core/Button/Button";
import Icon from "@material-ui/core/Icon/Icon";
import CreateEvent from "./components/CreateEvent";
import EventCard from "./components/EventCard";
import GridList from "@material-ui/core/GridList/GridList";

const DEMO_EVENTS = [{
	pk: 42,
	name: "Night at the Johnson",
	description: "Experience the magic of an after-hours event at Cornell's wonderful Johnson Museum with art, music, food, desserts, and drinks. Dress up or dress down and get ready for a fun time!",
	location: "Eddy St, Ithaca NY 14850",
	start_date: "2018-01-21",
	end_date: "2018-01-21",
	start_time: "19:30:00",
	end_time: "22:00:00",
	num_attendees: 39,
	is_public: true,
	organizer: 3,
	event_tags: [1, 2]
}];

class MyEvents extends Component {
	state = { createEvent: false };

	formatTime(time) {
		const [hour, minute, second] = time.split(":");
		const hour12 = hour % 12 === 0 ? 12 : hour % 12; //0 o'clock = 12AM
		const am_pm = hour < 12 ? 'AM' : 'PM';
		return `${hour12}:${minute} ${am_pm}`;
	}
	onCancelCreate() {
		this.setState({ createEvent: false });
	}
	onPublishEvent() {
		this.setState({ createEvent: false });

	}
	editEvent(event) {
		this.setState({ createEvent: true });
	}
	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<Button variant={"fab"} color={"primary"} className={classes.fab} onClick={() => this.setState({ createEvent: true })}>
					<Icon>add</Icon>
				</Button>
				<GridList className={classes.cardsContainer} cellHeight={"auto"} cols={3} spacing={50}>
					{DEMO_EVENTS.map(event => (
						<div key={`${event.pk}`}>
							<EventCard
								name={event.name}
								location={event.location}
								numAttendees={event.num_attendees}
								startTime={this.formatTime(event.start_time)}
								onClick={() => this.editEvent(event)} />
						</div>
					))}
				</GridList>
				<CreateEvent open={this.state.createEvent}
					onCancel={this.onCancelCreate.bind(this)}
					onPublish={this.onPublishEvent.bind(this)} />
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
