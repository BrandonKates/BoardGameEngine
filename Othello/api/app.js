const express = require('express');
const app = express();

const server = require('http').Server(app);
const io = require('socket.io')(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

const port = process.env.PORT || 9000;
const index = require("./routes/index");

app.use(index);


let players;
var joined = true;

var games = Array(100);
for (let i = 0; i < 100; i++){
  games[i] = {players: 0, pid: [0, 0]}
}


io.on("connection", (socket) => {
  console.log("New client connected");
  var color;
  var playerId = Math.floor((Math.random() * 100) + 1);

  console.log(playerId + ' connected!');

  socket.on('joined', function(roomId) {
    if(games[roomId].players < 2){
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
      for (let i = 0; i < 100; i++) {
          if (games[i].pid[0] == playerId || games[i].pid[1] == playerId)
              games[i].players--;
      }
      console.log(playerId + ' disconnected');
  });
});

server.listen(port, () => console.log(`Listening on port ${port}`));
