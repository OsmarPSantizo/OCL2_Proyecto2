import React, {useState} from "react";
import "./pages.css"
import {Form, Button} from 'react-bootstrap'

function Calc10(){
    const [cvacunados2, setcvacunados] = useState("")
    const [cpais2,setcpais]=useState("")
    const [n1pais2,setn1pais]=useState("")
    const [n2pais2,setn2pais]=useState("")
    const [cdias2,setdias]=useState("")

    const [respuestaa, setrespuesta] = useState("")
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
            reporte: 10,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            cvacunados: cvacunados2,
            cpais: cpais2,
            n1pais:n1pais2,
            n2pais:n2pais2,
            dias:cdias2
            
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
            <strong className="Calc">Análisis Comparativo de Vacunación entre 2 paises.</strong>
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
              <Form.Control name="dias" placeholder="Columna para Dias" value={cdias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Pais</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Pais" value={cpais2} onChange={(e)=> setcpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para casos Vacunados</Form.Label>
              <Form.Control name="vacunados" placeholder="Columna para Vacunados" value={cvacunados2} onChange={(e)=> setcvacunados(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el primer pais</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={n1pais2} onChange={(e)=> setn1pais(e.target.value)}></Form.Control>
              <Form.Label>Ingresa el segundo pais</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={n2pais2} onChange={(e)=> setn2pais(e.target.value)}></Form.Control>
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

export default Calc10;