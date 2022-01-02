
import React, {useState} from "react";
import "./pages.css"
import {Form} from 'react-bootstrap'
import { Bar } from 'react-chartjs-2'





function Calc2 (){

    const [pais2, setpais] = useState("")
    const [casos2, setcasos] = useState("")
    const [dias2, setdias] = useState("")
    const [prediccion2, setprediccion] = useState(0)
    const [respuestaa, setrespuesta] = useState("Ingrese la informacion para predecir")
    // Para el manejo de archivo
    const [contenidoArchvio, setcontenido]= useState("")
    const [tipoarchivo, setipoarchivo] = useState("")

    const handleClick =(event) =>{
      event.preventDefault();
      const options ={
        method:"POST",
        body:JSON.stringify({
          reporte: 2,
          content: contenidoArchvio,
          tipoa: tipoarchivo,
          dias:dias2,
          pais:pais2,
          casos: casos2,
          predic: prediccion2
          
        })
      };
     
  
      fetch('https://powerful-tundra-15123.herokuapp.com/reportes',options)
      .then(resp =>{
        if(resp.status ===200) return resp.json();
        else alert("Si sale esto. Creo que no ganaré compi :C")
      })
      .then(data =>{
        setrespuesta("Los infectados serán " + data.Reporte)
      
      })
      .catch(error =>{
        console.error("Hubo un error!!!",error)
      })
    }

    async function handleFile(event){
        event.preventDefault();
        var file = event.target.files[0]
        setipoarchivo(file.name.split(".")[1])
        var reader = new FileReader();
        reader.onload = function(event) {
          setcontenido(event.target.result)
        }
        reader.readAsText(file)      
      }

      

    return(
        <div>
            <h1>Predicción de Infectados en un País..</h1>
            <div className="row no-gutters">
        <div className = "col no-gutters">

          <div className = "leftside">
          <h1>Iran todos los datos</h1> 
            <Form>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Selecciona un archivo .csv, .xsls</Form.Label>
              <Form.Control type="file" name="file" onChange={(e)=> handleFile(e)}/>
              </Form.Group>
      
              <Form.Group>
              <Form.Label>Selecciona columna para Pais</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Pais" value={pais2} onChange={(e)=> setpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Casos</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Casos" value={casos2} onChange={(e)=> setcasos(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Días</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Dias" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              <Form.Label>Dia a predecir</Form.Label>
              <Form.Control name="prediccion" placeholder="Ingrese día a predecir" value={prediccion2} onChange={(e)=> setprediccion(e.target.value)}></Form.Control>
              </Form.Group>
              
              <br></br>
              <button onClick={handleClick}>Consultar</button>
              



            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          
          <h1>Grafica</h1>
         
             
          <h5> {respuestaa}</h5>
          
          </div>
        </div>

    </div>
            
        </div>
    );

}

export default Calc2;