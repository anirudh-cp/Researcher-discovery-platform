import React from 'react'
import HomeInput from './HomeInput'


const HomeBanner = () => {
    return (
        <div>
            <div className='home_banner'>
                <div className='center-screen'>
                    <div className='home_call_to_action_box item_box'>
                        <h1 className='home_main_heading' style={{ fontSize: "80px" }}>Discover. Conect. Innovate.</h1>
                        <h2 className='home_main_heading' style={{ fontSize: "30px", marginBottom: "40px" }}>Find the Top Researchers across India.</h2>
                        <HomeInput />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HomeBanner
