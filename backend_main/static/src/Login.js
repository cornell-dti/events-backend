import React, {Component, Fragment} from 'react';
import {withStyles} from "@material-ui/core";

class Login extends Component {
	render() {
		return (
			<Fragment>
			hi
			</Fragment>);
	}
}

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

export default withStyles(styles)(Login);