import React from 'react'

const InputContainer = ({ type, title, data, out, setOut, checkedState, setCheckedState, styleOuter, styleInner }) => {

    const handleOnChange = (event) => {
        if (type === "checkbox") {
            const { checked, value } = event.currentTarget;

            setOut(
                prev => checked
                    ? [...prev, value]
                    : prev.filter(val => val !== value)
            );
        }
        else if (type === 'radio') {
            setCheckedState(event.target.value)
            setOut(event.target.value)
        }
    }

    return (
        <div className='item_box SourcesFixedBox' style={styleOuter}>
            <h3 className='SourcesTitle'>{title}</h3>
            <div className='SourcesContentBox' style={styleInner}>
                {data.map((obj, index) => {
                    return (
                        <div className='checkbox_div'>
                            <input
                                key={`custom-${type}-${index}`}
                                type={`${type}`}
                                id={`custom-${type}-${index}`}
                                name={obj}
                                value={obj}
                                onChange={handleOnChange}
                                checked={type === "radio" ? checkedState === `${obj}` : out.indexOf(obj) > -1}
                            />
                            <label className='checkbox_text' htmlFor={`custom-${type}-${index}`}>{obj}</label>
                        </div>)
                })}
            </div>
        </div>
    )
}

export default InputContainer
