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

let interval;

io.on("connection", (socket) => {
  console.log("New client connected");
  if (interval) {
    clearInterval(interval);
  }
  interval = setInterval(() => getApiAndEmit(socket), 1000);
  socket.on("disconnect", () => {
    console.log("Client disconnected");
    clearInterval(interval);
  });
});

const getApiAndEmit = socket => {
  const response = new Date();
  // Emitting a new message. Will be consumed by the client
  socket.emit("FromAPI", response);
};

server.listen(port, () => console.log(`Listening on port ${port}`));


let players = [];
let current_turn = 0;
let timeOut;
let _turn = 0;
const MAX_WAITING = 5000;

function next_turn(){
    _turn = current_turn++ % players.length;
    players[_turn].emit('your_turn');
    console.log("next turn triggered " , _turn);
    triggerTimeout();
}

function triggerTimeout(){
   timeOut = setTimeout(()=>{
     next_turn();
   },MAX_WAITING);
}

function resetTimeOut(){
    if(typeof timeOut === 'object'){
      console.log("timeout reset");
      clearTimeout(timeOut);
    }
}

io.on('connection', function(socket){
  console.log('A player connected');

  players.push(socket);
  socket.on('pass_turn',function(){
     if(players[_turn] == socket){
        resetTimeOut();
        next_turn();
     }
  });

    socket.on('disconnect', function(){
        console.log('A player disconnected');
        players.splice(players.indexOf(socket),1);
        _turn--;
        console.log("A number of players now ",players.length);
    });
});