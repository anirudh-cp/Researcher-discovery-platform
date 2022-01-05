import React from 'react'

const HomePageContent = () => {
    return (
        <div>
            <div className='main_container' style={{ marginTop: "70px" }}>
                <div className='center'>
                    <div>
                        <h3 className='home_text_heading'>Researcher Discovery Platform</h3>
                        <div className='center'>
                            <div className='feature_box'>
                                <span className="fa fa-search feature_icon" style={{ fontSize: "170px" }}></span>
                                <p className='feature_text'><span style={{color: "#005c97"}}>Search</span> through Thousands<br></br> of Research Professionals.</p>
                            </div>
                            <div className='feature_box'>
                                <span className="fa fa-filter feature_icon" style={{ fontSize: "170px" }}></span>
                                <p className='feature_text'><span style={{color: "#005c97"}}>Filter</span> through Dozens<br></br> of Universities<br></br>and Colleges.</p>
                            </div>
                            <div className='feature_box'>
                                <span className="fa fa-connectdevelop feature_icon" style={{ fontSize: "170px" }}></span>
                                <p className='feature_text'><span style={{color: "#005c97"}}>Connect</span> with <br></br>the One<br></br> Professional Best Suited for You.</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default HomePageContent
