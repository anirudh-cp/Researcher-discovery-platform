import React from 'react'
import { Routes , Route } from 'react-router-dom';
import { useState } from 'react';

import Home from './Home';
import Results from './Results';
import { QueryContext } from '../Contexts/QueryContext';

const MainContent = () => {
    const [query_name, setQuery] = useState("")

    return (
        <div>
            <QueryContext.Provider value={{query_name, setQuery}}>
            <Routes> {/* The Switch decides which component to show based on the current URL.*/}
                <Route exact path='/' element={<Home />}></Route>
                <Route exact path='/home' element={<Home />}></Route>
                <Route exact path='/results' element={<Results />}></Route>
            </Routes>
            </QueryContext.Provider >
        </div>
    )
}

export default MainContent
