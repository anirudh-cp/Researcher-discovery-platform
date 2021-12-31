import React from 'react'

const PageDetails = ({page, load}) => {
    return (
        <div className='page_bar'>
            {load ? <p className='page_detail_text'>Loading Page.</p> : <p className='page_detail_text'>On page : { page }</p>}
            <p className='page_detail_text'>5 per Page.</p>
        </div>
    )
}

export default PageDetails
