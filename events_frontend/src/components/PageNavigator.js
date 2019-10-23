import React from "react";
import { withStyles } from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import Typography from "@material-ui/core/Typography/Typography";
import LinkColorless from "./LinkColorless";

const PageNavigator = ({
  currPage,
  lastPage,
  prevPageLink,
  nextPageLink,
  classes
}) => {
  return (
    <div className={classes.container}>
      <LinkColorless to={prevPageLink} disabled={currPage === 1}>
        <IconButton
          className={classes.button}
          aria-label="Navigate to previous page"
        >
          <ChevronLeft />
        </IconButton>
      </LinkColorless>
      <Typography className={classes.pageIndicator} color={"primary"}>
        Page {currPage} of {lastPage > 0 ? lastPage : 1}
      </Typography>
      <LinkColorless to={nextPageLink} disabled={currPage >= lastPage}>
        <IconButton
          className={classes.button}
          aria-label="Navigate to next page"
        >
          <ChevronRight />
        </IconButton>
      </LinkColorless>
    </div>
  );
};

const styles = theme => ({
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginTop: "12px"
  },
  button: {},
  pageIndicator: {}
});

export default withStyles(styles)(PageNavigator);
