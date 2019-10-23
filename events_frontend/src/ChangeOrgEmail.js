import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField/TextField";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button";
import FormError from "./components/FormError";
import axios from "axios";
import Cookies from "js-cookie";

axios.defaults.headers.post["X-CSRFToken"] = Cookies.get("csrftoken");

class ChangeOrgEmail extends Component {
  state = { newOrgEmail: "", emailUpdated: false, errors: [] };

  canContinue() {
    return (
      this.state.newOrgEmail !== undefined && this.state.newOrgEmail !== ""
    );
  }

  onClick() {
    this.setState({ emailUpdated: false });
    const email = {
      new_email: this.state.newOrgEmail
    };
    axios
      .post("/api/change_org_email/", email)
      .then(response => {
        this.setState({
          errors: [],
          newOrgEmail: "",
          emailUpdated: true
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
        <Typography className={classes.title} variant={"h5"} color={"inherit"}>
          Change Your Organization Email
        </Typography>
        <Typography className={classes.disclaimer} color={"primary"}>
          Warning: Doing so will change your login email as well!
        </Typography>
        <TextField
          label="New Organization Email"
          className={classes.textField}
          value={this.state.newOrgEmail}
          onChange={e => this.setState({ newOrgEmail: e.target.value })}
          margin={"normal"}
          type={"username"}
          onKeyPress={this.onEnter.bind(this)}
        />
        {this.state.emailUpdated ? (
          <Typography
            className={classes.verify}
            variant={"h6"}
            color={"primary"}
            align={"center"}
          >
            Organization email updated successfully!
          </Typography>
        ) : null}
        <FormError errors={this.state.errors} />
        <Button
          disabled={!this.canContinue()}
          color={"primary"}
          variant={"contained"}
          className={classes.spaced}
          onClick={this.onClick.bind(this)}
          id={"op-button"}
        >
          Update Organization Email
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
  disclaimer: {
    marginTop: theme.spacing(1),
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

export default withStyles(styles)(ChangeOrgEmail);
