import React, {Component} from 'react';
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";

class FormError extends Component {
	state = { errors: [] };
	render() {
		const {classes} = this.props;
		const errorString = this.state.errors.join(" ");
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