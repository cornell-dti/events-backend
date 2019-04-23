import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import ImageUploader from "./components/ImageUploader";
import TextField from "@material-ui/core/TextField/TextField";
import Button from "@material-ui/core/Button/Button";
import Typography from "@material-ui/core/Typography/Typography";
import TagField from "./components/TagField";
import FormError from "./components/FormError";
import LinkColorless from "./components/LinkColorless";
import routes from './routes';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.post['X-CSRFToken'] = Cookies.get('csrftoken') //get CSRF-token for POST requests

class Profile extends Component {
	state = {
		name: "",
		website: "",
		email: "",
		bio: "",
		tags: [],
		errors: [],
		profileUpdated: false
	};

	componentDidMount(){
		const self = this
		axios.get('/api/profile/')
		.then(response => {
			this.setState({
				name: response.data.name,
				website: response.data.website,
				email: response.data.email,
				bio: response.data.bio,
				tags: response.data.tags
			})
		})
		.catch(error => {
			if (error.response.status == 404)
				this.setState({ errors: ['An error has occurred while retrieving your profile. Please try again later.']})
		})
	}


	saveProfile(){
		this.setState({ profileUpdated: false })
		let orgData = this.state;
		delete orgData.errors;
		axios.post('/api/profile/', orgData)
		.then(response => {
			this.setState({
				name: response.data.name,
				website: response.data.website,
				email: response.data.email,
				bio: response.data.bio,
				tags: response.data.tags,
				profileUpdated: true,
				errors: []
			})
		})
		.catch(error => {
			if (error.response.status == 404)
				this.setState({ errors: ['An error has occurred while updating your profile. Please try again later.']})
			else
				this.setState({ errors: error.response.data.messages })
		})
	}

	onImageChange(image) {

	}

	onEnter(e) {
		if (e.key === 'Enter'){
			this.saveProfile();
		}
	}

	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<ImageUploader image_url={""} onImageChange={this.onImageChange} shape={"circle"} />
				<TextField
					id="name"
					label="Organization name"
					//className={classes.textField}
					value={this.state.name}
					onChange={e => this.setState({ name: e.target.value })}
					onKeyPress={this.onEnter.bind(this)}
					margin={"normal"} />
				<TextField
					id="email"
					label="Organization email"
					//className={classes.textField}
					value={this.state.email}
					disabled={true}
					margin={"normal"} />
				<TextField
					id="website"
					label="Organization website"
					//className={classes.textField}
					value={this.state.website}
					onChange={e => this.setState({ website: e.target.value })}
					onKeyPress={this.onEnter.bind(this)}
					margin={"normal"} />
				<TextField
					id="bio"
					label="Bio"
					placeholder={"What is your organization about?"}
					//className={classes.textField}
					value={this.state.bio}
					onChange={e => this.setState({ bio: e.target.value })}
					onKeyPress={this.onEnter.bind(this)}
					margin={"normal"}
					multiline={true} />
				<TagField onNewTags={(tags) => this.setState({ tags: tags })} />
				<FormError errors = {this.state.errors} />
				{this.state.profileUpdated ?
					<Typography className={classes.verify} variant={"title"} color={"primary"} align={"center"}>
						Profile updated successfully!
					</Typography> : null 
				}
				<Button color={"primary"} variant={"contained"} className={classes.button} onClick={this.saveProfile.bind(this)}>
					Save
				</Button>
				<LinkColorless to={routes.auth.changeOrgEmail.route}>
					<Button color={"primary"} className={classes.button}>
						Change Organization Email
					</Button>
				</LinkColorless>
				<LinkColorless to={routes.auth.changePassword.route}>
					<Button color={"primary"} className={classes.button}>
						Change Password
					</Button>
				</LinkColorless>
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
	},
	verify: {}
});
export default withStyles(styles)(Profile);
