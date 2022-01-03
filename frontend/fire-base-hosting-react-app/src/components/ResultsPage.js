import React, { useEffect, useState } from 'react'

import NoResults from './NoResults'

const ResultsPage = ({ results }) => {

    return (
        <div>
            <ul role="list" className="container list">
                {(results.length === 0) ? <NoResults /> :
                    results.map(obj => {
                        return (<li key={obj._id} className="result_item item_box">
                            <h3 className="name">{obj.name}</h3>
                            {obj.orcid !== '-1' ? <p className='orcid'>Orcid: {obj.orcid}</p> : <></>}
                            {obj.cite !== '-1' ? <p className='details'>Citations: {obj.cite}</p> : <></>}
                            {obj.hindex !== '-1' ? <p className='details'>H-Index: {obj.hindex}</p> : <></>}
                            <p className="qual">{obj.qual}</p>
                            <div className="actions">
                                <a href={`//${obj.link}'`}> 
                                    <button className='result_button'>View Profile</button>
                                </a>
                            </div>
                        </li>)
                    })
                }
            </ul>

        </div>
    )
}

export default ResultsPage
