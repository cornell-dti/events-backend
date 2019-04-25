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

	componentDidMount() {
		axios.get('/api/get_all_tags/')
			.then(response => {
				this.setState({ tags: response.data })
			})
			.catch(error => {
				if (error.response.status === 404)
					this.setState({ errors: ['An error has occurred while retrieving your profile. Please try again later.'] })
			})
	}

	newTags(addedTags) {
		const tags = this.props.tags;
		const newTag = addedTags[addedTags.length - 1];

		if (!tags.includes(newTag)) {
			tags.push(newTag);
			this.props.onNewTags(tags);
		}
	}
	render() {
		return (<Autocomplete
			label={"Tags"}
			placeholder={"Select at most 5 tags"}
			data={this.state.tags.map(tag =>
				({ value: tag.pk, label: tag.name }))}
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

// function mapStateToProps(state) {
// 	return {
// 		tags: []
// 	};
// }
// function mapDispatchToProps(dispatch) {
// 	return {

// 	};
// }

// TagField = connect(mapStateToProps, mapDispatchToProps)(TagField);
export default TagField;