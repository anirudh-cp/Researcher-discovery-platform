import React from 'react'

const ResultsList = ({ results }) => {
    return (
        <div>
            <table style={{ width: "100%", marginBottom: "20px"}}>
                <thead className="table_row" style={{paddingTop: "0px"}}>
                    <th className='table_data table_head' style={{ width: "40%", paddingLeft:"10px", textAlign:"left" }}>Name</th>
                    <th className='table_data table_head' style={{ width: "20%", textAlign:"left" }}>ORC-ID</th>
                    <th className='table_data table_head' style={{ width: "15%" }}>Citations</th>
                    <th className='table_data table_head' style={{ width: "15%" }}>H-Index</th>
                    <th className='table_data table_head' style={{ width: "12%"}}>Profile Link</th>
                </thead>
                <tbody>
                    {
                        results.map(obj => {
                            return (<tr key={obj._id} className="table_row">
                                <th className='table_data table_name' style={{ width: "40%" }}>{obj.honorifics} {obj.name}</th>
                                <th className='table_data' style={{ width: "20%", textAlign:"left" }}>{obj.orcid !== '-1' ? obj.orcid : <></>}</th>
                                <th className='table_data' style={{ width: "15%" }}>{obj.cite !== '-1' ? obj.cite : <></>}</th>
                                <th className='table_data' style={{ width: "15%" }}>{obj.hindex !== '-1' ? obj.hindex : <></>}</th>
                                <th className='table_data' style={{ width: "12%" }}>
                                    <a href={obj.link}>
                                        <button className='table_result_button table_center' style={{paddingBottom: "5px"}}>
                                        View Profile</button>
                                    </a>
                                </th>
                            </tr>)
                        })
                    }
                </tbody>
            </table>
        </div>
    )
}

export default ResultsList
