import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";
import Game from '../Game/Game';

interface Move {
    i: number
    color: string
    flips: Array<number>
}

const ENDPOINT = "http://localhost:9000";
const socket = io(ENDPOINT);

const makeMove = (move: Move) => {
  console.log("Make Move: ", move.i, "\nColor: ", move.color, "\nFlips: ", move.flips);
  // Emit to server, which propagates to other client
  socket.emit('move', move);
  return
}

socket.on('move', (msg: any) => {
  return msg;
});

const receiveMove = (msg: any) => {
  return msg;
}

export default function ClientComponent() {
  const [oppMove, setOppMove] = useState({i: -100, color: 'none', flips: []});

  useEffect(() => {
    socket.on('move', move => {
      console.log(move);
      setOppMove(move);
    });

  }, []);


  return (
    <div>
      <Game makeMove={(i) => makeMove(i)} receiveMove={oppMove}/>
    </div>
  );
}