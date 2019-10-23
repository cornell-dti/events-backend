import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography/Typography";
import Logo from "./components/Logo";
// import ScaleIn from 'material-ui/internal/ScaleIn';

class Landing extends Component {
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
