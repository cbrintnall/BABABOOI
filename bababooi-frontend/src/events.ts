import { Subject } from "rxjs";

export interface ErrorEvent {
  good?: boolean
  userMessage?: string;
}

export interface ServerJoinedEvent {
  host: string;
}

export interface NewUserEvent {
  username: string;
}

export const newHappyMessageSubject = new Subject<string>();
export const newBBRoundSubject = new Subject();
export const newDisplayImageSubject = new Subject<any>();
export const newImageSubmittedSubject = new Subject<string>();
export const newImageSubmissionSubject = new Subject();
export const newUserSubject = new Subject<NewUserEvent>();
export const eraseCanvasSubject = new Subject();
export const serverJoinSubject = new Subject<ServerJoinedEvent>();
export const errorSubject = new Subject<ErrorEvent>();
