import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {withStyles} from "@material-ui/core";
import Onboarding from "./components/Onboarding";
import TextField from "@material-ui/core/TextField/TextField";
import routes from './routes';
import {SET_NAME, SET_NET_ID} from "./redux/user";
import connect from "react-redux/es/connect/connect";
import Form from "./components/Form";

class VerifyCornellStatus extends Component
{
	submitCreateOrg = null;

	constructor(props) {
		super(props);
		this.setState({name: "", netid: ""});
	}
	canContinue()
	{
		return this.state.name !== undefined && this.state.name !== ""
			&& this.state.netid !== undefined && this.state.netid !== "";
	}
	onClick()
	{
		this.props.setName(this.state.name);
		this.props.setNetId(this.state.netid);

		const csrfMiddlewareToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
		fetch("https://cuevents-app.herokuapp.com/app/api-auth/login/", {
			method: "POST",
			credentials: "include",
			body: JSON.stringify({
				csrfmiddlewaretoken: csrfMiddlewareToken,
				id_username: this.props.orgEmail,
				id_password: this.props.password
			})
		}).then(res => console.log(JSON.stringify(res)))
			.catch(err => console.log("ERROR: " + JSON.stringify(err)));
		// document.getElementById("id_username").value = this.props.orgEmail;
		// document.getElementById("id_password").value = this.props.password;
		// this.submitCreateOrg();
	}

	render()
	{
		const {classes} = this.props;
		return (
			<Onboarding title={"VERIFY YOUR CORNELL STATUS"}
			            body={"To keep events and the community Cornell-specific, you must be a Cornell student to create an organization account."}
			            button={"I am a Cornell student"}
			            link={routes.verifyOrg.route}
			            canClick={this.canContinue()}
						onClick={this.onClick.bind(this)}>
				<TextField
					required
					id="name"
					label="Name"
					className={classes.textField}
					value={this.state.name}
					onChange={e => this.setState({name: e.target.value})}
					margin={"normal"} />
				<TextField
					required
					id="netid"
					label="Cornell NetID"
					className={classes.textField}
					value={this.state.netid}
					onChange={e => this.setState({netid: e.target.value})}
					margin={"normal"} />
				<div>{this.props.orgEmail}</div>
				<Form url={"https://cuevents-app.herokuapp.com/app/api-auth/login/"}
				      submit={(submit => this.submitCreateOrg = submit)}/>
			</Onboarding>
		)
	}
}

const styles = (theme) => ({
	textField: {
		width: '100%',
		margin: theme.spacing.unit * 3
	}
});

VerifyCornellStatus.propTypes = {
	setName: PropTypes.func.isRequired,
	setNetId: PropTypes.func.isRequired,
	orgEmail: PropTypes.string.isRequired,
	password: PropTypes.string.isRequired
};

function mapStateToProps(state)
{
	return {
		orgEmail: state.user.orgEmail,
		password: state.user.password
	};
}
function mapDispatchToProps(dispatch)
{
	return {
		setName: (name) => dispatch({type: SET_NAME, value: name}),
		setNetId: (netid) => dispatch({type: SET_NET_ID, value: netid})
	}
}

VerifyCornellStatus = connect(mapStateToProps, mapDispatchToProps)(VerifyCornellStatus);
export default withStyles(styles)(VerifyCornellStatus);