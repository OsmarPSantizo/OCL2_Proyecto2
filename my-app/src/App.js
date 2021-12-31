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
import Calc7 from "./Pages/Calc7";
import Calc8 from "./Pages/Calc8";
import Calc9 from "./Pages/Calc9";
import Calc10 from "./Pages/Calc10";
import Calc11 from "./Pages/Calc11";
import Calc12 from "./Pages/Calc12";
import Calc13 from "./Pages/Calc13";
import Calc14 from "./Pages/Calc14";
import Calc15 from "./Pages/Calc15";
import Calc16 from "./Pages/Calc16";
import Calc17 from "./Pages/Calc17";
import Calc18 from "./Pages/Calc18";
import Calc19 from "./Pages/Calc19";
import Calc20 from "./Pages/Calc20";
import Calc21 from "./Pages/Calc21";
import Calc22 from "./Pages/Calc22";
import Calc23 from "./Pages/Calc23";
import Calc24 from "./Pages/Calc24";
import Calc25 from "./Pages/Calc25";

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
          <Route exact path='/calc7' element={<Calc7/>}></Route>
          <Route exact path='/calc8' element={<Calc8/>}></Route>
          <Route exact path='/calc9' element={<Calc9/>}></Route>
          <Route exact path='/calc10' element={<Calc10/>}></Route>
          <Route exact path='/calc11' element={<Calc11/>}></Route>
          <Route exact path='/calc12' element={<Calc12/>}></Route>
          <Route exact path='/calc13' element={<Calc13/>}></Route>
          <Route exact path='/calc14' element={<Calc14/>}></Route>
          <Route exact path='/calc15' element={<Calc15/>}></Route>
          <Route exact path='/calc16' element={<Calc16/>}></Route>
          <Route exact path='/calc17' element={<Calc17/>}></Route>
          <Route exact path='/calc18' element={<Calc18/>}></Route>
          <Route exact path='/calc19' element={<Calc19/>}></Route>
          <Route exact path='/calc20' element={<Calc20/>}></Route>
          <Route exact path='/calc21' element={<Calc21/>}></Route>
          <Route exact path='/calc22' element={<Calc22/>}></Route>
          <Route exact path='/calc23' element={<Calc23/>}></Route>
          <Route exact path='/calc24' element={<Calc24/>}></Route>
          <Route exact path='/calc25' element={<Calc25/>}></Route>
        </Routes>
      </BrowserRouter>
      </>
  );
}

export default App;
