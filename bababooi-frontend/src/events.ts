import { Subject } from "rxjs";

export interface ErrorEvent {
  userMessage?: string;
}

export interface ServerJoinedEvent {
  host: string;
}

export const serverJoinSubject = new Subject<ServerJoinedEvent>();
export const errorSubject = new Subject<ErrorEvent>();
