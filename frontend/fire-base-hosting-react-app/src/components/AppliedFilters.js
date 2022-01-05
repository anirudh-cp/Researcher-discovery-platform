import React, { useEffect, useState } from 'react'


const AppliedFilters = ({ title, load, data, setData, APIData, styleOuter, styleInner }) => {
    const [localData, setLocalData] = useState([])

    useEffect(() => {
        setLocalData(data);
    }, [load])

    const handleOnChange = (event) => {
        const { checked, value } = event.currentTarget;
        setLocalData(
            prev => checked
                ? [...prev, value]
                : prev.filter(val => val !== value)
        );
        setData(
            prev => checked
                ? [...prev, value]
                : prev.filter(val => val !== value)
        );

    }

    return (
        <div>
            {localData.length > 0 ? 
            <div className='item_box SourcesFixedBox' style={styleOuter}>
                <h3 className='SourcesTitle'>{title}</h3>
                <div className='SourcesContentBox' style={styleInner}>
                    {localData.map((obj, index) => {
                        return (
                            <div className='checkbox_div'>
                                <input
                                    key={`custom-checkbox-${index}`}
                                    type={"checkbox"}
                                    id={`custom-checkbox-${index}`}
                                    name={obj}
                                    value={obj}
                                    defaultChecked={true}
                                    onChange={handleOnChange}
                                />
                                <label className='checkbox_text' htmlFor={`custom-checkbox-${index}`}>{obj}</label>
                            </div>)
                    })}
                </div>
            </div> 
            :
            <></>
            }
        </div>
    )
}

export default AppliedFilters
