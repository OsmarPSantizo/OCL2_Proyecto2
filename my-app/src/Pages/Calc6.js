import React, {useState} from "react";
import "./pages.css"
import {Form,Button} from 'react-bootstrap'


function Calc6(){
    const [pais2, setpais] = useState("")
    const [dias2, setdias] = useState("")
    const [muertes2, setmuertes] = useState("")
    const [spais2, setspais2] = useState("")
    const [grafica2, setgrafica] = useState();
    const [respuestaa, setrespuesta] = useState("")

    const [contenidoArchvio, setcontenido]= useState("")
    const [tipoarchivo, setipoarchivo] = useState("")

    async function getgrafica (event){
        event.preventDefault()
        const response = await fetch("https://powerful-tundra-15123.herokuapp.com/plot.png");
        const data = await response.blob()
        const imageObjectUrl = URL.createObjectURL(data)
        setgrafica(imageObjectUrl)
      }
      const handleClick =(event) =>{
        event.preventDefault();
        const options ={
          method:"POST",
          body:JSON.stringify({
            reporte: 6,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            cpais:pais2,
            dia: dias2,
            muertes: muertes2,
            spais: spais2,
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
            <strong className="Calc">Análisis del número de muertes por coronavirus en un País.</strong>
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
              <Form.Control name="pais1" placeholder="Columna para Pais" value={pais2} onChange={(e)=> setpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para Fecha</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Fecha" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Muertes</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Muertes" value={muertes2} onChange={(e)=> setmuertes(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el Pais a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={spais2} onChange={(e)=> setspais2(e.target.value)}></Form.Control>
              </Form.Group>
          
              <br></br>
              <Button className="botones" onClick={handleClick}>Consultar</Button>

            </Form>        
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <h3>Reporte</h3>
          <img  src={grafica2}/>  
          <Button className="botones" onClick={getgrafica}>Mostrar Grafica</Button>
          <br></br>
          <h3>{respuestaa}</h3>
  <br></br>
          <Button className="botones">Descargar PDF</Button>
          </div>
        </div>

    </div>
        </div>
    );

}

export default Calc6;