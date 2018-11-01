import React, {Component} from 'react';
import {withStyles} from "@material-ui/core";
import TextField from "@material-ui/core/TextField/TextField";
import FormError from "./components/FormError";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";

class Login extends Component {
	state = {email: "", password: ""};

	canClick() {
		return this.state.email !== undefined && this.state.email !== "" &&
			this.state.password !== undefined && this.state.password !== "";
	}
	onClick() {
		document.getElementById("id_username").value = this.state.email;
		document.getElementById("id_password").value = this.state.password;
		const form = document.getElementsByTagName("form")[0];
		form.submit();
	}
	render() {
		const {classes} = this.props;
		return (
			<div className={classes.root}>
				<Typography variant={"headline"} className={classes.title}>
					Organization Login
				</Typography>
				<FormError />
				<TextField
					label="Email"
					className={classes.textField}
					value={this.state.email}
					onChange={e => this.setState({ email: e.target.value })}
					margin={"normal"} />
				<TextField
					label="Password"
					className={classes.textField}
					value={this.state.password}
					onChange={e => this.setState({ password: e.target.value })}
					type={"password"}
					margin={"normal"} />
				<Button disabled={!this.canClick()} color={"primary"}
				        className={classes.button} variant={"contained"}
				        onClick={this.onClick.bind(this)} >
					Login
				</Button>
			</div>);
	}
}

const styles = (theme) => ({
	root: {
		width: '45vw',
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
		margin: theme.spacing.unit * 4
	},
	title: {
		fontWeight: 700,
		extend: 'spaced'
	},
	textField: {
		width: '100%',
		margin: theme.spacing.unit * 3
	},
	button: {
		margin: theme.spacing.unit * 2
	}
});

export default withStyles(styles)(Login);