import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TextField from "@material-ui/core/TextField/TextField";
import { withStyles } from "@material-ui/core";
import Onboarding from "./components/Onboarding";
import routes from './routes';
import connect from "react-redux/es/connect/connect";
import { SET_ORG_EMAIL, SET_ORG_NAME, SET_PASSWORD } from "./redux/user";

class CreateOrg extends Component {
	state = { name: "", email: "", password: "", confirmPassword: "" };
	submitCreateUser = null;

	confirmPasswordError() {
		return this.state.password !== this.state.confirmPassword;
	}
	canContinue() {
		return this.state.name !== undefined && this.state.name !== "" &&
			this.state.email !== undefined && this.state.email !== "" &&
			this.state.password !== undefined && this.state.password !== "" &&
			!this.confirmPasswordError();
	}
	onClick() {
		this.props.setEmail(this.state.email);
		this.props.setPassword(this.state.password);
		this.props.setName(this.state.name);
		//TODO go somewhere
	}
	render() {
		const { classes } = this.props;
		return (
			<Onboarding
				title={"Create an Organization Account"}
				button={"Continue"}
				link={routes.verifyCornellStatus.route}
				canClick={this.canContinue()}
				onClick={this.onClick.bind(this)}>
				<TextField
					label="Organization name"
					className={classes.textField}
					value={this.state.name}
					onChange={e => this.setState({ name: e.target.value })}
					margin={"normal"} />
				<TextField
					label="Organization email"
					className={classes.textField}
					value={this.state.email}
					onChange={e => this.setState({ email: e.target.value })}
					margin={"normal"} />
				<TextField
					label="Password"
					className={classes.textField}
					value={this.state.password}
					onChange={e => this.setState({ password: e.target.value })}
					margin={"normal"}
					type={"password"} />
				<TextField
					label="Confirm password"
					className={classes.textField}
					value={this.state.confirmPassword}
					onChange={e => this.setState({ confirmPassword: e.target.value })}
					margin={"normal"}
					type={"password"}
					error={this.confirmPasswordError()}
					helperText={this.confirmPasswordError() ? "Passwords do not match" : ""} />
			</Onboarding>
		);
	}
}

const styles = (theme) => ({
	textField: {
		width: '100%',
		margin: theme.spacing.unit * 3
	}
});

CreateOrg.propTypes = {
	setName: PropTypes.func.isRequired,
	setEmail: PropTypes.func.isRequired,
	setPassword: PropTypes.func.isRequired
};

function mapStateToProps(state) {
	return {};
}
function mapDispatchToProps(dispatch) {
	return {
		setName: (name) => dispatch({ type: SET_ORG_NAME, value: name }),
		setEmail: (email) => dispatch({ type: SET_ORG_EMAIL, value: email }),
		setPassword: (password) => dispatch({ type: SET_PASSWORD, value: password })
	}
}

CreateOrg = connect(mapStateToProps, mapDispatchToProps)(CreateOrg);
export default withStyles(styles)(CreateOrg);
