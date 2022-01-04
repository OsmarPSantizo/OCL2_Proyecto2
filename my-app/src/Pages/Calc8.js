import React, {useState} from "react";
import "./pages.css"
import {Form,Button} from 'react-bootstrap'


function Calc8(){
    const [cpais2, setcpais] = useState("")
    const [anio2, setanio] = useState("")
    const [npais2, setnpais] = useState("")
    const [respuestaa, setrespuesta] = useState("")
    const [grafica2, setgrafica] = useState();
    const [fecha2, setfecha] = useState("");
    const [predict2,setpredict] = useState("")

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
            reporte: 8,
            content: contenidoArchvio,
            tipoa: tipoarchivo,
            anio:anio2,
            cpais: cpais2,
            npais: npais2,
            fecha: fecha2,
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
            <strong className="Calc">Predicción de casos de un país para un año.</strong>
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
              <Form.Label>Selecciona la columna para casos</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Casos" value={anio2} onChange={(e)=> setanio(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la para Fecha</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Fecha" value={fecha2} onChange={(e)=> setfecha(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el pais a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={npais2} onChange={(e)=> setnpais(e.target.value)}></Form.Control>
              
              <Form.Label>Ingresa la fecha a predecir</Form.Label>
              <Form.Control name="npais" placeholder="Fecha a predecir YYYY-MM-DD" value={predict2} onChange={(e)=> setpredict(e.target.value)}></Form.Control>
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

export default Calc8;