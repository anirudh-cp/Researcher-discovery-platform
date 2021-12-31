import React, { useEffect, useState, useContext } from 'react'
import { QueryContext } from '../Contexts/QueryContext';
import { useNavigate } from 'react-router';

import APIService from '../API/APIService';

import SearchBanner from './SearchBanner';
import Filters from './Filters';
import ResultsPage from './ResultsPage';
import ResultsLoading from './ResultsLoading';
import MovePage from './MovePage'
import PageDetails from './PageDetails'


const Results = () => {
    const [results, setResults] = useState([])
    const [page, setPage] = useState(-1)
    const [filters, setFilters] = useState("None")

    const API = new APIService();
    const navigate = useNavigate();

    const [load, setLoad] = useState(true)

    const { query_name } = useContext(QueryContext)

    const APIData = async () => {
        const response = await API.GetResults({ query_name, page, filters }).then(response => {
            setResults(response.records);
            setPage(response.page);
        }).catch(error => console.log(error));
        setLoad(false);
    }

    useEffect(() => {
        if (query_name === "")
            navigate('/')
        
        setLoad(true);
        // API.GetResults({ query_name, page, filters }).then(response => setResults(response.records)).catch(error => console.log(error));
        // API.GetResults({ query_name, page, filters }).then(response => console.log(response)).catch(error => console.log(error));
        APIData();

    }, [page])

    return (
        <div>
            <SearchBanner query_name={query_name} />
            <div className='main_container form_wrap'>
                <div className='form_wrap grid'>
                    <div>
                        <Filters />
                    </div>
                    <div>
                        <PageDetails page={page} load={load}/>
                        {load ? <ResultsLoading /> : <ResultsPage results={results} />}
                        <MovePage page={page} setPage={setPage} load={load}/>
                    </div>
                </div>

            </div>

        </div>
    )
}

export default Results
