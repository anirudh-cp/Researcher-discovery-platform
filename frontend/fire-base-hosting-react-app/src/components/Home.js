import React from 'react'

import HomeInput from './HomeInput'

const Home = () => {
    return (
        <div>
            <div className='home_banner'>
                <h1 className='home_banner_heading'>Welcome</h1>
            </div>
            <div className='main_container'>
                <HomeInput />
            </div>
        </div>
    )
}

export default Home
