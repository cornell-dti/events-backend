import React, { Component } from 'react';
import PropTypes from 'prop-types';
import AppBar from "@material-ui/core/AppBar/AppBar";
import Toolbar from "@material-ui/core/Toolbar/Toolbar";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";
import { withStyles } from "@material-ui/core";
import { Route, withRouter } from "react-router-dom";
import routes from './routes';
import LinkColorless from "./components/LinkColorless";
import Logo from "./components/Logo";
import Landing from "./Landing";
import axios from 'axios'

class Main extends Component {
	state = { loggedIn: false }

	componentDidMount(){
		let self = this;
		axios.get('/api/loggedin/')
		.then(function (response){
			self.setState({ loggedIn: response.data.status })
		})
	}

	getNavBar(classes) {
		switch (this.props.location.pathname) {
			case "/app/":
				if (!this.state.loggedIn)
					return (
						<React.Fragment>
							<Typography variant={"title"} color={"inherit"}>
								Are you an organization?
							</Typography>
							<LinkColorless to={routes.login.route}>
								<Button color={"primary"} className={classes.button}>
									Log in
								</Button>
							</LinkColorless>
							<LinkColorless to={routes.signup.route}>
								<Button variant={"outlined"} color={"primary"}
									className={classes.button}>
									Sign up
								</Button>
							</LinkColorless>
						</React.Fragment>
					);
			case routes.settings.route:
				return (
					<React.Fragment>
						<LinkColorless to={routes.profile.route}>
							<Button color={"primary"} className={classes.button}>
								Profile
							</Button>
						</LinkColorless>
						<LinkColorless to={routes.myEvents.route}>
							<Button color={"primary"} className={classes.button}>
								My Events
							</Button>
						</LinkColorless>
						<LinkColorless to={routes.logout.route} logout={true}>
							<Button color={"primary"} className={classes.button}>
								Log Out
							</Button>
						</LinkColorless>
					</React.Fragment>
				);
			case routes.myEvents.route:
				return (
					<React.Fragment>
						<LinkColorless to={routes.profile.route}>
							<Button color={"primary"} className={classes.button}>
								Profile
							</Button>
						</LinkColorless>
						<LinkColorless to={routes.settings.route}>
							<Button color={"primary"} className={classes.button}>
								Settings
							</Button>
						</LinkColorless>
						<LinkColorless to={routes.logout.route} logout={true}>
							<Button color={"primary"} className={classes.button}>
								Log Out
							</Button>
						</LinkColorless>
					</React.Fragment>
				);
			case routes.profile.route:
				return (
					<React.Fragment>
						<LinkColorless to={routes.settings.route}>
							<Button color={"primary"} className={classes.button}>
								Settings
							</Button>
						</LinkColorless>
						<LinkColorless to={routes.myEvents.route}>
							<Button color={"primary"} className={classes.button}>
								My Events
							</Button>
						</LinkColorless>
						<LinkColorless to={routes.logout.route} logout={true}>
							<Button color={"primary"} className={classes.button}>
								Log Out
							</Button>
						</LinkColorless>
					</React.Fragment>
				);
			default:
				return null;
		}
	}

	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<AppBar color={"default"}>
					<Toolbar>
						<LinkColorless to={"/app/"} style={{ flexGrow: 1 }}>
							<Logo fontSize={40} />
						</LinkColorless>
						{this.getNavBar(classes)}
					</Toolbar>
				</AppBar>
				<div className={classes.appBarSpace} />
				{this.props.location.pathname === "/app/"
					? <Landing /> : null}
				{Object.values(routes).map(obj => <Route key={obj.route} path={obj.route}
					component={obj.component} />)}
			</div>
		);
	}
}

Main.propTypes = {
	location: PropTypes.shape({
		pathname: PropTypes.string
	}).isRequired
};

const styles = (theme) => ({
	root: {
		flexGrow: 1,
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center'
	},
	appBarSpace: theme.mixins.toolbar,
	button: {
		marginLeft: theme.spacing.unit * 2
	}
});

export default withStyles(styles)(withRouter(Main));