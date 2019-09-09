import React, { Component } from 'react';
import TextField from "@material-ui/core/TextField/TextField";
import { withStyles } from "@material-ui/core";
import Onboarding from "./components/Onboarding";
import FormError from "./components/FormError";
import axios from 'axios';

class SignUp extends Component {
	state = {
		name: "",
		email: "",
		password: "",
		confirmPassword: "",
		errors: []
	};

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
		const self = this;
		const signUpData = {
			name: this.state.name,
			email: this.state.email,
			password1: this.state.password,
			password2: this.state.confirmPassword
		};

		axios.post('/api/signup/', signUpData)
			.then(() => window.location.href = "/events/")
			.catch(error => self.setState({ errors: error.response.data.messages }));
	}
	onEnter(e) {
		if (e.key === 'Enter') {
			document.getElementById("op-button").click();
		}
	}
	render() {
		const { classes } = this.props;

		return (
			<div className={classes.root}>
			<Onboarding
				title={"Create an Organization Account"}
				button={"Continue"}
				canClick={this.canContinue()}
				onClick={this.onClick.bind(this)} >
				<FormError errors={this.state.errors} />
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
					helperText={this.confirmPasswordError() ? "Passwords do not match" : ""}
					onKeyPress={this.onEnter.bind(this)}
				/>
			</Onboarding>
			</div>
		);
	}
}

const styles = (theme) => ({
	root: {
		marginBottom: '10%'
	},
	textField: {
		width: '100%',
		margin: theme.spacing.unit * 3
	}
});

export default withStyles(styles)(SignUp);
