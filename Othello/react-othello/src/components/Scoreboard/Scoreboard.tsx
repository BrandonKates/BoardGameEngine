import React from "react";
import './Scoreboard.scss';

export default function Scoreboard(props: any) {
  return (
  <div className="scoreboard">
    <div className="score-header"> Score </div>
    <div className="score-color-row">
        <div className="score-color">{"⚪"}</div>
        <div className="score-color">{"⚫"}</div>
    </div>
    <div className="score-row">
        <div className="score">{props.score["⚪"]}</div>
        <div className="score">{props.score["⚫"]}</div>
    </div>
  </div>
);
  }