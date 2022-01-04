import React, {useState} from "react";
import "./pages.css"
import {Form, Button} from 'react-bootstrap'

function Calc15(){
const [dias2, setdias] = useState("")
const [casos2, setcasos] = useState("")
const [cpais2, setcpais] = useState("")
const [npais2, setnpais] = useState("")
const [cdepar2, setcdepar] = useState("")
const [ndepar2, setndepar] = useState("")
const [respuestaa, setrespuesta] = useState("")
const [grafica2, setgrafica] = useState();

 // Para el manejo de archivo
const [contenidoArchvio, setcontenido]= useState("")
const [tipoarchivo, setipoarchivo] = useState("")

async function getgrafica (event){
    event.preventDefault()
    const response = await fetch("https://powerful-tundra-15123.herokuapp.com/plot.png");
    const data = await response.blob()
    const imageObjectUrl = URL.createObjectURL(data)
    console.log(imageObjectUrl)
    setgrafica(imageObjectUrl)
    
  }
  
  const handleClick =(event) =>{
    event.preventDefault();
    const options ={
      method:"POST",
      body:JSON.stringify({
        reporte: 15,
        content: contenidoArchvio,
        tipoa: tipoarchivo,
        dias:dias2,
        casos: casos2,
        cpais: cpais2,
        npais: npais2,
        cdepar: cdepar2,
        ndepar:ndepar2
      })
    };
   

    fetch('https://powerful-tundra-15123.herokuapp.com/reportes',options)
    .then(resp =>{
      if(resp.status ===200) return resp.json();
      else alert("Si sale esto. Creo que no ganaré compi :C")
    })
    .then(data =>{
      setrespuesta(data.Reporte)
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
      <div className="titulo">
            <strong className="Calc">Tendencia de casos confirmados de Coronavirus en un departamento de un País..</strong>
            <div className="row no-gutters">
        <div className = "col no-gutters">

          <div className = "leftside">
          
            <Form>
            <h3>Carga de archivo</h3>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Selecciona un archivo .csv, .xsls</Form.Label>
              <Form.Control type="file" name="file" onChange={(e)=> handleFile(e)}/>
              </Form.Group>
              <h3>Parametrizacion</h3>
              <Form.Group>
              <Form.Label>Selecciona columna para Pais</Form.Label>
              <Form.Control name="pais" placeholder="Columna para pais" value={cpais2} onChange={(e)=> setcpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para Departamento</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Departamento" value={cdepar2} onChange={(e)=> setcdepar(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Dias</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Dias" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna Casos</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Casos" value={casos2} onChange={(e)=> setcasos(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el pais a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={npais2} onChange={(e)=> setnpais(e.target.value)}></Form.Control>
              <Form.Label>Ingresa el departamento a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={ndepar2} onChange={(e)=> setndepar(e.target.value)}></Form.Control>
              
              </Form.Group>
          
              
              <br></br>
              <Button className="botones" onClick={handleClick} >Consultar</Button>
            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <b>Reporte</b>
          <br></br>
          <img  src={grafica2}/>  
          <br></br>
          <Button className="botones" onClick={getgrafica}>Mostrar Grafica</Button>
          <h5>{respuestaa}</h5>     
          </div>
        </div>
    </div>
        </div>
    );

}

export default Calc15;