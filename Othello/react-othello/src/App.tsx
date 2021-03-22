import React from 'react';
import './App.scss';

import ClientComponent from './components/ClientComponent/ClientComponent';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* SOCKET IO CLIENT*/}
        <ClientComponent />
      </header>
    </div>
  );
}

export default App;
