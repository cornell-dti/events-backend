import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField/TextField";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button";
import FormError from "./components/FormError";
import axios from "axios";
import Cookies from "js-cookie";

axios.defaults.headers.post["X-CSRFToken"] = Cookies.get("csrftoken");

class ChangePassword extends Component {
  state = {
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
    passwordUpdated: false,
    errors: []
  };

  confirmPasswordError() {
    return this.state.newPassword !== this.state.confirmPassword;
  }
  canContinue() {
    return (
      this.state.oldPassword !== undefined &&
      this.state.oldPassword !== "" &&
      this.state.newPassword !== undefined &&
      this.state.newPassword !== "" &&
      this.state.confirmPassword !== undefined &&
      this.state.confirmPassword !== "" &&
      !this.confirmPasswordError()
    );
  }
  onClick() {
    this.setState({ passwordUpdated: false });
    const passwords = {
      old_password: this.state.oldPassword,
      new_password: this.state.newPassword
    };
    axios
      .post("/api/change_password/", passwords)
      .then(response => {
        this.setState({
          oldPassword: "",
          newPassword: "",
          confirmPassword: "",
          passwordUpdated: true,
          errors: []
        });
      })
      .catch(error => this.setState({ errors: error.response.data.messages }));
  }
  onEnter(e) {
    if (e.key === "Enter") {
      document.getElementById("op-button").click();
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
        <FormError errors={this.state.errors} />
        <Typography className={classes.title} variant={"h5"} color={"inherit"}>
          Change Your Password
        </Typography>
        <TextField
          label="Old Password"
          className={classes.textField}
          value={this.state.oldPassword}
          onChange={e => this.setState({ oldPassword: e.target.value })}
          margin={"normal"}
          type={"password"}
        />
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
          helperText={
            this.confirmPasswordError() ? "Passwords do not match" : ""
          }
          onKeyPress={this.onEnter.bind(this)}
        />
        {this.state.passwordUpdated ? (
          <Typography
            className={classes.verify}
            variant={"h6"}
            color={"primary"}
            align={"center"}
          >
            Password updated successfully!
          </Typography>
        ) : null}
        <Button
          disabled={!this.canContinue()}
          color={"primary"}
          variant={"contained"}
          className={classes.spaced}
          onClick={this.onClick.bind(this)}
          id={"op-button"}
        >
          Update Password
        </Button>
      </div>
    );
  }
}

const styles = theme => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  title: {
    marginTop: theme.spacing(5),
    fontWeight: 500
  },
  textField: {
    marginLeft: theme.spacing(25),
    marginRight: theme.spacing(25),
    width: "100%"
  },
  spaced: {
    marginTop: theme.spacing(3)
  },
  verify: {}
});

export default withStyles(styles)(ChangePassword);
