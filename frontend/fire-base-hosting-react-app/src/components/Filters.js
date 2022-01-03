import React, { useState } from 'react'
import InputContainer from './InputContainer'
import OptionData from '../assets/options.json'
import AppliedFilters from './AppliedFilters'


const Filters = ({ setSort, filters, setFilters, setOrder, APIData, load}) => {
    const [checkedStateSort, setCheckedStateSort] = useState("Sort by H-Index");
    const [checkedStateOrder, setCheckedStateOrder] = useState("Descending");

    const handleClick = (event) => {
        event.preventDefault()
        APIData()
    }

    return (
        <div>
            <form>
                <AppliedFilters title={"Applied Filters"} load={load}
                setData={setFilters} data={filters} 
                styleOuter={{height: '270px'}} styleInner={{height: '185px'}} />
               
                <InputContainer type={"checkbox"} title={"Sources"} data={OptionData.sources} 
                setOut={setFilters} out={filters} 
                styleOuter={{height: '325px'}} styleInner={{height: '250px'} }/>
                
                <InputContainer type={"radio"} title={"Sort By"} data={OptionData.sorts} 
                setOut={setSort} checkedState={checkedStateSort} setCheckedState={setCheckedStateSort}/>

                <InputContainer type={"radio"} title={"Order By"} data={OptionData.order} 
                setOut={setOrder} checkedState={checkedStateOrder} setCheckedState={setCheckedStateOrder}/>
                
                <button className='result_button' style={{fontSize:'14px'}} onClick={handleClick}>Filter Results</button>
            </form>
        </div>
    )

}
export default Filters
