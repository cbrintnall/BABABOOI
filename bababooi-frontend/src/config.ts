import * as process from "process";

interface Config {
  lobbyDomain: string;
  requestCorsMode: RequestMode
}

interface CommonConfig {
  backgroundColor: string;
  drawColor: string;
  lineWidth: number;
  firstBootTime: number;
  regularBootTime: number;
  bootTimeKey: string;
  loadingText: string;
  loadingTextSpeed: number;
  maxRoomIdLength: number;
  ownerTag: string;
}

const common: CommonConfig = {
  backgroundColor: "#000000",
  drawColor: "#FFFFFF",
  lineWidth: 2,
  firstBootTime: 10 * 1000, // 5 seconds
  regularBootTime: 3 * 1000, // 1 second
  bootTimeKey: "CACHED_BOOT_TIME",
  loadingText: "b o o t i n g 🅱 🅰 🅱 🅰 🅱 🅾 🅾 🅸 O S ... ",
  loadingTextSpeed: 125,
  maxRoomIdLength: 6,
  ownerTag: "(OWNER)"
};

const dev: Config = {
  lobbyDomain: "http://localhost:8080",
  requestCorsMode: 'cors'
};

const prod: Config = {
  lobbyDomain: "https://api.bababooi.club",
  requestCorsMode: 'cors'
};

export default {
  ...{ development: dev, production: prod, test: dev }[
    process.env.NODE_ENV || "development"
  ],
  ...common,
} as Config & CommonConfig;
