import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Autocomplete from "./Autocomplete";
import connect from "react-redux/es/connect/connect";
import axios from 'axios';

class TagField extends Component {

	constructor(props) {
		super(props);
		this.state = { tags: [] }
	}

	isEqual(tags, t) {
		for (var i = 0; i < tags.length; i++) {
			if (tags[i].value === t.value) return true;
		}
	}
	componentDidMount() {
		axios.get('/api/get_all_tags/')
			.then(response => {
				this.setState({ tags: response.data.map(tag => ({ value: tag.pk, label: tag.name })) })
			})
			.catch(error => {
				if (error.response.status === 404)
					this.setState({ errors: ['An error has occurred while retrieving your profile. Please try again later.'] })
			})
	}

	newTags(addedTags) {
		this.props.onNewTags(addedTags);
	}

	inputValue() {
		if (this.props.tags === undefined) return
		const tags = this.props.tags
		const newTag = tags.pop()
		if (newTag === undefined || this.isEqual(this.props.tags, newTag)) return tags
		tags.push(newTag)
		return tags
	}
	// MAKE CHECK THAT ONLY CAN ADD 5 EVENTS
	// EVEN WHEN PRESS CANCEL CHANGES THE EVENT
	render() {
		return (<Autocomplete
			label={"Tags"}
			value={this.inputValue()}
			placeholder={"Select at most 5 tags"}
			data={this.state.tags}
			onUpdate={this.newTags.bind(this)}
			multiSelect={true} />);
	}
}

TagField.propTypes = {
	onNewTags: PropTypes.func.isRequired,
	tags: PropTypes.arrayOf(PropTypes.shape({
		value: PropTypes.number,
		label: PropTypes.string,
	})).isRequired
};

export default TagField;