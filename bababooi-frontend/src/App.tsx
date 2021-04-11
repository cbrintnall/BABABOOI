import "./App.css";
import "aesthetic-css/aesthetic.css";

import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import { LandingPage } from "./pages/Landing";
import { NewGame } from "./pages/NewGame";
import { LoginScreen } from "./pages/LoginScreen";
import { errorSubject, ErrorEvent, newUserSubject } from "./events";
import { DrawingGame } from "./pages/Drawing";

type User = {
  username: string;
};

export const UserContext = React.createContext<User | undefined>(undefined);

export const getUsername = (): string | undefined => {
  return localStorage.getItem("USERNAME") || undefined;
};

function NotificationsHost() {
  const [error, setError] = useState<ErrorEvent>();

  useEffect(() => {
    errorSubject.subscribe((errorEvent) => setError(errorEvent));
  }, []);

  const url = error?.good ? "/happy.png" : "/error.png";
  const msg = error?.good ? error?.userMessage : `ERROR: ${error?.userMessage}`

  return (
    <div style={{ position: "fixed", left: "30px", bottom: "30px" }}>
      {error && (
        <div className="aesthetic-notification is-active">
          <button className="dismiss" onClick={() => setError(undefined)}>
            X
          </button>
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              paddingRight: "32px",
            }}
            className={`aesthetic-notification-content ${error?.good ? "aesthetic-arizona-blue-color":"aesthetic-pepsi-red-color"}`}
          >
            <div>
              <div className="aesthetic-effect-crt">
                <div
                  style={{
                    height: "50px",
                    width: "50px",
                    background: `url(${url})`,
                    backgroundSize: "contain",
                  }}
                ></div>
              </div>
              <span style={{ verticalAlign: "100%" }}>
                {" "}
                {msg}{" "}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  useEffect(() => {
    if (localStorage) {
      newUserSubject.subscribe((user) => {
        localStorage.setItem("USERNAME", user.username);
      });
    }
  }, []);

  return (
    <Router>
      <div id="app">
        <NotificationsHost />
        <Switch>
          <Route
            exact
            path="/login"
            render={(routeProps) => {
              if (getUsername()) {
                return <Redirect to="/game" />;
              }

              return <LoginScreen {...routeProps} />;
            }}
          />
          <Route
            exact
            path="/drawing/:gameId"
            render={(routeProps) => {
              if (!getUsername()) {
                return <Redirect to="/login" />;
              }

              return <DrawingGame {...routeProps} />;
            }}
          />
          <Route
            exact
            path="/game"
            render={(routeProps) => {
              if (!getUsername()) {
                return <Redirect to="/login" />;
              }

              return <NewGame {...routeProps} />;
            }}
          />
          <Route
            exact
            path="/"
            render={(routeProps) => <LandingPage {...routeProps} />}
          />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
