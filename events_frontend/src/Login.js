import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import PropTypes from "prop-types";
import connect from "react-redux/es/connect/connect";
import { SET_ORG_EMAIL, SET_ORG_NAME } from "./redux/user";
import TextField from "@material-ui/core/TextField/TextField";
import FormError from "./components/FormError";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";
import axios from "axios";
import ReactGA from "react-ga"

class Login extends Component {
  constructor(props) {
    super(props);
    ReactGA.pageview(window.location.pathname + window.location.search);
  }

  state = {
    name: "",
    email: "",
    password: ""
  };

  canClick() {
    return (
      this.state.email !== undefined &&
      this.state.email !== "" &&
      this.state.password !== undefined &&
      this.state.password !== ""
    );
  }

  onClick() {
    this.props.setName(this.state.name);
    this.props.setEmail(this.state.email);

    const self = this;

    const loginData = {
      email: this.state.email,
      password: this.state.password
    };

    axios
      .post("/api/login/", loginData)
      .then(response => (window.location.href = "/events/"))
      .catch(error => self.setState({ errors: error.response.data.messages }));
  }

  onEnter(e) {
    if (e.key === "Enter") {
      this.onClick();
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <Typography variant={"h5"} className={classes.title}>
          Organization Login
        </Typography>
        <FormError errors={this.state.errors} />
        <TextField
          label="Email"
          className={classes.textField}
          value={this.state.email}
          onChange={e => this.setState({ email: e.target.value })}
          margin={"normal"}
        />
        <TextField
          label="Password"
          className={classes.textField}
          value={this.state.password}
          onChange={e => this.setState({ password: e.target.value })}
          type={"password"}
          margin={"normal"}
          onKeyDown={this.onEnter.bind(this)}
        />
        <Button
          disabled={!this.canClick()}
          color={"primary"}
          className={classes.button}
          variant={"contained"}
          onClick={this.onClick.bind(this)}
        >
          Login
        </Button>
      </div>
    );
  }
}

const styles = theme => ({
  root: {
    width: "45vw",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    margin: theme.spacing(4)
  },
  title: {
    fontWeight: 700,
    extend: "spaced"
  },
  textField: {
    width: "100%",
    margin: theme.spacing(3)
  },
  button: {
    margin: theme.spacing(2)
  }
});

Login.propTypes = {
  setName: PropTypes.func.isRequired,
  setEmail: PropTypes.func.isRequired
};

function mapStateToProps(state) {
  return {};
}
function mapDispatchToProps(dispatch) {
  return {
    setName: name => dispatch({ type: SET_ORG_NAME, value: name }),
    setEmail: email => dispatch({ type: SET_ORG_EMAIL, value: email })
  };
}

Login = connect(
  mapStateToProps,
  mapDispatchToProps
)(Login);

export default withStyles(styles)(Login);
