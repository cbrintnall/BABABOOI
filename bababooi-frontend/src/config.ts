import { ModuleResolutionKind } from "typescript"

import * as process from 'process';

interface Config {
    domain: string,
    lobbyDomain: string
}

interface CommonConfig {
    backgroundColor: string,
    drawColor: string,
    lineWidth: number
}

const common: CommonConfig = {
    backgroundColor: "#000000",
    drawColor: "#FFFFFF",
    lineWidth: 10
}

const dev: Config = {
    domain: "http://127.0.0.1:5000/",
    lobbyDomain: "https://ayx8sw3us2.execute-api.us-west-2.amazonaws.com/test/game"
}

const prod: Config = {
    domain: "",
    lobbyDomain: ""
}

export default ({ ...{ "development": dev, "production": prod, "test": dev }[process.env.NODE_ENV  || "development"], ...common }) as Config & CommonConfig