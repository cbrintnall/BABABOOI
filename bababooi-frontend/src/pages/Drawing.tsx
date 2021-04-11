import React, { createRef, useContext } from "react";
import { RouteComponentProps } from "react-router-dom";
import { parse as parseQueryString } from "querystring";
import { io } from "socket.io-client";
import { Socket } from "socket.io";
import { Drawer } from "../Drawing";
import cfg from "../config";
import { eraseCanvasSubject, newImageSubmissionSubject } from "../events";
import { getUsername, UserContext } from "../App";

type GameUrlParams = {
  gameId: string;
};

type Player = {
  name: string;
  isOwner: boolean;
};

type GameState = {
  room: string;
  gameType: string;
  gameState: string;
  gameSpecificData: {};
  players?: Player[];
};

type DrawingGameState = {
  drawWidth: number;
  drawHeight: number;
  gameState?: GameState;
};

class DrawingGame extends React.Component<
  RouteComponentProps<GameUrlParams>,
  DrawingGameState
> {
  drawDivParent: React.RefObject<HTMLDivElement>;
  connection?: Socket<any, any>;

  constructor(props: RouteComponentProps<GameUrlParams>) {
    super(props);

    this.state = {
      drawWidth: 500,
      drawHeight: 500,
      // gameState: {
      //   room: "ZZZAAA",
      //   gameType: "bababooi",
      //   gameState: "playing",
      //   gameSpecificData: {},
      //   players: [
      //     {
      //       name: "player1",
      //       isOwner: true,
      //     },
      //     {
      //       name: "player2",
      //       isOwner: false,
      //     },
      //   ],
      // },
    };

    this.drawDivParent = createRef<HTMLDivElement>();
  }

  componentDidMount() {
    this.handleJoin();

    document.onkeydown = (ev: KeyboardEvent) => {
      if (ev.ctrlKey && ev.key === "z") {
      }
    };

    window.onresize = (e: UIEvent) => {
      if (this.drawDivParent.current) {
        this.sizeCanvas();
      }
    };

    if (this.drawDivParent.current) {
      this.sizeCanvas();
    }
  }

  sizeCanvas() {
    if (this.drawDivParent.current) {
      const drawHeight = Math.min(
        window.innerHeight,
        this.drawDivParent.current.clientHeight
      );

      // console.log(drawHeight)

      // this.setState({
      //   drawHeight,
      //   drawWidth:drawHeight
      // })
    }
  }

  undo() {}

  handleJoin() {
    const queryStrings = parseQueryString(this.props.location.search);
    const cleanedQs = Object.keys(queryStrings)
      .map((key) => {
        return { old: key, new: key.replace(/\?/gi, "") };
      })
      .reduce((lastVal, currVal) => {
        return { ...lastVal, [currVal.new]: queryStrings[currVal.old] };
      }, {});

    const host = (cleanedQs as any).host;

    if (host) {
      this.connection = (io(host, { reconnectionAttempts: 5 }) as unknown) as Socket<any, any>;

      this.connection.on("gamestate", (state: string) => {
        console.log(JSON.parse(state));
        this.setState({ gameState: JSON.parse(state) }, () => {
          if (this.state.gameState?.room) {
            localStorage.setItem("LAST_JOINED", this.state.gameState?.room);
          }
        });
      });

      this.connection.emit(
        "handshake",
        JSON.stringify({ room: this.getGameId() })
      );
    }
  }

  getGameId(): string {
    return this.props.match.params.gameId;
  }

  startSession() {
    if (this.connection) {
      this.connection.emit(
        "start_game",
        JSON.stringify({ room: this.getGameId(), name: getUsername() })
      );
    }
  }

  leaveSession() {
    if (this.connection) {
      this.connection.emit(
        "leave_game",
        JSON.stringify({ room: this.getGameId(), name: getUsername() })
      );

      this.props.history.push('/')
    }
  }

  render() {
    return (
      <div
        style={{ height: "100%", width: "100%" }}
        className="aesthetic-blue-bg-color"
      >
        <h2
          style={{ paddingLeft: "24px" }}
          className="aesthetic-effect-text-glitch"
          data-glitch="_-_-_-++_-_--__"
        >
          ROOM ID: { this.state.gameState?.room }
        </h2>
        <div
          className="aesthetic-windows-95-modal"
          style={{ marginLeft: "64px" }}
        >
          <div className="aesthetic-windows-95-modal-title-bar">
            <div className="aesthetic-windows-95-modal-title-bar-text">
              DRAWING.EXE
            </div>
            <div className="aesthetic-windows-95-modal-title-bar-controls">
              <div className="aesthetic-windows-95-button-title-bar">
                <div style={{ display: "flex", flexDirection: "row" }}>
                  <button onClick={() => this.leaveSession()}>X</button>
                </div>
              </div>
            </div>
          </div>
          <div className="aesthetic-windows-95-modal-content">
            <div
              style={{
                display: "flex",
                flexDirection: "row",
              }}
            >
              {this.state.gameState?.gameState === "lobby" && (
                <div className="aesthetic-windows-95-button">
                  <button onClick={() => this.startSession()}>START</button>
                </div>
              )}
              <div className="aesthetic-windows-95-button">
                <button onClick={() => this.leaveSession()}>LEAVE</button>
              </div>
              <span style={{ marginLeft: "12px", marginRight: "12px" }}>
                {" "}
                |{" "}
              </span>
              {this.state.gameState?.gameState === "playing" && (
                <div className="aesthetic-windows-95-button">
                  <button onClick={() => newImageSubmissionSubject.next()}>SUBMIT</button>
                </div>
              )}
              <div className="aesthetic-windows-95-button">
                <button onClick={() => eraseCanvasSubject.next()}>CLEAR</button>
              </div>
            </div>
            <hr />
            <div style={{ display: "flex", flexDirection: "row" }}>
              <div className="aesthetic-windows-95-container-indent">
                <span className="aesthetic-arizona-pink-color"> PLAYERS: </span>
                <ul>
                  {this.state.gameState?.players &&
                    this.state.gameState.players.map((player) => {
                      return (
                        <li>
                          {player.name} {player.isOwner ? cfg.ownerTag : ""}
                        </li>
                      );
                    })}
                </ul>
              </div>
              <div
                ref={this.drawDivParent}
                className="aesthetic-windows-95-container-indent"
                onChange={console.log}
                style={{
                  marginLeft: "4px",
                  width: "100%",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <Drawer
                  height={this.state.drawHeight}
                  width={this.state.drawWidth}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export { DrawingGame };
