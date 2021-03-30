import React from "react";
import './Scoreboard.scss';

export default function Scoreboard(props: any) {
  const whiteScore = props.score[0];
  const blackScore = props.score[1];

  return (
  <div className="scoreboard">
    <div className="score-header"> Score </div>
    <div className="score-color-row">
        <div className="score-color">{"⚪"}</div>
        <div className="score-color">{"⚫"}</div>
    </div>
    <div className="score-row">
        <div className="score">{whiteScore}</div>
        <div className="score">{blackScore}</div>
    </div>
  </div>
);
  }