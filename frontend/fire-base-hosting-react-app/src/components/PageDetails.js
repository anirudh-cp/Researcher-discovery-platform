import React, { useState, useEffect } from 'react'
import Dropdown from './Dropdown'

const PageDetails = ({ page, load, setPage, pageTotal, setPageTotal, pageView, setPageView }) => {
    const [isActivePage, setIsActivePage] = useState(false)
    const [isActiveView, setIsActiveView] = useState(false)

    useEffect(() => {
        setPage(0);
    }, [pageTotal])

    return (
        <div className='page_bar'>
            {load ? <p className='page_detail_text'>Loading Page.</p> : <p className='page_detail_text'>On page : {page}</p>}
            <div className='page_bar'>
                <p className='page_detail_text'>View: </p>
                <Dropdown selected={pageView} setSelected={setPageView}
                    isActive={isActiveView} setIsActive={setIsActiveView}
                    options={["Tile", "List"]} style={{ width: "80px" }} />

                <p className='page_detail_text'>Per Page: </p>
                <Dropdown selected={pageTotal} setSelected={setPageTotal}
                    isActive={isActivePage} setIsActive={setIsActivePage}
                    options={[5, 10, 15]} style={{ width: "60px" }} />
            </div>
        </div>
    )
}

export default PageDetails
