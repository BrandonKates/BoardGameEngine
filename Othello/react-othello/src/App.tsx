import React from 'react';
import logo from './logo.svg';
import './App.scss';

import Game from './components/Game/Game';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Game/>
      </header>
    </div>
  );
}

export default App;
