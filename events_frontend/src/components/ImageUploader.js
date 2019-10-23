import React, { Component } from "react";
import PropTypes from "prop-types";
import Button from "@material-ui/core/Button/Button";
import { withStyles } from "@material-ui/core";
import AvatarEditor from "react-avatar-editor";
// import classNames from "classnames";

class ImageUploader extends Component {
  state = { image_file: null, scaled_image: null };

  onFileChange(e) {
    const image = e.target.files[0];
    this.props.onImageChange(image);
    this.setState({ image_file: image });

    if (this.editor) {
      const canvasScaled = this.editor.getImageScaledToCanvas();
      this.setState({ scaled_image: canvasScaled });
    }
  }

  onUploadClick() {
    document.getElementById("fileInput").click();
  }

  classForShape(shape, classes) {
    switch (shape) {
      case "circle":
        return classes.circle;
      case "rectangle":
        return classes.rectangle;
      default:
        console.log("ImageUploader.classForShape() incorrect shape: " + shape);
        return null;
    }
  }

  setEditorRef = editor => {
    this.editor = editor;
  };

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
          <AvatarEditor
            ref={this.setEditorRef}
            image={this.state.image_file || this.props.image_url}
            width={500}
            height={300}
            border={0}
          />
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
  imagePreview: {
    marginTop: theme.spacing(2),
    backgroundSize: "cover"
  },
  circle: {
    width: theme.spacing(50),
    height: theme.spacing(50),
    borderRadius: theme.spacing(25)
  },
  rectangle: {
    width: "100%",
    paddingTop: "50%" //2:1 ratio
  }
});

export default withStyles(styles)(ImageUploader);
