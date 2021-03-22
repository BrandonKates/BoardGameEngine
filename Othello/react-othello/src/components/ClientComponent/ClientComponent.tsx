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


export default function ClientComponent() {
  const [oppMove, setOppMove] = useState({i: -100, color: 'none', flips: []});
  const [gameStatus, setGameStatus] = useState('Waiting for second player');
  const [startGame, setStartGame] = useState(false);
  const [color, setColor] = useState("⚪");

  useEffect(() => {
    socket.on('move', move => {
      console.log(move);
      setOppMove(move);
    });

  }, []);

  useEffect(() => {
    socket.on('player', msg => {
      setColor(msg.color);
      const players = msg.players; // number of players

      if(players === 2){
        setStartGame(true);
        socket.emit('play', msg.roomId);
        setGameStatus('Game in Progress');
      }
      else {
        setGameStatus('Waiting for Second Player');
      }
    });
  });


  return (
    <div>
      <Game makeMove={(i) => makeMove(i)} receiveMove={oppMove} startGame={startGame} color={color} gameStatus={gameStatus}/>
    </div>
  );
}