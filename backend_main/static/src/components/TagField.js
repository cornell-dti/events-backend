import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Autocomplete from "./Autocomplete";
import connect from "react-redux/es/connect/connect";

class TagField extends Component
{
	newTags(tags)
	{
		const newTag = tags[tags.length - 1];
		// if (!this.state.tags.includes(newTag)) //TODO update backend
		this.props.onNewTags(tags.map(tag => tag.value));
	}
	render()
	{
		return (<Autocomplete
			label={"Tags"}
			placeholder={"Select at most 5 tags"}
			data={this.props.tags}
			onUpdate={this.newTags.bind(this)}
			multiSelect={true} />);
	}
}

TagField.propTypes = {
	onNewTags: PropTypes.func.isRequired,
	tags: PropTypes.arrayOf(PropTypes.shape({
		value: PropTypes.string,
		label: PropTypes.string
	})).isRequired
};

function mapStateToProps(state)
{
	return {
		tags: state.tags.tags.map(tag => ({value: tag.name, label: tag.name}))
	};
}
function mapDispatchToProps(dispatch)
{
	return {

	};
}

TagField = connect(mapStateToProps, mapDispatchToProps)(TagField);
export default TagField;