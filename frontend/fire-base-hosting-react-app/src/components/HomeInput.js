import React from 'react'


const HomeInput = () => {
    return (
        <div>
            <form className="item_box">
                <div className='form_wrap'>
                    <input type="text" id="query" placeholder="Enter a Domain" className="home_input flex-grow-1" />
                    <button name="search" type="submit" className="button">Search</button>
                </div>
            </form>
        </div>
    )
}

export default HomeInput
