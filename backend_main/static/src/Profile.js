import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import ImageUploader from "./components/ImageUploader";
import TextField from "@material-ui/core/TextField/TextField";
import Button from "@material-ui/core/Button/Button";
import TagField from "./components/TagField";

class Profile extends Component {
	state = {
		name: "Cornell DTI", website: "https://cornelldti.org",
		email: "hello@cornelldti.org", bio: "", tags: []
	};

	onImageChange(image) {

	}
	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<ImageUploader onImageChange={this.onImageChange} shape={"circle"} />
				<TextField
					id="name"
					label="Organization name"
					className={classes.textField}
					value={this.state.name}
					onChange={e => this.setState({ name: e.target.value })}
					margin={"normal"} />
				<TextField
					id="email"
					label="Organization email"
					className={classes.textField}
					value={this.state.email}
					onChange={e => this.setState({ email: e.target.value })}
					margin={"normal"} />
				<TextField
					id="website"
					label="Organization website"
					className={classes.textField}
					value={this.state.website}
					onChange={e => this.setState({ website: e.target.value })}
					margin={"normal"} />
				<TextField
					id="bio"
					label="Bio"
					placeholder={"What is your organization about?"}
					className={classes.textField}
					value={this.state.bio}
					onChange={e => this.setState({ bio: e.target.value })}
					margin={"normal"}
					multiline={true} />
				<TagField onNewTags={(tags) => this.setState({ tags: tags })} />
				<Button color={"primary"} variant={"contained"} className={classes.button}>
					Save
				</Button>
			</div>
		);
	}
}

const styles = (theme) => ({
	root: {
		display: 'flex',
		flexDirection: 'column',
		alignSelf: 'stretch',
		padding: theme.spacing.unit * 4
	},
	button: {
		marginTop: theme.spacing.unit * 2
	}
});
export default withStyles(styles)(Profile);
