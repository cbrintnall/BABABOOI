import React, { CSSProperties } from "react";
import { RouteComponentProps } from "react-router-dom";
import { requestGame } from "../api-calls";
import cfg from "../config";
import { errorSubject, serverJoinSubject } from "../events";
import { getUsername } from '../App';

const defaultId = "ZGH69Q";

const style: CSSProperties = {
  height: "100%",
  width: "100%",
  display: "flex",
  flexDirection: "column",
};

type NewGameState = {
  joining: boolean;
  joinId: string;
};

class NewGame extends React.Component<RouteComponentProps, NewGameState> {
  constructor(props: RouteComponentProps) {
    super(props);

    this.state = {
      joining: false,
      joinId: defaultId,
    };
  }

  tryServerJoin() {
    if (!getUsername()) {
      return;
    }

    requestGame(
      getUsername()!,
      this.hasValidJoinId() ? this.state.joinId : undefined
    )
      .then((result) => {
        // if returned a string, it's an error
        if (typeof result === "string" || (result as any).errorMessage) {
          errorSubject.next({ userMessage: result as string });
          console.error(result)
        } else {
          // otherwise we've received a valid payload
          // const gameUrl =
          //   process.env.NODE_ENV === "development"
          //     ? cfg.backendDomain
          //     : result.host;

          this.props.history.push(`/drawing/${result.gameId}?host=${result.host}`);
        }
      })
      .catch((err) => {
        errorSubject.next({ userMessage: err });
      });
  }

  hasValidJoinId(): boolean {
    return (
      this.state.joining &&
      this.state.joinId !== defaultId &&
      this.state.joinId.length === cfg.maxRoomIdLength
    );
  }

  render() {
    return (
      <div className="aesthetic-blue-bg-color" style={style}>
        <div>
          <h1
            style={{ paddingLeft: "24px" }}
            className="aesthetic-effect-text-glitch"
            data-glitch="WELCOME"
          >
            WELCOME
          </h1>
          <div
            className="aesthetic-windows-95-modal"
            style={{ margin: "24px", marginLeft: "64px" }}
          >
            <div className="aesthetic-windows-95-modal-title-bar">
              <div className="aesthetic-windows-95-modal-title-bar-text">
                GAME.EXE
              </div>
              <div className="aesthetic-windows-95-modal-title-bar-controls">
                <div className="aesthetic-windows-95-button-title-bar">
                  <div style={{ display: "flex", flexDirection: "row" }}>
                    <button onClick={() => console.error("no")}>X</button>
                  </div>
                </div>
              </div>
            </div>
            <div className="aesthetic-windows-95-modal-content">
              <div
                style={{
                  height: "30vh",
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "center",
                  justifyContent: "space-evenly",
                  cursor: "pointer",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{ width: "16em" }}
                    className="interactable aesthetic-windows-95-button"
                  >
                    <button
                      style={{ padding: "12px" }}
                      onClick={() => this.tryServerJoin()}
                    >
                      CREATE NEW GAME ?
                    </button>
                  </div>
                  <hr />
                  <div
                    style={{ width: "16em" }}
                    className="interactable aesthetic-windows-95-button"
                  >
                    <button
                      style={{ padding: "12px" }}
                      onClick={() =>
                        this.setState({ joining: !this.state.joining })
                      }
                    >
                      {this.state.joining ? "BACK OUT" : "JOIN A GAME ?"}
                    </button>
                  </div>
                  <hr
                    style={{
                      visibility: this.state.joining ? "visible" : "hidden",
                    }}
                  />
                  {
                    <div
                      style={{
                        visibility: this.state.joining ? "visible" : "hidden",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        flexDirection: "column",
                      }}
                    >
                      <div>
                        <span> game id: </span>
                      </div>
                      <div
                        style={{
                          padding: "12px",
                          display: "flex",
                          flexDirection: "row",
                        }}
                      >
                        <input
                          style={{ flexShrink: 0 }}
                          maxLength={cfg.maxRoomIdLength}
                          className="aesthetic-windows-95-text-input"
                          type="text"
                          value={this.state.joinId}
                          onChange={(e) =>
                            this.setState({
                              joinId: e.target.value.toUpperCase(),
                            })
                          }
                        />
                        <div
                          className="interactable aesthetic-windows-95-button"
                          style={{ flexShrink: 3 }}
                        >
                          <button onClick={() => this.setState({ joinId: "" })}>
                            X
                          </button>
                        </div>
                        <div
                          className="interactable aesthetic-windows-95-button"
                          style={{ flexShrink: 3 }}
                        >
                          <button
                            onClick={() => this.tryServerJoin()}
                            disabled={
                              this.state.joinId.length !==
                                cfg.maxRoomIdLength ||
                              this.state.joinId === defaultId
                            }
                          >
                            join
                          </button>
                        </div>
                      </div>
                    </div>
                  }
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export { NewGame };
