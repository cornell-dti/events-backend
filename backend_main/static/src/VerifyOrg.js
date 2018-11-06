import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import Onboarding from "./components/Onboarding";
import TextField from "@material-ui/core/TextField/TextField";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";
import routes from './routes';
import Radio from "@material-ui/core/Radio/Radio";
import PropTypes from "prop-types";
import connect from "react-redux/es/connect/connect";


const FACEBOOK = "facebookLink";
const WEBSITE = "website";
const CONTACT = "contact";
const FIELD = { FACEBOOK, WEBSITE, CONTACT };
const CUE_EMAIL = "cue@cornelldti.org";
class VerifyOrg extends Component {
	state = { facebookLink: "", website: "", selectedField: "" };

	canContinue() {
		return (this.state.facebookLink !== undefined && this.state.facebookLink !== "")
			|| (this.state.website !== undefined && this.state.website !== "");
	}
	onClick() {
		let link;
		switch (this.state.selectedField) {
			case FIELD.FACEBOOK:
				link = this.state.facebookLink;
				break;
			case FIELD.WEBSITE:
				link = this.state.website;
				break;
			default:
				return;
		}

        fetch("./email/orgEmail=" + this.props.orgEmail + "&orgName=" + this.props.orgName + "&name=" + this.props.name +
            "&netID=" + this.props.netid + "&link=" + link)
            .then(response => console.log("E-mail sent!"));
	}
	onEmailClick() {
		const newline = escape("\n");
		const link = `mailto:${CUE_EMAIL}?subject=Organization Verification: ${this.props.orgName}&body=Organization email: ${this.props.orgEmail}${newline}
		Name: ${this.props.name}${newline}
		NetID: ${this.props.netid}`;
		window.open(link, "_blank");
	}
	render() {
		const { classes } = this.props;
		return (
			<Onboarding title={"Verify your Organization"}
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
						<Button variant={"contained"} color={"secondary"} onClick={this.onEmailClick.bind(this)}>
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
	orgName: PropTypes.string.isRequired,
	orgEmail: PropTypes.string.isRequired,
	name: PropTypes.string.isRequired,
	netid: PropTypes.string.isRequired
};

function mapStateToProps(state) {
	return {
		orgName: state.user.orgName,
		orgEmail: state.user.orgEmail,
		name: state.user.name,
		netid: state.user.netid
	};
}
function mapDispatchToProps(dispatch) {
	return {}
}

VerifyOrg = connect(mapStateToProps, mapDispatchToProps)(VerifyOrg);
export default withStyles(styles)(VerifyOrg);