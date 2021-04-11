import { ModuleResolutionKind } from "typescript"

import * as process from 'process';

interface Config {
    backendDomain: string,
    lobbyDomain: string
}

interface CommonConfig {
    backgroundColor: string,
    drawColor: string,
    lineWidth: number,
    firstBootTime: number,
    regularBootTime: number,
    bootTimeKey: string,
    loadingText: string,
    loadingTextSpeed: number,
    maxRoomIdLength: number
}

const common: CommonConfig = {
    backgroundColor: "#000000",
    drawColor: "#FFFFFF",
    lineWidth: 10,
    firstBootTime: 10 * 1000, // 5 seconds
    regularBootTime: 3 * 1000, // 1 second
    bootTimeKey: "CACHED_BOOT_TIME",
    loadingText: "b o o t i n g 🅱 🅰 🅱 🅰 🅱 🅾 🅾 🅸 O S ... ",
    loadingTextSpeed: 125,
    maxRoomIdLength: 6
}

const dev: Config = {
    backendDomain: "http://127.0.0.1:5000/",
    lobbyDomain: "https://ayx8sw3us2.execute-api.us-west-2.amazonaws.com/test/game"
}

const prod: Config = {
    backendDomain: "",
    lobbyDomain: "https://api.bababooi.club"
}

export default ({ ...{ "development": dev, "production": prod, "test": dev }[process.env.NODE_ENV  || "development"], ...common }) as Config & CommonConfig