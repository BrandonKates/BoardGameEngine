import React, { useState } from "react";
import Square from "../Square/Square";
import "./Board.scss";
import * as _ from "underscore";

interface Props {
  squares: Array<string>;
  onClick: any;
  myColor: string;
  currentColor: string;
  legalMoves: { [key: number]: Array<number> };
}

export default function Board(props: Props) {
  const [state, setState] = useState<{ show: number[] }>({ show: [] });

  const isLegal = (i: number) => {
    return (
      props.myColor === props.currentColor && props.legalMoves.hasOwnProperty(i)
    );
  };

  const onMouseEnter = (i: number) => {
    if (isLegal(i)) {
      setState({ show: [...props.legalMoves[i], i] });
    }
  };

  const onClick = (i: number) => {
    if (isLegal(i)) {
      setState({ show: [] });
      props.onClick(i);
    }
  };

  const onMouseLeave = (i: number) => {
    if (isLegal(i)) {
      // reset state
      setState({ show: [] });
    }
  };

  const renderSquare = (i: number) => {
    return (
      <Square
        onClick={() => onClick(i)}
        value={props.squares[i]}
        myColor={props.myColor}
        mouseOver={state.show.includes(i)}
        onMouseEnter={() => onMouseEnter(i)}
        onMouseLeave={() => onMouseLeave(i)}
        key={i}
      />
    );
  };

  return (
    <div className="board">
      {_.times(8, (i: number) => (
        <div className="board-row" key={i}>
          {_.times(8, (j: number) => renderSquare(i * 8 + j))}
        </div>
      ))}
    </div>
  );
}

export { Board };
