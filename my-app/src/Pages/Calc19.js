import React, {useState} from "react";
import "./pages.css"
import {Form, Button} from 'react-bootstrap'

function Calc19(){
    const [canio2, setcanio] = useState("")
    const [nanio2, setnanio] = useState("")
    const [muertes2,setmuertes] = useState("")
    const [respuestaa, setrespuesta] = useState("")
    const [grafica2, setgrafica] = useState();
    const [dias2, setdias] = useState("");

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
            reporte: 19,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            canio:canio2,
            nanio:nanio2,
            dias:dias2,
            muertes:muertes2
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
            <h1 className="Calc">Predicción de muertes en el último día del primer año de infecciones en un país.</h1>
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
              <Form.Label>Selecciona columna para Año</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Año" value={canio2} onChange={(e)=> setcanio(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para muertes</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Muertes" value={muertes2} onChange={(e)=> setmuertes(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la para Dias</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Dias" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el año a calcular</Form.Label>
              <Form.Control name="nanio" placeholder="Año a calcular" value={nanio2} onChange={(e)=> setnanio(e.target.value)}></Form.Control>
              </Form.Group>
              <br></br>
              <Button className="botones" onClick={handleClick} >Consultar Muertes al último dia del año</Button>
              
            </Form>
         
          
            </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <h3>Grafica</h3>
          <br></br>
          <div><img  src={grafica2}/>  </div>
          
          <br></br>
          <Button className="botones" onClick={getgrafica}>Mostrar Grafica</Button>
          <h5>{respuestaa}</h5>     
          </div>
        </div>

    </div>
        </div>
    );

}

export default Calc19;