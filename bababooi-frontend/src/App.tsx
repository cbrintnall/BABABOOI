import "./App.css";
import 'aesthetic-css/aesthetic.css';

import React, { useEffect, useState } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import { LandingPage } from './pages/Landing';
import { NewGame } from './pages/NewGame';
import { io } from 'socket.io-client';
import cfg from "./config";
import { errorSubject, ErrorEvent } from "./events";

function NotificationsHost() {
  const [ error, setError ] = useState<ErrorEvent>();

  useEffect(() => {
    errorSubject.subscribe(errorEvent => 
      setError(errorEvent)
    )
  }, [])

  return (
    <div style={{ position: 'fixed', left: '30px', bottom: '30px' }}>
      {
        error && 
        <div className="aesthetic-notification is-active">
          <button 
            className="dismiss" 
            onClick={() => setError(undefined)}
          >
            X
          </button>
          <div 
            style={{ display: 'flex', flexDirection: 'row', paddingRight: '32px' }} 
            className="aesthetic-notification-content aesthetic-pepsi-red-color"
          >
            <div>
              <div className="aesthetic-effect-crt">
                <div style={{
                  height: '50px',
                  width: '50px',
                  background: 'url("/error.png")',
                  backgroundSize: 'contain'
                }}>
                </div>
              </div>
              <span style={{verticalAlign: "100%"}}> { `ERROR: ${error.userMessage}` } </span>
            </div>
          </div>
        </div>
      }
    </div>
  )
}

function App() {
  return (
    <Router>
      <div id="app">
        <NotificationsHost />
        <Switch>
          <Route
            path="/game"
            render={routeProps => <NewGame {...routeProps} />}
          />
          <Route 
            path="/" 
            render={routeProps => <LandingPage {...routeProps} />} 
          />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
