import React, {Component} from 'react';
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";

/**
 * Displays Django errors from form submission.
 */
class FormError extends Component {
	state = { errors: [] }
	componentWillReceiveProps(nextProps){
		this.setState({ errors: nextProps.errors })
	}
	render() {
		const {classes} = this.props;
		var errorString = ""
		for(var error of this.state.errors){
			errorString += error + " "
		}
		return (
			<Typography className={classes.error} variant={"title"} color={"secondary"}>
				{errorString}
			</Typography>
		);
	}
}

FormError.defaultProps = { errors: [] };

const styles = (theme) => ({
	error: {
		marginTop: theme.spacing.unit * 2
	}
});

export default withStyles(styles)(FormError);