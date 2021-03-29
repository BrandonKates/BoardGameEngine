import React from 'react';
import Square from '../Square/Square';
import './Board.scss';
import * as _ from 'underscore'


interface Props {
    squares: Array<Number>,
    onClick: any
    myColor: string
    currentColor: string
}

class Board extends React.Component<Props> {
    renderSquare(i: number) {
        return (
            <Square
                value={this.props.squares[i]}
                onClick={() => this.props.onClick(i)}
                myColor={this.props.myColor}
                currentColor={this.props.currentColor}
                key={i}
            />
        );
    }

    render() {
        return (
            <div className="board">
                {_.times(8, (i: number) => (
                    <div className="board-row" key={i}>
                    {_.times(8, (j: number) => (
                        this.renderSquare(i * 8 + j)
                    ))}
                    </div>
                ))}
            </div>
);
    }
}

export default Board;