import React, { Component } from "react";
import { withStyles } from "@material-ui/core";
import ImageUploader from "./components/ImageUploader";
import TextField from "@material-ui/core/TextField/TextField";
import Button from "@material-ui/core/Button/Button";
import Typography from "@material-ui/core/Typography/Typography";
import TagField from "./components/TagField";
import FormError from "./components/FormError";
import LinkColorless from "./components/LinkColorless";
import routes from "./routes";
import axios from "axios";
import Cookies from "js-cookie";
import ReactGA from 'react-ga'
axios.defaults.headers.post["X-CSRFToken"] = Cookies.get("csrftoken"); //get CSRF-token for POST requests

class Profile extends Component {
    state = {
        name: "",
        website: "",
        email: "",
        bio: "",
        tags: [],
        imageUrl: "",
        errors: [],
        profileUpdated: false,

        image: null,
        imageChanged: false
    };

    componentDidMount() {
        ReactGA.pageview(window.location.pathname + window.location.search);
        axios
            .get("/api/get_profile/")
            .then(response => {
                let org_tags = response.data.tags.map(tag => ({
                    value: tag.id,
                    label: tag.name
                }));
                this.setState({
                    name: response.data.name,
                    website: response.data.website,
                    email: response.data.email,
                    bio: response.data.bio,
                    tags: org_tags,
                    imageUrl:
                        response.data.photo.length > 0
                            ? response.data.photo.sort(
                                (a, b) =>
                                    Date.parse(b.uploaded_at) - Date.parse(a.uploaded_at)
                            )[0].link
                            : ""
                });
            })
            .catch(error => {
                if (error.response.status === 404)
                    this.setState({
                        errors: [
                            "An error has occurred while retrieving your profile. Please try again later."
                        ]
                    });
            });
    }

    uploadImage(callback) {
        const file = this.state.image;
        let xhr = new XMLHttpRequest();
        xhr.open(
            "GET",
            "/api/sign_s3/?file_name=" + file.name + "&file_type=" + file.type
        );
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    xhr = new XMLHttpRequest();
                    xhr.open("POST", response.data.url);

                    let postData = new FormData();
                    for (let key in response.data.fields) {
                        postData.append(key, response.data.fields[key]);
                    }
                    postData.append("file", file);

                    xhr.onreadystatechange = function () {
                        if (xhr.readyState === 4) {
                            if (xhr.status === 200 || xhr.status === 204) {
                                console.log("File uploaded!");
                                callback(
                                    response.url
                                        .split("/")
                                        .slice(3)
                                        .join("/")
                                );
                            } else {
                                alert("Could not upload file.");
                            }
                        }
                    };
                    xhr.send(postData);
                } else {
                    alert("Could not get signed URL.");
                }
            }
        };
        xhr.send();
    }

    async saveProfile() {
        this.setState({ profileUpdated: false });
        let { bio, email, name, tags, website } = this.state,
            orgData = {
                bio,
                email,
                name,
                tags,
                website
            },
            imageUrl = "";

        if (this.state.imageChanged) {
            let promise = new Promise((res, req) =>
                this.uploadImage(url => res(url))
            );
            imageUrl = await promise;
        }
        orgData.imageUrl = imageUrl;

        axios
            .post("/api/edit_profile/", orgData)
            .then(response => {
                this.setState({
                    name: response.data.name,
                    website: response.data.website,
                    email: response.data.email,
                    bio: response.data.bio,
                    tags: this.state.tags,
                    profileUpdated: true,
                    imageUrl: imageUrl,
                    errors: []
                });
            })
            .catch(error => {
                if (error.response.status === 404)
                    this.setState({
                        errors: [
                            "An error has occurred while updating your profile. Please try again later."
                        ]
                    });
                else this.setState({ errors: error.response.data.messages });
            });
    }

    onEnter(e) {
        if (e.key === "Enter") {
            this.saveProfile();
        }
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root}>
                <ImageUploader
                    image_url={this.state.imageUrl}
                    onImageChange={image =>
                        this.setState({ image: image, imageChanged: true })
                    }
                    shape={"rectangle"}
                />
                <TextField
                    id="name"
                    label="Organization name"
                    //className={classes.textField}
                    value={this.state.name}
                    onChange={e => this.setState({ name: e.target.value })}
                    onKeyPress={this.onEnter.bind(this)}
                    margin={"normal"}
                />
                <TextField
                    id="email"
                    label="Organization email"
                    //className={classes.textField}
                    value={this.state.email}
                    disabled={true}
                    margin={"normal"}
                />
                <TextField
                    id="website"
                    label="Organization website"
                    //className={classes.textField}
                    value={this.state.website}
                    onChange={e => this.setState({ website: e.target.value })}
                    onKeyPress={this.onEnter.bind(this)}
                    margin={"normal"}
                />
                <TextField
                    id="bio"
                    label="Bio"
                    placeholder={"What is your organization about?"}
                    //className={classes.textField}
                    value={this.state.bio}
                    onChange={e => this.setState({ bio: e.target.value })}
                    onKeyPress={this.onEnter.bind(this)}
                    margin={"normal"}
                    multiline={true}
                />
                <TagField
                    tags={this.state.tags}
                    onNewTags={tags => this.setState({ tags: tags })} />
                <FormError errors={this.state.errors} />
                {this.state.profileUpdated ? (
                    <Typography
                        className={classes.verify}
                        variant={"h6"}
                        color={"primary"}
                        align={"center"}
                    >
                        Profile updated successfully!
                    </Typography>
                ) : null}
                <Button
                    color={"primary"}
                    variant={"contained"}
                    className={classes.button}
                    onClick={this.saveProfile.bind(this)}
                >
                    Save
        </Button>
                <LinkColorless to={routes.auth.changeOrgEmail.route}>
                    <Button color={"primary"} className={classes.button}>
                        Change Organization Email
          </Button>
                </LinkColorless>
                <LinkColorless to={routes.auth.changePassword.route}>
                    <Button color={"primary"} className={classes.button}>
                        Change Password
          </Button>
                </LinkColorless>
            </div>
        );
    }
}

const styles = theme => ({
    root: {
        display: "flex",
        flexDirection: "column",
        alignSelf: "stretch",
        padding: theme.spacing(4),
        marginBottom: theme.spacing(8)
    },
    button: {
        marginTop: theme.spacing(2)
    },
    verify: {}
});
export default withStyles(styles)(Profile);
