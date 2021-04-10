import { Drawer } from './Drawing';
import React, { useEffect } from 'react';

import { io } from 'socket.io-client';
import cfg from "./config";

const socket = io(cfg.domain);

function App() {
  const requestId = () => {
    fetch(cfg.lobbyDomain, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow'
    })
    .then(console.log)
    .catch(console.error)
  }

  return (
    <div className="App">
      <button onClick={requestId}>
        Send Create Request
      </button>
      <Drawer />
    </div>
  );
}

export default App;
