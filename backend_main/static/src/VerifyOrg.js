import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import Onboarding from "./components/Onboarding";
import TextField from "@material-ui/core/TextField/TextField";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";
import routes from './routes';
import Radio from "@material-ui/core/Radio/Radio";
import PropTypes from "prop-types";
import { SET_FB, SET_WEBSITE } from "./redux/user";
import connect from "react-redux/es/connect/connect";

const FACEBOOK = "facebookLink";
const WEBSITE = "website";
const CONTACT = "contact";
const FIELD = { FACEBOOK, WEBSITE, CONTACT };
class VerifyOrg extends Component {
	state = { facebookLink: "", website: "", selectedField: "" };

	canContinue() {
		return (this.state.facebookLink !== undefined && this.state.facebookLink !== "")
			|| (this.state.website !== undefined && this.state.website !== "");
	}
	onClick() {
		switch (this.state.selectedField) {
			case FIELD.FACEBOOK:
				this.props.setFbLink(this.state.facebookLink);
				break;
			case FIELD.WEBSITE:
				this.props.setWebsite(this.state.website);
				break;
		}
		//TODO send all data to backend, or show error if anything is missing
	}
	render() {
		const { classes } = this.props;
		return (
			<Onboarding title={"VERIFY YOUR ORGANIZATION"}
				body={"To make sure the events posted by organizations are accurate, only Cornell organizations can create an organization account.\nSelect a verification method below:"}
				button={"Done"}
				link={routes.verifyDone.route}
				canClick={this.canContinue()}
				onClick={this.onClick.bind(this)}>
				<div className={classes.radioField}>
					<Radio
						checked={this.state.selectedField === FIELD.FACEBOOK} />
					<TextField
						id="facebook"
						label="Organization's Facebook Link"
						className={classes.textField}
						value={this.state.facebookLink}
						onChange={e => this.setState({ facebookLink: e.target.value })}
						onClick={() => this.setState({ selectedField: FIELD.FACEBOOK })}
						disabled={this.state.selectedField !== FIELD.FACEBOOK}
						margin={"normal"} />
				</div>

				<div className={classes.radioField}>
					<Radio
						checked={this.state.selectedField === FIELD.WEBSITE} />
					<TextField
						id="website"
						label="Organization's Website"
						className={classes.textField}
						value={this.state.website}
						onChange={e => this.setState({ website: e.target.value })}
						onClick={() => this.setState({ selectedField: FIELD.WEBSITE })}
						disabled={this.state.selectedField !== FIELD.WEBSITE}
						margin={"normal"} />
				</div>
				<div className={classes.radioField}
					onClick={() => this.setState({ selectedField: FIELD.CONTACT })}>
					<Radio
						checked={this.state.selectedField === FIELD.CONTACT} />
					<div className={classes.contactUsContainer}>
						<Typography variant={"title"} className={classes.contactUsText}>
							Contact Us
						</Typography>
						<Typography variant={"subheading"} className={classes.contactUsText}>
							Please send us an email with alternative ways to verify your club.
						</Typography>
						<Button variant={"contained"} color={"secondary"}>
							Email Us
						</Button>
					</div>
				</div>
			</Onboarding>
		)
	}
}

const styles = (theme) => ({
	radioField: {
		width: '100%',
		display: 'flex',
		flexDirection: 'row',
		alignItems: 'center'
	},
	contactUsContainer: {
		flex: 1,
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'flex-start'
	},
	contactUsText: {
		marginBottom: theme.spacing.unit
	},
	textField: {
		width: '100%',
		marginBottom: theme.spacing.unit * 4
	}
});

VerifyOrg.propTypes = {
	setFbLink: PropTypes.func.isRequired,
	setWebsite: PropTypes.func.isRequired
};

function mapStateToProps(state) {
	return {};
}
function mapDispatchToProps(dispatch) {
	return {
		setFbLink: (link) => dispatch({ type: SET_FB, value: link }),
		setWebsite: (website) => dispatch({ type: SET_WEBSITE, value: website })
	}
}

VerifyOrg = connect(mapStateToProps, mapDispatchToProps)(VerifyOrg);
export default withStyles(styles)(VerifyOrg);