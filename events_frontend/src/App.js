import React, { Component } from "react";
import CssBaseline from "@material-ui/core/CssBaseline";
import { Provider } from "react-redux";
import { createStore } from "redux";
import reducers from "./redux/reducers";
import Main from "./Main";
import { BrowserRouter } from "react-router-dom";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core";
import ReactGA from "react-ga";

const store = createStore(reducers, {});
const trackingId = "UA-146557345-1";

export default class App extends Component {
  constructor(props) {
    super(props);
    ReactGA.initialize(trackingId, {
      debug: true,
      gaOptions: {cookieDomain: 'none'}
    });
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
    fontFamily: "Dosis"
  },
  palette: {
    primary: {
      main: "#fd565b"
    },
    secondary: {
      main: "#fd565b"
    }
  }
});
