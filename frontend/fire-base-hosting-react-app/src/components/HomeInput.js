import React, { useContext } from 'react'
import { QueryContext } from '../Contexts/QueryContext';
import { useNavigate } from 'react-router';


const HomeInput = () => {
    const navigate = useNavigate();
    
    const { query_name, setQuery } = useContext(QueryContext);

    const handleSubmit = (event) => {
        event.preventDefault();
        navigate('/results');
    }

    return (
        <div>
            <form style={{marginBottom: "10px"}} onSubmit={handleSubmit}>
                <div className='form_wrap'>
                    <input type="text" id="query" placeholder="Enter a Domain" 
                    className="home_input flex-grow-1"
                    value={query_name}
                    onChange={(e)=>setQuery(e.target.value)}/>
                    <button name="search" type="submit" className="button">Search</button>
                </div>
            </form>
        </div>
    )
}

export default HomeInput
