import React, { useState } from 'react'


const Dropdown = ({ selected, setSelected, isActive, setIsActive, options, style }) => {

    function close() {
        setIsActive(false);
    }

    return (
        <div className='dropdown_wrapper' tabIndex={0} onBlur={close} style={style}>
            <div className='dropdown_button' onClick={(event) => setIsActive(!isActive)}>
                {selected}
                <span className="fa fa-caret-down"></span>
            </div>

            {isActive && (<div className='dropdown_content' >
                {options.map(option => (
                    <div className='dropdown_item' onClick={(event) => { 
                        setSelected(option); 
                        setIsActive(false); 
                        }}>
                        {option}
                    </div>
                ))}
            </div>)}

        </div>
    )
}

export default Dropdown
