import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography/Typography";
import Logo from "./components/Logo";
// import ScaleIn from 'material-ui/internal/ScaleIn';

class Landing extends Component {
	//TODO update download links
	render() {
		const { classes } = this.props;
		return (

			<div className={classes.root}>
				<div className={classes.textContainer}>
					<Logo fontSize={150} />
					<Typography className={classes.tagline}>
						Discover all the events at Cornell
						</Typography>
					<div className={classes.buttonContainer}>
						<a href={"/"} className={classes.button}>
							<img src={"https://upload.wikimedia.org/wikipedia/commons/3/3c/Download_on_the_App_Store_Badge.svg"} alt="Download on the App Store" />
						</a>
						<a href={"/"} className={classes.button}>
							<img src={"https://upload.wikimedia.org/wikipedia/commons/c/cd/Get_it_on_Google_play.svg"} alt="Download on the Google Play Store" />
						</a>
					</div>
				</div>
				<img src={"/static/device.png"} className={classes.image} alt="Phone" />
			</div >

		);
	}
}

const styles = (theme) => ({
	root: {
		flex: 1,
		display: 'flex',
		flexDirection: 'row',
		alignItems: 'center',
		alignSelf: 'stretch',
		marginRight: theme.spacing.unit * 24,
		marginLeft: theme.spacing.unit * 16,
	},
	textContainer: {
		flexGrow: 1,
		flexDirection: 'column',
		marginRight: theme.spacing.unit * 8
	},
	buttonContainer: {
		flexDirection: 'row',
		marginTop: theme.spacing.unit * 2
	},
	button: {
		marginRight: theme.spacing.unit * 2
	},
	image: {
		marginleft: theme.spacing.unit * 16,
		marginTop: theme.spacing.unit * 8,
		height: '75vh'
	},
	tagline: {
		fontSize: 40
	}

});

export default withStyles(styles)(Landing);