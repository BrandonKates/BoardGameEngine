import React from 'react';
import './App.css';
import Chessboard from 'chessboardjsx';
import RandomVsRandomGame from './RandomVsRandom'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div style={boardsContainer}>
          <RandomVsRandomGame />
        </div>
      </header>
    </div>
  );
}

const boardsContainer = {
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
  flexWrap: "wrap",
  width: "100vw",
  marginTop: 30,
  marginBottom: 50
};

export default App;
