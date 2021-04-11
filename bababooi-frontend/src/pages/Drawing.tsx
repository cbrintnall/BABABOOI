import React, { createRef, useContext } from "react";
import { RouteComponentProps } from "react-router-dom";
import { parse as parseQueryString } from "querystring";
import { io } from "socket.io-client";
import { Socket } from "socket.io";
import { Drawer } from "../Drawing";
import cfg from "../config";
import { eraseCanvasSubject, newDisplayImageSubject, newImageSubmissionSubject, newImageSubmittedSubject } from "../events";
import { getUsername } from "../App";

type GameUrlParams = {
  gameId: string;
};

type Player = {
  name: string;
  isOwner: boolean;
};

type BabaBooiSpecificData = {
  startingClassName: string;
  targetClassName: string;
  startingImg: any;
  startDelayInSecs: number;
  roundLengthInSecs: number;
  newRound: boolean;
  state: "playing" | "reviewing";
};

type GameSpecificData = BabaBooiSpecificData;

type GameState = {
  room: string;
  gameType: string;
  gameState: string;
  gameSpecificData: GameSpecificData;
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
      drawWidth: 512,
      drawHeight: 512,
    };

    this.drawDivParent = createRef<HTMLDivElement>();
  }

  isOwner(): boolean {
    const idx = this.state.gameState?.players?.filter(plr => plr.name === getUsername());

    if (idx && idx.length>0) {
      return idx[0].isOwner;
    }

    return false;
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
    }
  }

  getRoundInfoComponents() {
    const { startingClassName, targetClassName } = this.state.gameState!.gameSpecificData;

    return (
      <h3 style={{paddingLeft: '12px'}}>
        ok, heres a <u className="aesthetic-green-color">{startingClassName}</u>, make it think it's a <u className="aesthetic-arizona-pink-color">{targetClassName}</u>
      </h3>
    )
  }

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
      this.connection = (io(host, {
        reconnectionAttempts: 5,
      }) as unknown) as Socket<any, any>;

      this.connection.on("gamestate", (state: string) => {
        this.setState({ gameState: JSON.parse(state) }, () => {
          console.log(this.state);

          if (this.state.gameState?.room) {
            localStorage.setItem("LAST_JOINED", this.state.gameState?.room);
          }

          if (this.state.gameState?.gameSpecificData.startingImg) {
            newDisplayImageSubject.next(
              this.state.gameState?.gameSpecificData.startingImg
            );
          }
        });
      });

      this.connection.emit(
        "handshake",
        JSON.stringify({ room: this.getGameId() })
      );

      newImageSubmittedSubject.subscribe((img) => {
        console.log(img)

        const submissionData = {
          data: img.split("base64,")[1],
          room: this.getGameId(),
          name: getUsername(),
        };

        this.connection?.emit("submit_image", JSON.stringify(submissionData));
      });
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

      this.props.history.push("/game");
    }
  }

  forceEnd() {
    if(this.connection) {
      this.connection.emit(
        "is_round_over",
        JSON.stringify({ room: this.getGameId() })
      )
    }
  }

  render() {
    return (
      <div
        style={{ height: "100%", width: "100%" }}
        className="aesthetic-blue-bg-color"
      >
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
              {this.state.gameState?.gameState === "playing" && (
                <span style={{ marginLeft: "12px", marginRight: "12px" }}>
                  {" "}
                  |{" "}
                </span>
              )}
              {this.state.gameState?.gameState === "playing" && (
                <div className="aesthetic-windows-95-button">
                  <button onClick={() =>{ 
                    if (this.state.gameState?.gameState === "playing") {
                      newImageSubmissionSubject.next() 
                    } else {
                      setTimeout(() => eraseCanvasSubject.next(), 100)
                    }
                  }}>
                    SUBMIT
                  </button>
                </div>
              )}
              {this.state.gameState?.gameState === "playing" && this.isOwner() && (
                <div className="aesthetic-windows-95-button">
                  <button onClick={() => this.forceEnd()}>
                    END
                  </button>
                </div>
              )}
              {/* <div className="aesthetic-windows-95-button">
                <button onClick={() => eraseCanvasSubject.next()}>CLEAR</button>
              </div> */}
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
                style={{
                  marginLeft: "4px",
                  width: "100%",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <div style={{ width: "100%" }}>
                  <h2 style={{ paddingLeft: "24px", color: "black" }}>
                    { `ROOM ID: "${this.state.gameState?.room}" <== send to your 🌈f r i e n d s🌈` }
                  </h2>
                  <h4 className="aesthetic-green-color"> how to plaaay: </h4>
                  <ol>
                    <li> view base image </li>
                    <li> acknowledge what it is (ex: <u className="aesthetic-arizona-pink-color">cat</u>) </li>
                    <li> acknowledge what you're supposed to draw (ex: <u className="aesthetic-arizona-blue-color">dog</u>) </li>
                    <li> draw over <u className="aesthetic-arizona-pink-color">cat</u> and try to make the Ą͝Į̕ think it's <u className="aesthetic-arizona-blue-color">dog</u> </li>
                    <li> a̭͈̰̬d̗͕̞̗̩͢ḓ̢̘̟̣r̸̺̬͚̩̪̬̪e͚̹͎̤͟s̢͏̼̗͍s͙̫͢͡ ̛̯̟̜̭͎͠y̡͈̬̟͓ͅͅọ̕u͇̻̫̰̫͉r҉͚̞͕̝̭͇̭̻ ̢̖͔̣͕̗̪͝͠i̻̮͇̥n̤̬͇̲̺̝̻͔͜n̡͏̳e̹̮̱̫̱̼͜r̷̲̺͇̜͈̬̭ ̰̬̘͓̕f̛͍̺̕è͉̪̫͉̺̜a̯̟͈͖̻̫̱͡ṛ͉̫̤̼̰̘ͅs҉͇̻̬̗͞ </li>
                    <li> win! </li>
                  </ol>
                  <h4 className="aesthetic-pink-color"> R U L E S: </h4>
                  <ol>
                    <li> you cannot erase, get it right the first time </li>
                  </ol>
                </div>
                <Drawer
                  height={this.state.drawHeight}
                  width={this.state.drawWidth}
                />
                <div style={{ width: "100%" }}>
                  {
                    this.state.gameState?.gameState === "playing" &&
                    this.getRoundInfoComponents()
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

export { DrawingGame };
