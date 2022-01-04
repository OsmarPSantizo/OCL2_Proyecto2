import React, {useState} from "react";
import "./pages.css"
import {Form, Button} from 'react-bootstrap'

function Calc21(){
    const [dias2, setdia] = useState("")
    const [confirmados2, setconfirmados] = useState("")
    const [muertos2, setmuertos] = useState("")
    const [respuestaa, setrespuesta] = useState("")
    const [predict2,setpredict] = useState("")
    const [grafica2, setgrafica] = useState();

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
            reporte: 21,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            confirmados:confirmados2,
            muertos:muertos2,
            dias:dias2,
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
            <strong className="Calc">Predicciones de casos y muertes en todo el mundo </strong>
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
              <Form.Label>Selecciona columna para Dias</Form.Label>
              <Form.Control name="casos" placeholder="Columna para Dias" value={dias2} onChange={(e)=> setdia(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para Confirmados</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Confirmados" value={confirmados2} onChange={(e)=> setconfirmados(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Muertos</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Muertos" value={muertos2} onChange={(e)=> setmuertos(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el dia a calcular</Form.Label>
              <Form.Control name="predict" placeholder="Dia a predecir" value={predict2} onChange={(e)=> setpredict(e.target.value)}></Form.Control>
              
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

export default Calc21;