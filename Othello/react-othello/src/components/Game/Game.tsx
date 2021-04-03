import React from "react";
import Board from "../Board/Board";
import Scoreboard from "../Scoreboard/Scoreboard";
import "./Game.scss";
import * as _ from "underscore";

interface Props {
  makeMove(move: Move): void;
  startGame: boolean;
  color: string;
  gameStatus: string;
  roomId: number;
  socket: any;
}

interface State {
  history: Array<any>;
  stepNumber: number;
  xIsNext: boolean;
  legalMoves: object;
  passTurn: boolean;
  color: string;
}

interface Move {
  i: number;
  color: string;
  flips: Array<number>;
}

class Game extends React.Component<Props, State> {
  constructor(props: any) {
    super(props);
    this.state = {
      history: [
        {
          squares: this.getEmptyBoard(),
        },
      ],
      stepNumber: 0,
      xIsNext: true,
      legalMoves: {},
      passTurn: false,
      color: props.color,
    };
    this.makeMove = this.makeMove.bind(this);
    this.receiveMove = this.receiveMove.bind(this);
  }

  componentDidMount() {
    this.props.socket.on("move", (msg: any) => {
      if (msg.roomId === this.props.roomId) {
        this.receiveMove(msg.move);
      }
    });
  }
  componentWillUnmount() {
    this.props.socket.off("move");
  }

  makeMove(move: Move) {
    return this.props.makeMove(move);
  }

  receiveMove(move: Move) {
    const passTurn = move.i === -1;
    // Do not move if spot is invalid

    if (passTurn || (isSpotInBoard(move.i) && this.isSpotEmpty(move.i))) {
      console.log("Opponent made move: ", move);
      return this.move(move);
    }
  }

  getBoard() {
    return this.state.history[this.state.stepNumber].squares;
  }

  getCurrentPlayer() {
    return this.state.xIsNext ? "⚪" : "⚫";
  }

  isSpotEmpty(i: number) {
    return this.getBoard()[i] === null;
  }

  isGameOver() {
    const current = this.getBoard();
    const currColor = this.getCurrentPlayer();
    const nextColor = this.state.xIsNext ? "⚫" : "⚪";
    var legalMoves = Object.keys(getLegalMoves(currColor, current));
    var nextLegalMoves = Object.keys(getLegalMoves(nextColor, current));

    // If both players can only pass, the game is over!
    return (
      legalMoves.length === 1 &&
      legalMoves[0] === "-1" &&
      nextLegalMoves.length === 1 &&
      nextLegalMoves[0] === "-1"
    );
  }

  getEmptyBoard() {
    var board = Array(64).fill(null);
    board[3 * 8 + 3] = board[4 * 8 + 4] = "⚪";
    board[3 * 8 + 4] = board[4 * 8 + 3] = "⚫";
    return board;
  }

  move(move: Move) {
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    var squares = this.getBoard();
    if (move.i !== -1) {
      _.forEach(move.flips, (flip) => flipSquare(flip, squares));
      squares[move.i] = move.color;
    }

    this.setState({
      history: history.concat([
        {
          squares: squares,
        },
      ]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
    });

    return squares;
  }

  randomTurn() {
    const currColor = this.getCurrentPlayer();
    const squares = this.getBoard().slice();
    const legalMoves = Object.keys(getLegalMoves(currColor, squares));
    const randMove = legalMoves[~~(Math.random() * legalMoves.length)];
    this.turn(parseInt(randMove));
  }

  turn(i: number) {
    const currColor = this.getCurrentPlayer();
    if (
      !this.props.startGame ||
      this.isGameOver() ||
      this.state.color !== currColor
    ) {
      return;
    }
    const squares = this.getBoard().slice();
    const legalMoves = getLegalMoves(currColor, squares);
    if (squares[i] || !legalMoves.hasOwnProperty(i)) {
      return;
    }

    // Create move object
    var move = {
      i: i,
      color: currColor,
      flips: legalMoves[i],
    };

    // Perform the move on the current board
    this.move(move);

    // Emit move to server
    this.makeMove(move);
  }

  handleClick(i: number) {
    this.turn(i);
  }

  jumpTo(step: number) {
    this.setState({
      stepNumber: step,
      xIsNext: step % 2 === 0,
    });
  }

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];

    let status;
    if (this.isGameOver()) {
      const winner = calculateWinner(current.squares);
      status = "Winner: " + winner;
    } else {
      status = "Next player: " + this.getCurrentPlayer();
    }
    const score = getScore(current.squares);
    const legalMoves = getLegalMoves(this.getCurrentPlayer(), current.squares);

    return (
      <div>
        <div className="game">
          <Scoreboard className="scoreboard" score={score} />
          <div className="game-board">
            <div className="game-board-header">{this.props.gameStatus}</div>
            <Board
              squares={current.squares}
              onClick={(i: any) => this.handleClick(i)}
              myColor={this.state.color}
              currentColor={this.getCurrentPlayer()}
              legalMoves={legalMoves}
            />
          </div>
          <div className="game-info">
            <div> My Color: {this.state.color} </div>
            <div>{status}</div>
            <div>
              {this.props.startGame && (
                <button onClick={() => this.randomTurn()}>
                  Random Move (or Pass){" "}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default Game;

function getScore(squares: Array<string>) {
  var score: Record<string, number> = {
    "⚪": 0,
    "⚫": 0,
  };
  _.forEach(squares, (sq) => {
    if (score.hasOwnProperty(sq)) {
      score[sq]++;
    }
  });
  return score;
}

function calculateWinner(squares: Array<string>) {
  const score = getScore(squares);
  if (score["⚪"] > score["⚫"]) {
    return "⚪";
  } else if (score["⚫"] > score["⚪"]) {
    return "⚫";
  } else {
    return "tie";
  }
}

function isSpotInBoard(spot: number): boolean {
  return 0 <= spot && spot <= 63;
}

function is2DSpotInBoard(row: number, column: number): boolean {
  return 0 <= row && row <= 7 && 0 <= column && column <= 7;
}

function calculateMove(spot: number, move: Array<number>): number {
  var x = ~~(spot / 8);
  var y = spot % 8;
  x += move[0];
  y += move[1];
  return is2DSpotInBoard(x, y) ? x * 8 + y : -1;
}

function getMoves(): Array<Array<number>> {
  // UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT
  //return [8, -8, 1, -1, 9, 7, -7, -9];
  return [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],
    [1, -1],
    [1, 1],
    [-1, 1],
    [-1, -1],
  ];
}

function getPositionsOfKind(kind: string | null, squares: Array<string>) {
  var positions: Array<number> = [];
  _.forEach(squares, (square, idx) => {
    if (square === kind) {
      positions.push(idx);
    }
  });
  return positions;
}

function getEmptyPositions(squares: Array<string>) {
  return getPositionsOfKind(null, squares);
}

function flipSquare(spot: number, squares: Array<string>) {
  const square = squares[spot];
  if (square === "⚪") {
    squares[spot] = "⚫";
  }
  if (square === "⚫") {
    squares[spot] = "⚪";
  }
}

function getFlipsInDirection(
  spot: number,
  move: Array<number>,
  currColor: string,
  squares: Array<string>
): Array<number> {
  if (!isSpotInBoard(spot)) {
    return [];
  }
  spot = calculateMove(spot, move);
  let flips = [];

  while (isSpotInBoard(spot)) {
    if (squares[spot] === null) {
      return [];
    }
    // if same color, return flips
    else if (squares[spot] === currColor) {
      return flips;
    }
    // if enemy, add a flip
    else {
      flips.push(spot);
    }
    spot = calculateMove(spot, move);
  }
  return [];
}

function getFlips(
  spot: number,
  currColor: string,
  squares: Array<string>
): Array<number> {
  if (squares[spot] != null) {
    return [];
  }
  return _.map(getMoves(), (move) =>
    getFlipsInDirection(spot, move, currColor, squares)
  ).flat();
}

function getLegalMoves(currColor: string, squares: Array<string>) {
  var spots: { [key: number]: Array<number> } = {};
  _.forEach(getEmptyPositions(squares), (pos) => {
    var flips = getFlips(pos, currColor, squares);
    if (flips.length > 0) {
      spots[pos] = flips;
    }
  });
  // If no spots are legal, add passTurn as an option
  if (spots && Object.keys(spots).length === 0) {
    spots[-1] = [];
  }
  return spots;
}
