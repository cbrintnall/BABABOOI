import React, { CSSProperties } from "react";
import { RouteComponentProps } from "react-router-dom";
import { errorSubject, newUserSubject } from "../events";

const style: CSSProperties = {
  width: "100%",
  height: "100%",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
};

type LoginState = {
  login: string;
};

export class LoginScreen extends React.Component<
  RouteComponentProps,
  LoginState
> {
  constructor(props: RouteComponentProps) {
    super(props);

    this.state = {
      login: "",
    };
  }

  render() {
    return (
      <div className="aesthetic-blue-bg-color" style={style}>
        <div
          style={{ margin: "12px" }}
          className="aesthetic-windows-95-container"
        >
          <span> LOGIN: </span>
          <hr />
          <div>
            <input
              className="aesthetic-windows-95-text-input"
              type="text"
              value={this.state.login}
              onChange={(e) => this.setState({ login: e.target.value })}
            />
            <div style={{marginTop: "6px" }} className="aesthetic-windows-95-button">
              <button 
                disabled={this.state.login.length===0}
                onClick={() => {
                  if (this.state.login.length > 0) {
                    newUserSubject.next({ username: this.state.login });
                    errorSubject.next({ good: true, userMessage: `Welcome, ${this.state.login}` })
                    this.props.history.push('/game')
                  }
                }}
              >
                LOGIN
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
