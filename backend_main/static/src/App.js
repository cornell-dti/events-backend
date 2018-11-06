import React, {Component} from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import {Provider} from "react-redux";
import {applyMiddleware, createStore} from "redux";
import reducers from "./redux/reducers";
import Main from "./Main";
import {BrowserRouter} from "react-router-dom";
import {createMuiTheme} from "@material-ui/core";
import MuiThemeProvider from "@material-ui/core/styles/MuiThemeProvider";
import {dataService, GET_TAGS} from "./redux/dataService";

const store = createStore(reducers, {}, applyMiddleware(dataService));
export default class App extends Component
{
	render()
	{
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

store.dispatch({type: GET_TAGS});

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