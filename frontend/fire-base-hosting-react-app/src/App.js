import React, { useState, useEffect } from 'react';
import './App.css';

import Header from './components/Header';
import MainContent from './components/MainContent';

// TODO : Create API service module in /components
// TODO : Configure API service for HomeInput component

function App() {
  const [data, setData] = useState(0);

  /*
  useEffect(()=>{
    fetch('http://localhost:8000/results',{
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())
    .then(response => setData(response))
    .catch(error => console.log(error))

  },[]
  )*/

  return (
    <div className="App">
      <Header />
      <MainContent />
      {/*<p>Hello : {data.Hello}, ABC : {data.ABC}</p>*/}
    </div>
  );
}


export default App;