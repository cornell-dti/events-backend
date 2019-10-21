import React, { Component } from "react";
import PropTypes from "prop-types";
import AppBar from "@material-ui/core/AppBar/AppBar";
import Toolbar from "@material-ui/core/Toolbar/Toolbar";
import Typography from "@material-ui/core/Typography/Typography";
import Button from "@material-ui/core/Button/Button";
import { withStyles } from "@material-ui/core";
import { Route, Switch, Redirect, withRouter } from "react-router-dom";
import routes from "./routes";
import LinkColorless from "./components/LinkColorless";
import Logo from "./components/Logo";
import Landing from "./Landing";
import axios from "axios";

class Main extends Component {
  state = { loggedIn: true };

  componentDidMount() {
    let self = this;
    axios
      .get("/api/loggedin/")
      .then(response => self.setState({ loggedIn: response.data.status }));
  }

  getNavBar(classes) {
    if (!this.state.loggedIn)
      return (
        <React.Fragment>
          <Typography variant={"title"} color={"inherit"}>
            Are you an organization?
          </Typography>
          <LinkColorless to={routes.noAuth.login.route}>
            <Button color={"primary"} className={classes.button}>
              Log in
            </Button>
          </LinkColorless>
          <LinkColorless to={routes.noAuth.signup.route}>
            <Button
              variant={"outlined"}
              color={"primary"}
              className={classes.button}
            >
              Sign up
            </Button>
          </LinkColorless>
        </React.Fragment>
      );
    else
      return (
        <React.Fragment>
          <LinkColorless to={routes.auth.profile.route}>
            <Button color={"primary"} className={classes.button}>
              Profile
            </Button>
          </LinkColorless>
          <LinkColorless to={routes.auth.myEventsDefault.route}>
            <Button color={"primary"} className={classes.button}>
              My Events
            </Button>
          </LinkColorless>
          <LinkColorless to={routes.auth.logout.route} logout={true}>
            <Button color={"primary"} className={classes.button}>
              Log Out
            </Button>
          </LinkColorless>
        </React.Fragment>
      );
  }

  getFooter(classes) {
    return (
      <React.Fragment>
        <a href={"https://www.cornelldti.org/"}>
          <img
            src={"/static/dti_logo.png"}
            className={classes.logo}
            alt="Logo"
          />
        </a>

        <a
          target="_blank"
          style={{ textDecoration: "none" }}
          href={"https://forms.gle/UUCa8mzi6b9fnfxq9"}
        >
          <Typography variant="h6" color="primary">
            {" "}
            Contact Us{" "}
          </Typography>
        </a>
        <div className={classes.buttonContainer}>
          <a href={"/"} className={classes.appButton}>
            <img
              src={
                "../../assets/download-on-itunes.svg"
              }
              alt="Download on the App Store"
            />
          </a>
          <a href={"/"} className={classes.appButton}>
            <img
              src={
                "../../assets/google-play-store-badge.svg"
              }
              alt="Download on the Google Play Store"
            />
          </a>
        </div>
      </React.Fragment>
    );
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <AppBar color={"default"}>
          <Toolbar>
            <LinkColorless to={"/"} style={{ flexGrow: 1 }}>
              <Logo fontSize={40} />
            </LinkColorless>
            {this.getNavBar(classes)}
          </Toolbar>
        </AppBar>
        <div className={classes.appBarSpace} />
        {this.state.loggedIn ? (
          <Switch>
            {Object.values(Object.assign(routes.auth, routes.noAuth)).map(
              obj => (
                <Route
                  exact
                  key={obj.route}
                  path={obj.route}
                  component={obj.component}
                />
              )
            )}
            <Redirect to={"/"} />
          </Switch>
        ) : (
          <Switch>
            {Object.values(routes.noAuth).map(obj => (
              <Route
                exact
                key={obj.route}
                path={obj.route}
                component={obj.component}
              />
            ))}
            {Object.values(routes.auth).map(obj => (
              <Redirect key={obj.route} from={obj.route} to={"/login/"} />
            ))}
            <Redirect to={"/"} />
          </Switch>
        )}
        <AppBar color={"default"} className={classes.footer}>
          {this.getFooter(classes)}
        </AppBar>
      </div>
    );
  }
}

Main.propTypes = {
  location: PropTypes.shape({
    pathname: PropTypes.string
  }).isRequired
};

const styles = theme => ({
  footer: {
    bottom: 0,
    top: "auto",
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-evenly"
  },
  buttonContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    marginTop: theme.spacing.unit * 2,
    marginBottom: theme.spacing.unit * 2
  },
  appButton: {
    height: "40%",
    width: "10vw",
    marginRight: theme.spacing.unit * 2
  },
  logo: {
    width: "15vw"
  },
  root: {
    flexGrow: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  appBarSpace: theme.mixins.toolbar,
  button: {
    marginLeft: theme.spacing.unit * 2
  }
});

export default withStyles(styles)(withRouter(Main));
