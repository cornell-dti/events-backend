import React, { Component } from "react";
import Typography from "@material-ui/core/Typography/Typography";
import { withStyles } from "@material-ui/core";

class FormError extends Component {
    state = { errors: [] };

    static getDerivedStateFromProps(nextProps, prevState) {
        if (nextProps.errors != prevState.errors) {
            return { errors: nextProps.errors };
        }
        else return null;
    }

    render() {
        const { classes } = this.props;
        const errorString = this.state.errors.join(" ");
        return (
            <Typography
                className={classes.error}
                variant={"subtitle1"}
                color={"secondary"}
                align={"center"}
            >
                {errorString}
            </Typography>
        );
    }
}

FormError.defaultProps = { errors: [] };

const styles = theme => ({
    error: {
        marginTop: theme.spacing(2)
    }
});

export default withStyles(styles)(FormError);
