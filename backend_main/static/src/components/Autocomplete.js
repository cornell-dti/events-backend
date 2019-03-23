import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CreatableSelect from "react-select/lib/Creatable";
import Select from "react-select";
import MenuItem from "@material-ui/core/MenuItem/MenuItem";
import TextField from "@material-ui/core/TextField/TextField";
import { withStyles } from "@material-ui/core";
import Chip from "@material-ui/core/Chip/Chip";
import Paper from "@material-ui/core/Paper/Paper";
import Typography from "@material-ui/core/Typography/Typography";

class Autocomplete extends Component {
	state = { selected: null };
	
	componentDidMount() {
		this.setState({ selected: this.props.value});
  	}	
	onSelect(val) {
		this.setState({ selected: val });
		this.props.onUpdate(val);
	}
	onChange(val) {
		if (this.props.onChange !== undefined)
			this.props.onChange(val);
	}
	render() {
		const { classes } = this.props;
		const Field = this.props.canCreate ? CreatableSelect : Select;
		return (
			<Field
				classes={classes}
				value={this.state.selected}
				onChange={this.onSelect.bind(this)}
				onInputChange={this.onChange.bind(this)}
				options={this.props.data}
				textFieldProps={{
					label: this.props.label,
					InputLabelProps: { shrink: true }
				}}
				placeholder={this.props.placeholder}
				components={components}
				isMulti={this.props.multiSelect}
			/>
		);
	}
}

Autocomplete.propTypes = {
	canCreate: PropTypes.bool,
	multiSelect: PropTypes.bool.isRequired,
	placeholder: PropTypes.string.isRequired,
	label: PropTypes.string.isRequired,
	data: PropTypes.arrayOf(PropTypes.shape({
		value: PropTypes.string,
		label: PropTypes.string
	})).isRequired,
	onChange: PropTypes.func,
	onUpdate: PropTypes.func.isRequired
};

function NoOptionsMessage(props) {
	return (
		<Typography
			color="textSecondary"
			className={props.selectProps.classes.noOptionsMessage}
			{...props.innerProps}
		>
			{props.children}
		</Typography>
	);
}

function inputComponent({ inputRef, ...props }) {
	return <div ref={inputRef} {...props} />;
}

function Control(props) {
	return (
		<TextField
			fullWidth
			InputProps={{
				inputComponent,
				inputProps: {
					className: props.selectProps.classes.input,
					inputRef: props.innerRef,
					children: props.children,
					...props.innerProps,
				},
			}}
			{...props.selectProps.textFieldProps}
		/>
	);
}

function Option(props) {
	return (
		<MenuItem
			buttonRef={props.innerRef}
			selected={props.isFocused}
			component="div"
			style={{ fontWeight: props.isSelected ? 500 : 400 }}
			{...props.innerProps}>
			{props.children}
		</MenuItem>
	);
}

function Placeholder(props) {
	return (
		<Typography
			color="textSecondary"
			className={props.selectProps.classes.placeholder}
			{...props.innerProps}>
			{props.children}
		</Typography>
	);
}

function SingleValue(props) {
	return (
		<Typography className={props.selectProps.classes.singleValue} {...props.innerProps}>
			{props.children}
		</Typography>
	);
}

function ValueContainer(props) {
	return <div className={props.selectProps.classes.valueContainer}>{props.children}</div>;
}

function MultiValue(props) {
	return (
		<Chip
			tabIndex={-1}
			label={props.children}
			className={props.selectProps.classes.chip}
			onDelete={event => {
				props.removeProps.onClick();
				props.removeProps.onMouseDown(event);
			}}
		/>
	);
}

function Menu(props) {
	return (
		<Paper square className={props.selectProps.classes.paper} {...props.innerProps}>
			{props.children}
		</Paper>
	);
}

const components = {
	NoOptionsMessage,
	Option,
	Control,
	Placeholder,
	SingleValue,
	MultiValue,
	ValueContainer,
	Menu
};

const styles = (theme) => ({
	input: {
		display: 'flex',
		padding: 0
	},
	valueContainer: {
		display: 'flex',
		flexWrap: 'wrap',
		flex: 1,
		alignItems: 'center'
	},
	chip: {
		margin: `${theme.spacing.unit / 2}px ${theme.spacing.unit / 4}px`
	},
	placeholder: {
		position: 'absolute',
		left: 2,
		fontSize: 16
	},
	noOptionsMessage: {
		padding: `${theme.spacing.unit}px ${theme.spacing.unit * 2}px`,
	},
	singleValue: {
		fontSize: 16,
	},
	paper: {
		position: 'absolute',
		zIndex: 1,
		marginTop: theme.spacing.unit,
		left: 0,
		right: 0
	}
});

export default withStyles(styles, { withTheme: true })(Autocomplete);