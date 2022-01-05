import React, { useState, useEffect } from 'react'
import InputContainer from './InputContainer'
import OptionData from '../assets/options.json'
import AppliedFilters from './AppliedFilters'


const Filters = ({ setSort, filters, setFilters, setOrder, APIData, load }) => {
    const [checkedStateSort, setCheckedStateSort] = useState("Sort by H-Index");
    const [checkedStateOrder, setCheckedStateOrder] = useState("Descending");
    const [showClear, setShowClear] = useState(false);

    const handleClick = (event) => {
        event.preventDefault();
        APIData();
    }

    const handleClear = async (event) => {
        event.preventDefault();
        await setFilters([]);
        await APIData();
    }

    useEffect(() => {
        if (filters.length === 0) {
            setShowClear(false);
        }
        else {
            setShowClear(true);
        }

    }, [load])

    return (
        <div>
            <form>
                <AppliedFilters title={"Applied Filters"} load={load}
                    setData={setFilters} data={filters} APIData={APIData}
                    styleOuter={{ height: '270px' }} styleInner={{ height: '185px' }} />

                <InputContainer type={"checkbox"} title={"Sources"} data={OptionData.sources}
                    setOut={setFilters} out={filters}
                    styleOuter={{ height: '325px' }} styleInner={{ height: '250px' }} />

                <InputContainer type={"radio"} title={"Sort By"} data={OptionData.sorts}
                    setOut={setSort} checkedState={checkedStateSort} setCheckedState={setCheckedStateSort} />

                <InputContainer type={"radio"} title={"Order By"} data={OptionData.order}
                    setOut={setOrder} checkedState={checkedStateOrder} setCheckedState={setCheckedStateOrder} />

                <div className='page_bar'>
                    <button className='result_button' style={{ fontSize: '14px' }} onClick={handleClick}>Filter Results</button>
                    {(showClear) ?
                        <button className='result_button' style={{ fontSize: '14px' }} onClick={handleClear}>Clear Filters</button>
                        : <></>
                    }
                </div>
            </form>
        </div>
    )

}
export default Filters
