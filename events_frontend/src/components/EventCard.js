import React, { Component } from "react";
import PropTypes from "prop-types";
import Card from "@material-ui/core/Card/Card";
import CardActionArea from "@material-ui/core/CardActionArea/CardActionArea";
import CardMedia from "@material-ui/core/CardMedia/CardMedia";
import { withStyles } from "@material-ui/core";
import CardContent from "@material-ui/core/CardContent/CardContent";
import Typography from "@material-ui/core/Typography/Typography";

class EventCard extends Component {
  render() {
    const { classes } = this.props;
    return (
      <Card className={classes.root} onClick={this.props.onClick} raised>
        <CardActionArea className={classes.actionArea}>
          <CardMedia className={classes.image} image={this.props.imageUrl} />
          <CardContent>
            <Typography variant="h5" className={classes.title}>
              {this.props.name}
            </Typography>
            <Typography variant={"body1"} className={classes.location}>
              {this.props.location.building}
            </Typography>
            <div className={classes.horizLayout}>
              <div className={classes.vertLayout}>
                <Typography variant={"body1"} className={classes.bold}>
                  {this.props.startMonth}
                </Typography>
                <Typography variant={"body1"} className={classes.num}>
                  {this.props.startDay}
                </Typography>
              </div>
              <div className={classes.vertLayout}>
                <Typography variant={"body1"} className={classes.bold}>
                  Starts
                </Typography>
                <Typography variant={"body1"} className={classes.num}>
                  {this.props.startTime}
                </Typography>
              </div>
              <div className={classes.vertLayout}>
                <Typography variant={"body1"} className={classes.bold}>
                  Going
                </Typography>
                <Typography variant={"body1"} className={classes.num}>
                  {this.props.numAttendees}
                </Typography>
              </div>
            </div>
          </CardContent>
        </CardActionArea>
      </Card>
    );
  }
}

EventCard.propTypes = {
  name: PropTypes.string.isRequired,
  startTime: PropTypes.string.isRequired,
  location: PropTypes.object.isRequired,
  numAttendees: PropTypes.number.isRequired,
  onClick: PropTypes.func.isRequired
};

const styles = theme => ({
  root: {
    flex: 1
  },
  image: {
    width: "100%",
    paddingTop: "50%", //2:1 ratio
    backgroundColor: theme.palette.primary.main
  },
  actionArea: {
    width: "100%"
  },
  horizLayout: {
    display: "flex",
    flexDirection: "row",
    alignItems: "stretch",
    justifyContent: "space-around",
    marginTop: theme.spacing(2)
  },
  vertLayout: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  title: {
    fontWeight: 600,
    fontSize: 25
  },
  location: {
    fontWeight: 400,
    fontSize: 20
  },
  bold: {
    fontWeight: 600,
    fontSize: 20
  },
  num: {
    fontWeight: 400,
    fontSize: 25
  }
});

export default withStyles(styles)(EventCard);
