import React from 'react'

const SearchBanner = ({ query_name }) => {
    return (
        <div>
            <div className="search_banner">
                <div className='form_wrap'>
                    <div className="column col-6">
                        <h1 className="search_banner_heading">Search Results</h1>
                    </div>
                    <div className="column col-6 search_banner_text_box">
                        <h1 className='search_banner_text'>{ query_name }</h1>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SearchBanner
