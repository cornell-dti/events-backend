import React, { Component } from "react";
import PropTypes from "prop-types";
import Button from "@material-ui/core/Button/Button";
import { withStyles } from "@material-ui/core";

class ImageUploader extends Component {
  state = { image_file: null, image_preview: null};

  onFileChange(e) {
    e.preventDefault();
    const reader = new FileReader();
    const file = e.target.files[0];

    reader.onloadend = () => {
      this.setState({
        image_file: file,
        image_preview: reader.result
      });
    }

    reader.readAsDataURL(file)
    this.props.onImageChange(file);
  }

  onUploadClick() {
    document.getElementById("fileInput").click();
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <div className={classes.hidden}>
          <input
            id={"fileInput"}
            type={"file"}
            onChange={this.onFileChange.bind(this)}
            accept={"image/*"}
          />
        </div>
        <Button className={classes.button} onClick={this.onUploadClick}>
          {this.state.image_file || this.props.image_url
            ? "Change image"
            : "Upload image"}
        </Button>
        {this.state.image_file || this.props.image_url ? (
          <div className={classes.container}>
            <img className={classes.avatar} src={this.state.image_preview || this.props.image_url}/>
          </div>
        ) : null}
      </div>
    );
  }
}

ImageUploader.propTypes = {
  onImageChange: PropTypes.func.isRequired,
  shape: PropTypes.string.isRequired
};

const styles = theme => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  hidden: {
    height: 0,
    overflow: "hidden"
  },
  button: {
    width: "100%"
  },
  container: {
    width: "500px",
    height: "300px"
  },
  avatar: {    
    width: "100%",
    height: "100%",
    overflow: "hidden",
    "object-fit": "cover"
  }
});

export default withStyles(styles)(ImageUploader);
