import { RequestOptions } from "https";
import cfg from "./config";

interface GameJoinResponse {
  statusCode: number;
  host: string;
  gameId: string;
}

export const requestGame = (
  username: string,
  gameId?: string
): Promise<string | GameJoinResponse> => {
  const data = {
    userId: username,
    gameId
  }

  const options: RequestInit = { 
    redirect: "follow", 
    method: "POST", 
    body: JSON.stringify(data), 
    mode: cfg.requestCorsMode 
  }

  return fetch(cfg.lobbyDomain, options)
    .then((res) => {
      switch (res.status) {
        case 200:
          return res.json();
        case 404:
          return `Couldn't find room ${gameId}`;
        case 400:
          return `${gameId} is a valid room ID.`;
        case 503:
          return "No capacity for a new game, try again soon!";
      }
    })
    .then((data) => {
      return data;
    })
    .catch((err) => {
      console.error(err)
      return "There was an error finding the server";
    }) as Promise<string | GameJoinResponse>;
};
