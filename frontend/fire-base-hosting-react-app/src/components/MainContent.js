import React from 'react'
import { Routes , Route } from 'react-router-dom';

import Home from './Home';
import Results from './Results';

const MainContent = () => {
    return (
        <div>
            <Routes> {/* The Switch decides which component to show based on the current URL.*/}
                <Route exact path='/' element={<Home/>}></Route>
                <Route exact path='/home' element={<Home/>}></Route>
                <Route exact path='/results' element={<Results/>}></Route>
            </Routes>
        </div>
    )
}

export default MainContent
