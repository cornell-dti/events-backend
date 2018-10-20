import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {withStyles} from "@material-ui/core";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";
import LinkColorless from "./LinkColorless";

class Onboarding extends Component
{
	render()
	{
		const {classes} = this.props;
		return (
			<div className={classes.root}>
				<Typography variant={"headline"} className={classes.title}>
					{this.props.title}
				</Typography>
				{this.props.body !== undefined
					? <Typography variant={"title"} className={classes.spaced} align={"center"}>
						{this.props.body}
					</Typography>
					: null}
				{this.props.children}
				{this.props.button !== undefined
					?
						<Button disabled={!this.props.canClick} color={"primary"} variant={"contained"} className={classes.spaced} onClick={this.props.onClick} >
							{this.props.button}
						</Button>
					: null}
			</div>
		);
	}

}

Onboarding.propTypes = {
	title: PropTypes.string.isRequired,
	body: PropTypes.string,
	button: PropTypes.string,
	link: PropTypes.string,
	canClick: PropTypes.bool,
	onClick: PropTypes.func
};

const styles = (theme) => ({
	root: {
		height: '80vh',
		width: '45vw',
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
		justifyContent: 'space-evenly',
		margin: theme.spacing.unit * 2
	},
	title: {
		fontWeight: 700,
		extend: 'spaced'
	},
	spaced: {
		margin: theme.spacing.unit * 2
	}
});
export default withStyles(styles)(Onboarding);