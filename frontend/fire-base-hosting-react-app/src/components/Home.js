import React, {useEffect, useState} from 'react'

import HomeBanner from './HomeBanner'
import HomeInput from './HomeInput'


const Home = () => {
    return (
        <div>
            <HomeBanner />
            <div className='main_container'>
                <HomeInput />
            </div>
            
        </div>
    )
}

export default Home
