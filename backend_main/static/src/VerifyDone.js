import React, {Component} from 'react';
import {withStyles} from "@material-ui/core";
import Onboarding from "./components/Onboarding";
import Typography from "@material-ui/core/Typography/Typography";

class VerifyDone extends Component
{
	render()
	{
		const {classes} = this.props;
		return (
			<Onboarding title={"ALL SET FOR NOW!"}
			            body={"An email will be sent to your organization within the next 36 hours when your organization is verified. Follow instructions in the email to complete your organization’s profile. Enjoy!"}>
				<Typography variant={"body1"}>
					Questions? Email contact@cornelldti.org
				</Typography>
			</Onboarding>
		)
	}
}

const styles = (theme) => ({});

export default withStyles(styles)(VerifyDone);