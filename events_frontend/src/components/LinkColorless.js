import React, { Component } from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export default class LinkColorless extends Component {
  render() {
    const disabled = this.props.disabled ? { pointerEvents: "none" } : null;
    if (!this.props.logout)
      return (
        <Link
          {...this.props}
          style={{
            textDecoration: "none",
            ...disabled,
            ...this.props.style
          }}
        >
          {this.props.children}
        </Link>
      );
    else
      return (
        <a
          href={this.props.to}
          style={{
            textDecoration: "none",
            ...disabled
          }}
        >
          {this.props.children}
        </a>
      );
  }
}

LinkColorless.propTypes = {
  style: PropTypes.object,
  to: PropTypes.string.isRequired,
  disabled: PropTypes.bool,
  logout: PropTypes.bool //"true" if logging out
};
