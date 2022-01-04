import React, {useState} from "react";
import "./pages.css"
import {Form, Button} from 'react-bootstrap'

function Calc24(){

    const [confirmados2, setconfirmados] = useState("")
    const [pruebas2, setpruebas]= useState("")
    const [cpais2,setcpais]=useState("")
    const [npais2,setnpais]=useState("")

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
            reporte: 24,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            confirmados:confirmados2,
            pruebas:pruebas2,
            cpais: cpais2,
            npais:npais2
            
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


    return(
        <div className="titulo">
            <strong className="Calc">Comparación entre el número de casos detectados y el número de pruebas de un país.</strong>
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
              <Form.Control name="casos" placeholder="Columna para Pais" value={cpais2} onChange={(e)=> setcpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para casos confirmados</Form.Label>
              <Form.Control name="confirmados" placeholder="Columna para Confirmados" value={confirmados2} onChange={(e)=> setconfirmados(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para numero de pruebas</Form.Label>
              <Form.Control name="pais" placeholder="Columna para pruebas" value={pruebas2} onChange={(e)=> setpruebas(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el pais a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={npais2} onChange={(e)=> setnpais(e.target.value)}></Form.Control>
              </Form.Group>
              <br></br>
              <Button className="botones" onClick={handleClick} >Comparar</Button>
            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <b>Reporte</b>
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

export default Calc24;