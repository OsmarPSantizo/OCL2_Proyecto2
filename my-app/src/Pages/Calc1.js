import React, {useState} from "react";
import "./pages.css"
import {InputGroup,FormControl,Form} from 'react-bootstrap'



function Consulting() {
  

  const [fecha2, setfecha] = useState("")
  const [dias2, setdias] = useState("")
  const [casos2, setcasos] = useState("")
  const [respuestaa, setrespuesta] = useState("No se que reporte soy")
  const [data2, setdata] = useState("")
  const handleClick =(event) =>{
    event.preventDefault();
    const options ={
      method:"POST",
      body:JSON.stringify({
        reporte: 1,
        dias:dias2,
        casos:casos2,
        fecha: fecha2
      })
    };
   

    fetch('https://powerful-tundra-15123.herokuapp.com/reportes',options)
    .then(resp =>{
      if(resp.status ===200) return resp.json();
      else alert("Erroooooor")
    })
    .then(data =>{
      setrespuesta(data.Reporte)
      console.log("Si se pudooo",data)
    })
    .catch(error =>{
      console.error("Hubo un error!!!",error)
    })
  }



  return (
 
  <div >
    
    <h1>Tendencia de la infección por Covid-19 en un País.</h1>

    <div className="row no-gutters">
        <div className = "col no-gutters">

          <div className = "leftside">
          <h1>Iran todos los datos</h1> 
            <Form>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Selecciona un archivo .csv, .xsls</Form.Label>
              <Form.Control type="file" name="archivo" onChange={(e)=> setdata(e.target.value)}/>
              </Form.Group>

      
              <Form.Group>
              <Form.Label>Selecciona columna para Casos</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Casos" value={casos2} onChange={(e)=> setcasos(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Fecha</Form.Label>
              <Form.Control name="fecha" placeholder="Columna para fecha" value={fecha2} onChange={(e)=> setfecha(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Días</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Dias" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              </Form.Group>
             
          
              
              <br></br>
              <button onClick={handleClick}>Probemos</button>

              



            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <h1>{respuestaa}</h1>
          <h1>Graficaa</h1>
          </div>
        </div>

    </div>
</div>



   
  );
}

export default Consulting;