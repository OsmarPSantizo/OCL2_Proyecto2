import React from "react";
import './App.css';
import {useState,useEffect} from 'react';
import { BrowserRouter, Route,Routes,Switch} from "react-router-dom";
import {Deploy} from './Component/Deploy/Deploy'
import Navbar from './Component/Navbar';
import Calc1 from "./Pages/Calc1";
import Calc2 from "./Pages/Calc2";
import Calc3 from "./Pages/Calc3";
import Calc4 from "./Pages/Calc4";
import Calc5 from "./Pages/Calc5";
import Calc6 from "./Pages/Calc6";

function App() {
  // const [state,setState]= useState({})

  // useEffect(()=> {
  //   fetch("/api").then(response=>{
  //     if(response.status == 200){
  //       return response.json()
  //     }
  //   }).then(data => setState(data))
  //   .then(error => console.log(error))
  // },[])
  return (
    <>
      <BrowserRouter>
        <Navbar/>
        <Routes>
        
          <Route exact path='/calc1' element={<Calc1/>}></Route>
          <Route exact path='/calc2' element={<Calc2/>}></Route>
          <Route exact path='/calc3' element={<Calc3/>}></Route>
          <Route exact path='/calc4' element={<Calc4/>}></Route>
          <Route exact path='/calc5' element={<Calc5/>}></Route>
          <Route exact path='/calc6' element={<Calc6/>}></Route>
        </Routes>
      </BrowserRouter>
      </>
  );
}

export default App;
