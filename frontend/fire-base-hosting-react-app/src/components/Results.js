import React, { useEffect, useState, useContext } from 'react'
import { QueryContext } from '../Contexts/QueryContext';
import { useNavigate } from 'react-router';

import APIService from '../API/APIService';

import SearchBanner from './SearchBanner';
import Filters from './Filters';
import ResultsPage from './ResultsPage';
import ResultsLoading from './ResultsLoading';


const Results = () => {
    const [results, setResults] = useState([])
    const [page, setPage] = useState(0)
    const [filters, setFilters] = useState("None")

    const API = new APIService();
    const navigate = useNavigate();

    const [load, setLoad] = useState(true)

    const { query_name } = useContext(QueryContext)

    useEffect(() => {
        // if (query_name === "")
        //    navigate('/')

        setLoad(true)
        API.GetResults({ query_name, page, filters }).then(response => setResults(response.records)).catch(error => console.log(error));
        // API.GetResults({ query_name, page, filters }).then(response => console.log(response)).catch(error => console.log(error));
        setLoad(false)        
    }, [])

    return (
        <div>
            <SearchBanner query_name={query_name} />
            <div className='main_container form_wrap'>
                <div className='form_wrap grid'>
                    <div>
                        <Filters />
                    </div>
                    <div>
                        {load==true ? <ResultsLoading /> : <ResultsPage results={results} />}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Results
