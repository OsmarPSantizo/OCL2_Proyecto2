import React, {useState} from "react";
import "./pages.css"
import {Form} from 'react-bootstrap'

function Calc25(){
    const [dias2, setdias] = useState("")
    const [cdias2, setcdia] = useState("")
    const [casos2, setcasos] = useState("")
    const [predict2, setpredict] = useState("")
    const [respuestaa, setrespuesta] = useState("")
    const [grafica2, setgrafica] = useState();

    const [contenidoArchvio, setcontenido]= useState("")
    const [tipoarchivo, setipoarchivo] = useState("")
    async function getgrafica (event){
        event.preventDefault()
        const response = await fetch("http://127.0.0.1:5000/plot.png");
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
            reporte: 25,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            casos:casos2,
            cdias: cdias2,
            predict: predict2,
            pdias: dias2
          })
        };
       
    
        fetch('http://127.0.0.1:5000/reportes',options)
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
        <div>
            <h1 className="Calc">Predicción de casos confirmados por día</h1>
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
              <Form.Label>Selecciona columna para Casos</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Casos" value={casos2} onChange={(e)=> setcasos(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para Dias</Form.Label>
              <Form.Control name="cdias" placeholder="Columna para Dias" value={cdias2} onChange={(e)=> setcdia(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el día a predecirr</Form.Label>
              <Form.Control name="pdias" placeholder="Dia a predecir" value={predict2} onChange={(e)=> setpredict(e.target.value)}></Form.Control>
              
              </Form.Group>
          
              
              <br></br>
              <button onClick={handleClick} >Consultar</button>
            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <h3>Grafica</h3>
          <img  src={grafica2}/>  
          <button onClick={getgrafica}>Mostrar Grafica</button>
          <h5>{respuestaa}</h5>     
          </div>
        </div>

    </div>
        </div>
    );

}

export default Calc25;