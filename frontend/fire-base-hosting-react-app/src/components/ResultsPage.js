import React, { useEffect, useState } from 'react'

const ResultsPage = ({ results }) => {

    return (
        <div>
            <ul role="list" className="container list">

                {results.map(obj => {
                    return (<li key={obj.key} className="result_item item_box">
                        <h3 className="name">{obj.first_name} {obj.last_name}</h3>
                        <p className="qual">{obj.qual}</p>
                        <div className="actions">
                            <button className='result_button' onClick={(e) => {
                                e.preventDefault();
                                window.location.href = `//${obj.link}`;
                            }}>View Profile</button>
                        </div>
                    </li>)
                })}

            </ul>

        </div>
    )
}

export default ResultsPage
