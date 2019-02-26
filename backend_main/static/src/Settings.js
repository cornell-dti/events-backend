import React, { Component } from 'react';
import { withStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField/TextField";
import Typography from "@material-ui/core/Typography/Typography";
import Button from '@material-ui/core/Button';
import routes from './routes';
import LinkColorless from "./components/LinkColorless";
import FormError from "./components/FormError";

class Settings extends Component {
  state = { oldPassword: "", newPassword: "", confirmPassword: "" };

  confirmPasswordError() {
    return this.state.newPassword !== this.state.confirmPassword;
  }
  canContinue() {
    return this.state.oldPassword !== undefined && this.state.oldPassword !== "" &&
      this.state.newPassword !== undefined && this.state.newPassword !== "" &&
      this.state.confirmPassword !== undefined && this.state.confirmPassword !== "" &&
      !this.confirmPasswordError();
  }
  onClick() {
    document.getElementById("id_old_password").value = this.state.oldPassword;
    document.getElementById("id_new_password1").value = this.state.newPassword;
    document.getElementById("id_new_password2").value = this.state.confirmPassword;
    const form = document.getElementsByTagName("form")[0];
    form.submit();
  }
  onEnter(e) {
    if (e.key === 'Enter') {
      document.getElementsByTagName("button")[0].click();
    }
  }
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        {/* <Typography variant={"h4"} className={classes.title}>
          Account Settings
        </Typography> 
        <TextField
          label="Email Address"
          className={classes.textField}
          value={this.state.email}
          onChange={e => this.setState({ email: e.target.value })}
          margin={"normal"} />
        <Typography variant={"body1"} color={"inherit"}>
          Update your email address on your
          <LinkColorless to={routes.profile.route}> profile page </LinkColorless>
        </Typography> */}
        < FormError />
        <Typography className={classes.title} variant={"h5"} color={"inherit"}>
          Change Your Password
				</Typography>
        <TextField
          label="Old Password"
          className={classes.textField}
          value={this.state.oldPassword}
          onChange={e => this.setState({ oldPassword: e.target.value })}
          margin={"normal"}
          type={"password"} />
        <TextField
          label="New Password"
          className={classes.textField}
          value={this.state.newPassword}
          onChange={e => this.setState({ newPassword: e.target.value })}
          margin={"normal"}
          type={"password"}
        />
        <TextField
          label="Confirm Password"
          className={classes.textField}
          value={this.state.confirmPassword}
          onChange={e => this.setState({ confirmPassword: e.target.value })}
          margin={"normal"}
          type={"password"}
          error={this.confirmPasswordError()}
          helperText={this.confirmPasswordError() ? "Passwords do not match" : ""}
          onKeyPress={this.onEnter.bind(this)}
        />
        <LinkColorless to={routes.auth.myEvents.route} disabled={!this.canContinue()} >
          <Button disabled={!this.canContinue()} color={"primary"} variant={"contained"} className={classes.spaced} onClick={this.onClick.bind(this)}>
            Update Password
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
    alignItems: 'center'
  },
  title: {
    marginTop: theme.spacing.unit * 5,
    fontWeight: 500
  },
  textField: {
    marginLeft: theme.spacing.unit * 25,
    marginRight: theme.spacing.unit * 25,
    width: '100%'
  },
  spaced: {
    marginTop: theme.spacing.unit * 5
  }
});

export default withStyles(styles)(Settings)