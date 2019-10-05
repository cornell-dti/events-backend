import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography/Typography";
import Logo from "./components/Logo";
import ReactGA from "react-ga";
// import ScaleIn from 'material-ui/internal/ScaleIn';

class Landing extends Component {
  constructor(props) {
    super(props);
    ReactGA.pageview(window.location.pathname + window.location.search);
  }
  //TODO update download links
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <div className={classes.textContainer}>
          <Logo fontSize={150} />
          <Typography className={classes.tagline}>
            Discover all the events at Cornell
          </Typography>
          {/* <div className={classes.buttonContainer}>
            <a href={"/"} className={classes.button}>
              <img
                // src={
                //   "https://upload.wikimedia.org/wikipedia/commons/5/55/Download_on_iTunes.svg"
                // }
                src={"/static/apple-store.svg"}
                alt="Download on the App Store"
              />
            </a>
            <a href={"/"} className={classes.button}>
              <img
                // src={
                //   "https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg"
                // }
                src={"/static/google-play-badge.png"}
                alt="Download on the Google Play Store"
              />
            </a>
          </div> */}
        </div>
        <img src={"/static/device.png"} className={classes.image} alt="Phone" />
      </div>
    );
  }
}

const styles = theme => ({
  root: {
    flex: 1,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "stretch",
    marginRight: theme.spacing(24),
    marginLeft: theme.spacing(16)
  },
  textContainer: {
    flexGrow: 1,
    flexDirection: "column",
    marginRight: theme.spacing(8)
  },
  buttonContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    marginTop: theme.spacing(2)
  },
  button: {
    width: "13vw",
    height: "auto",
    marginRight: theme.spacing(2)
  },
  image: {
    marginleft: theme.spacing(16),
    marginTop: theme.spacing(6),
    height: "70vh"
  },
  tagline: {
    fontSize: 40
  }
});

export default withStyles(styles)(Landing);
