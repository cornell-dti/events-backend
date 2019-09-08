import React, { Component } from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Provider } from "react-redux";
import { createStore } from "redux";
import reducers from "./redux/reducers";
import Main from "./Main";
import { BrowserRouter } from "react-router-dom";
import { createMuiTheme } from "@material-ui/core";
import MuiThemeProvider from "@material-ui/core/styles/MuiThemeProvider";
import ReactGA from 'react-ga';

const store = createStore(reducers, {});

export default class App extends Component {
	constructor() {
    super();
    ReactGA.initialize('UA-146557345-1');
		ReactGA.pageview(window.location.pathname + window.location.search);
	}

	render() {
		return (
			<Provider store={store}>
				<BrowserRouter>
					<MuiThemeProvider theme={theme}>
						<CssBaseline />
						<Main />
					</MuiThemeProvider>
				</BrowserRouter>
			</Provider>
		);
	}
}

const theme = createMuiTheme({
	typography: {
		fontFamily: 'Dosis'
	},
	palette: {
		primary: {
			main: '#fd565b'
		},
		secondary: {
			main: '#fd565b'
		}
	}
});