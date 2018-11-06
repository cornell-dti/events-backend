import React, {Component} from 'react';
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";

/**
 * Displays Django errors from form submission.
 */
class FormError extends Component {
	state = {error: ""};

	constructor(props) {
		super(props);
		//see templates/main.html
		document.addEventListener("animationstart", this.showDjangoError.bind(this), false);
	}

	/**
	 * When a new node is created (the error text), an animation is triggered in
	 * main.html named "nodeInserted". We then display the error.
	 */
	showDjangoError() {
		if (event.animationName !== 'nodeInserted')
			return;
		const errorList = document.getElementsByClassName("errorlist")[0];
		if (errorList === undefined)
			return;
		const error = errorList.getElementsByTagName("li")[0];
		if (error === undefined)
			return;
		this.setState({error: error.textContent});
	}

	render() {
		const {classes} = this.props;
		return (
			<Typography className={classes.error} variant={"title"} color={"secondary"}>
				{this.state.error}
			</Typography>
		);
	}
}

const styles = (theme) => ({
	error: {
		marginTop: theme.spacing.unit * 2
	}
});

export default withStyles(styles)(FormError);