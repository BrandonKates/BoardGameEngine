import React, { useState } from 'react';
import './Square.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle } from '@fortawesome/free-solid-svg-icons';

function unicodeToColor(value: any){
	switch(value) {
		case "⚪":
			return 'white';
		case "⚫":
			return 'black';
		default:
			return false;
	}
}

export default function Square(props: any) {
	let [mouseOver, setMouseOver] = useState(false);

	const showPiece = (event: any) => {
		return event.target.value === '' && props.myColor === props.currentColor;
	};

	let displayColor = unicodeToColor(mouseOver ? props.myColor : props.value);
	let opacity = mouseOver ? 0.5 : 1;

    return (
        <button className='square' 
        		onClick={props.onClick}
        		onMouseEnter={(event: any) => setMouseOver(showPiece(event))} 
        		onMouseLeave={(event: any) => setMouseOver(false)}
        		value={props.value}>
            {displayColor ?
            	<FontAwesomeIcon 
	            	icon={faCircle} 
	            	color={displayColor} 
	            	opacity={opacity}/>
            	: ""}
        </button>
    )   
}
