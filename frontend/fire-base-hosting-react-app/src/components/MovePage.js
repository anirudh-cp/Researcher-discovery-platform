import React from 'react'

const MovePage = ({ page, setPage, load, results }) => {
    return (
        <div className='page_bar'>
            <button className='page_bar_button' onClick={() => setPage(page - 1)} disabled={!(page-1) || load}> <>&larr;</> </button>
            <button className='page_bar_button' onClick={() => setPage(page + 1)} disabled={(results.length<5) || load}><>&rarr;</> </button>
        </div>
    )
}

export default MovePage
