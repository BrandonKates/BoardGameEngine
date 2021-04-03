import React from "react";
import "./Square.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircle } from "@fortawesome/free-solid-svg-icons";

function unicodeToColor(value: any) {
  switch (value) {
    case "⚪":
      return "white";
    case "⚫":
      return "black";
    default:
      return false;
  }
}

export default function Square(props: any) {
  let displayColor = unicodeToColor(
    props.mouseOver ? props.myColor : props.value
  );
  let opacity = props.mouseOver ? 0.5 : 1;

  return (
    <button
      className="square"
      onClick={props.onClick}
      onMouseEnter={props.onMouseEnter}
      onMouseLeave={props.onMouseLeave}
    >
      {displayColor ? (
        <FontAwesomeIcon
          icon={faCircle}
          color={displayColor}
          opacity={opacity}
        />
      ) : (
        ""
      )}
    </button>
  );
}
