const express = require('express');
const app = express();

const server = require('http').Server(app);
const io = require('socket.io')(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const port = process.env.PORT || 9000;
const index = require("./routes/index");

app.use(index);

var playerNum = 1;
let players;
var joined = true;
const numGames = 10;
var games = Array(numGames);
for (let i = 0; i < numGames; i++){
  games[i] = {players: 0, pid: [0, 0]}
}


io.on("connection", (socket) => {
  console.log("New client connected");
  var color;
  var playerId = playerNum;
  playerNum++;

  console.log(playerId + ' connected!');

  socket.on('joined', function(roomId) {
    console.log(roomId);
    if(roomId < games.length && games[roomId].players < 2){
      games[roomId].players++;
      games[roomId].pid[games[roomId].players - 1] = playerId;
    }
    else{
      socket.emit('full', roomId);
      return;
    }

    console.log(games[roomId]);
    players = games[roomId].players;

    color = players % 2 == 0 ? "⚪" : "⚫";

    socket.emit('player', { playerId, players, color, roomId });
  });

  socket.on('move', msg => {
    socket.broadcast.emit('move', msg);
    console.log(msg);
  });

  socket.on('play', msg => {
    socket.broadcast.emit('play', msg);
    console.log("ready " + msg);
  });

  socket.on("disconnect", () => {
      for (let i = 0; i < numGames; i++) {
        // on disconnect, reset the room
          if (games[i].pid[0] == playerId || games[i].pid[1] == playerId)
            // on disconnect, reset the room
            games[i] = {players: 0, pid: [0, 0]}
      }
      console.log(playerId + ' disconnected');
  });
});

server.listen(port, () => console.log(`Listening on port ${port}`));
