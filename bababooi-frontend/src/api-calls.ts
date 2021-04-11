import cfg from "./config";
import {getUsername} from './App';

interface GameJoinResponse {
  statusCode: number;
  host: string;
  gameId: string;
}

export const requestGame = (
  username: string,
  gameId?: string
): Promise<string | GameJoinResponse> => {
  const url = [
    cfg.lobbyDomain,
    `?userId=${username}`,
    gameId ? `&gameId=${gameId}` : "",
  ].join("");

  return fetch(url, { redirect: "follow" })
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
      return "There was an error finding the server";
    }) as Promise<string | GameJoinResponse>;
};
