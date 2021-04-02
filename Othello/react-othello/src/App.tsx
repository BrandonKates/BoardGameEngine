import React, { useState } from 'react';
import {
  MemoryRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";

import ClientComponent from './components/ClientComponent/ClientComponent';
import './App.scss';

import { io } from "socket.io-client";

const ENDPOINT = "localhost:9000";
const socket = io(ENDPOINT);

function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/game">
            <ClientComponent socket={socket}/>
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home(){
  const [redirect, setRedirect] = useState(false);
  const [roomId, setRoomId] = useState("");
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    socket.emit('joined', roomId);
    setRedirect(true);
  }
  if(redirect){
    return (<Redirect to={{
      pathname: "/game",
      state: {
        roomId: roomId
      }
    }} />);
  }
  return (
    <form onSubmit={handleSubmit}>
      <label>
        Enter Room Number (1-10)
        <input
          type='text'
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        />
      </label>
      <input type='submit' value="Submit" />
    </form>
  )
}

export default App;
