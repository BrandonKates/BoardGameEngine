import React from 'react';
import Board from '../Board/Board';
import './Game.scss';
import * as _ from 'underscore'


interface Props {
    makeMove(move: Move): void
    receiveMove: Move
    startGame: boolean
    color: string
    gameStatus: string
}

interface State {
    history: Array<any>
    stepNumber: number
    xIsNext: boolean
    legalMoves: object
    passTurn: boolean
    color: string
}

interface Move {
    i: number
    color: string
    flips: Array<number>
}

class Game extends React.Component<Props, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            history: [
                {
                    squares: this.getEmptyBoard()
                }
            ],
            stepNumber: 0,
            xIsNext: true,
            legalMoves: {},
            passTurn: false,
            color: props.color
        };
        this.makeMove = this.makeMove.bind(this);
        this.receiveMove = this.receiveMove.bind(this);
    }

    makeMove(move: Move){
        return this.props.makeMove(move);
    }

    receiveMove(){
        const move = this.props.receiveMove;
        const passTurn = move.i === -1;
        // Do not propagate move if it is not in board, or the spot already has a piece on it
        if(!isSpotInBoard(move.i) || !passTurn || !this.isSpotEmpty(move.i)){
            return
        }
        console.log("Opponent made move: ", move);
        return this.move(move);
    }

    getBoard(){
        return this.state.history[this.state.stepNumber].squares;
    }

    getCurrentPlayer(){
        return this.state.xIsNext ? "⚪" : "⚫";
    }

    isSpotEmpty(i: number){
        return this.getBoard()[i] === null;
    }

    isGameOver() {
        const current = this.getBoard();
        const currColor = this.getCurrentPlayer();
        const nextColor = this.state.xIsNext ? "⚫" : "⚪";
        var legalMoves = Object.keys(getLegalMoves(currColor, current));
        var nextLegalMoves = Object.keys(getLegalMoves(nextColor, current));
        return legalMoves.length === 0 && nextLegalMoves.length === 0;

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
        _.forEach(move.flips, flip => flipSquare(flip, squares));
        squares[move.i] = move.color;
        
        this.setState({
            history: history.concat([
                {
                    squares: squares
                }
            ]),
            stepNumber: history.length,
            xIsNext: !this.state.xIsNext
        });

        return squares;
    }

    handleClick(i: number) {
        var squares = this.getBoard().slice();
        
        const currColor = this.getCurrentPlayer();
        
        const legalMoves = getLegalMoves(currColor, squares);
        if (!this.props.startGame ||
            this.isGameOver() ||
            squares[i] ||
            !legalMoves.hasOwnProperty(i) ||
            this.state.color !== currColor) {
            return;
        }

        // Create move object 
        var move = {
            i: i,
            color: currColor,
            flips: legalMoves[i]
        };
        // Perform the move on the current board
        this.move(move);

        // Emit move to server
        this.makeMove(move);
    }

    jumpTo(step: number) {
        this.setState({
            stepNumber: step,
            xIsNext: (step % 2) === 0
        });
    }

    render() {
        const history = this.state.history;
        const current = history[this.state.stepNumber];

        /*const moves = history.map((step, move) => {
            const desc = move ?
                'Move #' + move :
                'Start';
            return (
                <li key={move}>
                    <button onClick={() => this.jumpTo(move)}>{desc}</button>
                </li>
            );
        });*/

        this.receiveMove();

        let status;
        if (this.isGameOver()) {
            const winner = calculateWinner(current.squares);
            status = "Winner: " + winner;
        } else {
            status = "Next player: " + (this.getCurrentPlayer());
        }

        return (
            <div>{this.props.gameStatus}
                <div className="game">
                    <div className="game-board">
                        <Board
                            squares={current.squares}
                            onClick={(i: any) => this.handleClick(i)}
                        />
                    </div>
                    <div className="game-info">
                        <div>{status}</div>
                        {/*<ol>{moves}</ol>*/}
                    </div>
                </div>
            </div>
        );
    }
}
export default Game;

function calculateWinner(squares: Array<String>) {
    var score = [0, 0];
    _.forEach(squares, sq => {
        if (sq === "⚪"){
            score[0] += 1
        }
        if (sq === "⚫"){
            score[1] += 1
        }
    });
    if(score[0] > score[1]){
        return "⚪";
    }
    else if (score[1] > score[0]){
        return "⚫";
    }
    else if (score[0] === score[1]){
        return 'tie';
    }
}

function isSpotInBoard(spot: number): boolean{
    return 0 <= spot && spot <= 63;
}

function getMoves(): Array<number> {
    // UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT
    return [8, -8, 1, -1, 9, 7, -7, -9]
    //return [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
}

function moveDirection(spot: number, move: number) {
    return spot + move;
}

function getPositionsOfKind(kind: string | null, squares: Array<string>) {
    var positions: Array<number> = []; 
    _.forEach(squares, (square, idx) => {
        if (square === kind){
            positions.push(idx);
        };
    });
    return positions;
}

function getEmptyPositions(squares: Array<string>) {
    return getPositionsOfKind(null, squares);
}

function flipSquare(spot: number, squares: Array<String>) {
    const square = squares[spot];
    if (square === "⚪") {
        squares[spot] = "⚫";
    }
    if (square === "⚫") {
        squares[spot] = "⚪";
    }
}

function getFlipsInDirection(spot: number, move: number, currColor: string, squares: Array<string>): Array<number> {
    if (!isSpotInBoard(spot)){
        return [];
    }
    spot = moveDirection(spot, move);
    var flips = [];
    var square;

    while(isSpotInBoard(spot)) {
        square = squares[spot];
        if (square === null){
            return [];
        }
        // enemy color
        if (square !== currColor){
            flips.push(spot);
        }
        else if (square === currColor) {
            return flips;
        }
        spot = moveDirection(spot, move);
    }
    return [];
}

function getFlips(spot: number, currColor: string, squares: Array<string>): Array<number> {
    if (squares[spot] != null){
        return [];
    }
    return _.map(getMoves(), move => (
        getFlipsInDirection(spot, move, currColor, squares)
    )).flat();
}

function getLegalMoves(currColor: string, squares: Array<string>) {
    var spots: { [key: number]: Array<number> }  = {};
    _.forEach(getEmptyPositions(squares), pos => {
        var flips = getFlips(pos, currColor, squares);
        if (flips.length > 0){
            spots[pos] = flips;
        }
    });
    return spots;
}
