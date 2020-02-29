import React, { Component } from "react";
import PropTypes from "prop-types";
import CreatableSelect from "react-select/lib/Creatable";
import Select from "react-select";
import MenuItem from "@material-ui/core/MenuItem/MenuItem";
import TextField from "@material-ui/core/TextField/TextField";
import { withStyles } from "@material-ui/core";
import Chip from "@material-ui/core/Chip/Chip";


class Autocomplete extends Component {
  state = { selected: null };

  componentDidMount() {
    if (this.props.value !== this.state.selected && this.props.value !== [])
      this.setState({selected: this.props.value});
  }

  componentDidUpdate() {
    if (this.props.value !== this.state.selected && this.props.value !== [])
      this.setState({selected: this.props.value});
  }

  onSelect(val) {
    this.setState({ selected: val });
    this.props.onUpdate(val);
  }

  onChange(val) {
    if (this.props.onChange !== undefined) this.props.onChange(val);
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
        // isClearable
      />
    );
  }
}

Autocomplete.propTypes = {
  canCreate: PropTypes.bool,
  multiSelect: PropTypes.bool.isRequired,
  placeholder: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  // data: PropTypes.arrayOf(PropTypes.shape({
  // 	value: PropTypes.string,
  // 	label: PropTypes.string
  // })).isRequired,
  onChange: PropTypes.func,
  onUpdate: PropTypes.func.isRequired
};


function inputComponent({ inputRef, ...props }) {
  return <div ref={inputRef} {...props} />;
}

// Changes input into a text box
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
          ...props.innerProps
        }
      }}
      {...props.selectProps.textFieldProps}
    />
  );
}

// Changes the styling of the options
function Option(props) {
  return (
    <MenuItem
      buttonRef={props.innerRef}
      selected={props.isFocused}
      component="div"
      style={{ fontWeight: props.isSelected ? 500 : 300 }}
      {...props.innerProps}
    >
      {props.children}
    </MenuItem>
  );
}

function ValueContainer(props) {
  return (
    <div className={props.selectProps.classes.valueContainer}>
      {props.children}
    </div>
  );
}

// Changes the selects to a elliptical chip,
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

const components = {
  ValueContainer,
  Control,
  Option,
  // MultiValue,
};

const styles = theme => ({

  input: {
    display: "flex", // causes the thing to go down
    height: "80%",
    padding: 0
  },
  valueContainer: {
    display: "flex",
    flex: 1,
    flexWrap: "wrap",
    alignItems: "center",
    paddingLeft: 0
  }
});

export default withStyles(styles, { withTheme: true })(Autocomplete);
