import React, { CSSProperties } from "react";
import { RouteComponentProps } from "react-router-dom";
import ReactTypingEffect from "react-typing-effect";
import cfg from '../config';

const landingStyles: CSSProperties = {
  height: "100%",
  width: "100%",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
};

class LandingPage extends React.Component<RouteComponentProps, {}> {
  /**
   * if first boot, we wait a little longer for the effect to finish,
   * otherwise if we can access local storage check if we have a stored value,
   * if no access to localstorage assume we want fastest entry
   */
  getBootTimeout(): number {
    if (localStorage) {
      const cachedValue = localStorage.getItem(cfg.bootTimeKey);
      const returned = (cachedValue && parseInt(cachedValue, 10)) || cfg.firstBootTime;

      if (returned === cfg.firstBootTime) {
        localStorage.setItem(cfg.bootTimeKey, cfg.regularBootTime.toString());
      }

      return returned;
    } else {
      return cfg.regularBootTime
    }
  }

  componentDidMount() {
    setTimeout(() => {
      this.props.history.push('/game')
    }, this.getBootTimeout());
  }

  render() {
    return (
      <div style={landingStyles} className="aesthetic-black-bg-color">
        <div className="aesthetic-effect-crt">
          <video
            src="https://media.giphy.com/media/gQbVzXQQbGO7C/giphy.mp4"
            width="400"
            height="300"
            loop
          >
          </video>
        </div>
        <div style={{ margin: '12p' }} >
          <h3 className="aesthetic-light-purple-color">
            <ReactTypingEffect
              className="aesthetic-white-color"
              text={["b o o t i n g 🅱 🅰 🅱 🅰 🅱 🅾 🅾 🅸 O S ... "]}
              eraseDelay={99999999}
              eraseSpeed={99999999}
              speed={cfg.loadingTextSpeed}
              cursor={"█"}
            />
          </h3>
        </div>
        <div
          className="aesthetic-windows-95-boot-loader"
          style={{ width: "35%", margin: "12px" }}
        >
          <div></div>
        </div>
      </div>
    );
  }
}

export { LandingPage };
