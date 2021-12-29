import React, { useEffect, useState, useContext } from 'react'
import { QueryContext } from '../Contexts/QueryContext';
import { useNavigate } from 'react-router';

import APIService from '../API/APIService';
import Temp from './Temp';


const Results = () => {
    const [results, setResults] = useState([])
    const [page, setPage] = useState(0)
    const [filters, setFilters] = useState("None")

    const navigate = useNavigate();

    const [load, setLoad] = useState(true)

    const { query_name } = useContext(QueryContext)
    const API = new APIService()
    
    useEffect(() => {
        if (query_name === "")
            navigate('/')

        setLoad(true)
        API.GetResults({ query_name, page, filters }).then(response => setResults(response)).catch(error => console.log(error));
        setLoad(false)
    }, [])

    return (
        <div>
            <p>In results page.</p>
            {load ? <h1>Loading</h1>: <Temp results={results} />}
        </div>
    )
}

export default Results
