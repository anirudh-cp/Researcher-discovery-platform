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
    const [filters, setFilters] = useState([])
    const [sort, setSort] = useState("Sort by H-Index")
    const [order, setOrder] = useState("Descending")

    const API = new APIService();
    const navigate = useNavigate();

    const [load, setLoad] = useState(true)

    const { query_name } = useContext(QueryContext)

    const APIData = async () => {
        setLoad(true);
        const response = await API.GetResults({ query_name, page, filters, sort, order }).then(response => {
            setResults(response.records);
            setPage(response.page);
        }).catch(error => console.log(error));
        setLoad(false);
    }

    const APIData_filter = async (event) => {
        event.preventDefault()
        const response = await API.GetResults({ query_name, page, filters, sort, order }).then(response => {
            setResults(response.records);
            setPage(response.page);
        }).catch(error => console.log(error));
        setLoad(false);
    }

    useEffect(() => {
        if (query_name === "")
            navigate('/')
        
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
                        <Filters setSort={setSort} filters={filters} setFilters={setFilters} setOrder={setOrder}
                        APIData={APIData} load={load}/>
                    </div>
                    <div>
                        <PageDetails page={page} load={load}/>
                        {load ? <ResultsLoading /> : <ResultsPage results={results} />}
                        <MovePage page={page} setPage={setPage} load={load} results={results}/>
                    </div>
                </div>

            </div>

        </div>
    )
}

export default Results
