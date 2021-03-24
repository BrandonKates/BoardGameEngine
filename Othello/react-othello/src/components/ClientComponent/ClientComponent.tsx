import React, { useEffect, useState } from "react";
import { useLocation } from 'react-router-dom';
import Game from '../Game/Game';

interface Move {
    i: number
    color: string
    flips: Array<number>
}

export default function ClientComponent(props: any) {
  const { state } : any = useLocation();
  const socket = props.socket;

  const [gameStatus, setGameStatus] = useState('');
  const [startGame, setStartGame] = useState(false);
  const [color, setColor] = useState("");

  const [full, setFull] = useState(false);

  const makeMove = (move: Move) => {
    console.log("Make Move: ", move.i, "\nColor: ", move.color, "\nFlips: ", move.flips);
    // Emit to server, which propagates to other client
    socket.emit('move', move);
    return
  }
  
  useEffect(() => {
    socket.on('full', function (roomId: number){
      if(state.roomId === roomId){
        setFull(true);
      }
    });
  });

  useEffect(() => {
    socket.on('play', function (roomId: number){
      if(state.roomId === roomId){
        setStartGame(true);
        setGameStatus('Game in Progress');
      }
    });
  });


  useEffect(() => {
    socket.on('player', (msg: any) => {
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


  if(full){
    return (<h2> Room is full, please refresh and try another room. </h2>);
  }

  if(color !== '' && gameStatus !== ''){
    return (
      <div>
        <Game makeMove={(i) => makeMove(i)} startGame={startGame} color={color} gameStatus={gameStatus} socket={socket}/>
      </div>
    );
  }
  return (<h2>Refresh Page</h2>);
}