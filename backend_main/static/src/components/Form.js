import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Snackbar from "@material-ui/core/Snackbar/Snackbar";

/**
 * Hides HTML containing Django form in background. Allows parent to call submit().
 * Access form fields by ID.
 */
export default class Form extends Component
{
	constructor(props)
	{
		super(props);
		this.setState({form: "", error: ""});
		this.getForm();
	}
	componentDidMount()
	{
		this.props.submit(this.submit.bind(this));
	}
	getForm()
	{
		fetch(this.props.url)
			.then(res => res.text())
			.then(html => this.setState({form: html}))
			.catch(err => this.setState({error: err}));
	}
	removeSubmitButton()
	{
		const submitButton = document.getElementsByName("submit")[0];
		if (submitButton != null)
			submitButton.name = "";
	}
	submit()
	{
		const form = document.getElementsByTagName("form")[0]; //NOTE: assumes 1 form per page
		form.target = "formFrame";
		form.action = this.props.url;
		this.removeSubmitButton();
		form.submit();
	}
	render()
	{
		return (
			<React.Fragment>
				<iframe width={0} height={0} frameBorder={0} name={"formFrame"} />
				<div hidden={true} dangerouslySetInnerHTML={{__html: this.state.form}} />
				<Snackbar open={this.state.error !== ""}
					message={this.state.error}/>
			</React.Fragment>
		);
	}
}

Form.propTypes = {
	url: PropTypes.string.isRequired,
	submit: PropTypes.func.isRequired //function that allow parent to call submit()
};