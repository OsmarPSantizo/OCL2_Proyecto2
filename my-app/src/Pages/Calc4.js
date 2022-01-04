import React, {useState} from "react";
import "./pages.css"
import {Form,Button} from 'react-bootstrap'

function Calc2(){
    const [departamento2, setdepartamento] = useState("")
    const [dias2, setdias] = useState("")
    const [muertes2, setmuertes] = useState("")
    const [sdepartamento2, setsdepartamento] = useState("")
    const [predict2, setpredict] = useState("")
    const [grafica2, setgrafica] = useState();
    const [respuestaa, setrespuesta] = useState("Ingrese la informacion para predecir")
     // Para el manejo de archivo
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
          reporte: 4,
          content: contenidoArchvio,
          tipoa: tipoarchivo,
          cdepartamento:departamento2,
          dia: dias2,
          muertes: muertes2,
          sdepartamento: sdepartamento2,
          predict:predict2
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
            <strong className="Calc">Predicción de mortalidad por COVID en un Departamento.</strong>
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
              <Form.Label>Selecciona columna para Departamento</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Departamento" value={departamento2} onChange={(e)=> setdepartamento(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para Fecha</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Fecha" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Muertes</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Muertes" value={muertes2} onChange={(e)=> setmuertes(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el Departamento a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del Departamento" value={sdepartamento2} onChange={(e)=> setsdepartamento(e.target.value)}></Form.Control>
              <Form.Label>Fecha a predecir</Form.Label>
              <Form.Control name="predict" placeholder="Ingrese fecha a predecir YYYY-MM-DD" value={predict2} onChange={(e)=> setpredict(e.target.value)}></Form.Control>
              
              </Form.Group>
          
              
              <br></br>
              <Button className="botones" onClick={handleClick}>Consultar</Button>
              



            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <h3>Grafica</h3>
          <img  src={grafica2}/>  
          <Button className="botones" onClick={getgrafica}>Mostrar Grafica</Button>
          <h3>{respuestaa}</h3>
          <br></br>
          <Button className="botones">Descargar PDF</Button>
  
          </div>
        </div>

    </div>
        </div>
    );

}

export default Calc2;