import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";

class Logo extends Component
{
	render()
	{
		const {classes} = this.props;
		return (
			<Typography className={classes.title} style={{fontSize: this.props.fontSize}}>
				cue
			</Typography>
		);
	}
}

Logo.propTypes = {
	fontSize: PropTypes.number.isRequired
};

const styles = (theme) => ({
	title: {
		fontWeight: 700,
		lineHeight: 1,
		color: theme.palette.primary.main
	}
});

export default withStyles(styles)(Logo);