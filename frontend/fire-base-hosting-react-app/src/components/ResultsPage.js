import React, { useEffect, useState } from 'react'

import NoResults from './NoResults'
import ResultsTile from './ResultsTile'
import ResultsList from './ResultsList'

const ResultsPage = ({ results, pageView }) => {

    return (
        <div>
            <ul role="list" className="container list">
                {(results.length === 0) ? <NoResults /> : 
                (pageView === "Tile") ? <ResultsTile results={results} /> : <ResultsList results={results} />}
            </ul>

        </div>
    )
}

export default ResultsPage
