import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Link} from "react-router-dom";

export default class LinkColorless extends Component
{
	render()
	{
		const disabled = this.props.disabled ? {pointerEvents: 'none'} : null;
		return (
			<Link {...this.props}
				style={{
					textDecoration: 'none',
					...disabled,
					...this.props.style
				}}>
				{this.props.children}
			</Link>
		);
	}
}

LinkColorless.propTypes = {
	style: PropTypes.object,
	disabled: PropTypes.bool
};