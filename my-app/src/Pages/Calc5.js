import React, {useState} from "react";
import "./pages.css"
import {Form} from 'react-bootstrap'

function Calc2(){
    const [pais2, setpais] = useState("")
    const [dias2, setdias] = useState("")
    const [muertes2, setmuertes] = useState("")
    const [spais2, setspais2] = useState("")
    const [predict2, setpredict] = useState("")
    const [respuestaa, setrespuesta] = useState("No se que reporte soy")
     // Para el manejo de archivo
    const [contenidoArchvio, setcontenido]= useState("")
    const [tipoarchivo, setipoarchivo] = useState("")
    const handleClick =(event) =>{
      event.preventDefault();
      const options ={
        method:"POST",
        body:JSON.stringify({
          reporte: 5,
          content: contenidoArchvio,
          tipoa: tipoarchivo,
          cpais:pais2,
          dia: dias2,
          muertes: muertes2,
          spais: spais2,
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
        <div>
            <h1 className="Calc">Predicción de mortalidad por COVID en un País.</h1>

            <div className="row no-gutters">
        <div className = "col no-gutters">

          <div className = "leftside">
          
            <Form>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Selecciona un archivo .csv, .xsls</Form.Label>
              <Form.Control type="file" name="file" onChange={(e)=> handleFile(e)}/>
              </Form.Group>
              <h3>Parametrizacion</h3>
              <Form.Group>
              <Form.Label>Selecciona columna para Pais</Form.Label>
              <Form.Control name="pais1" placeholder="Columna para Pais" value={pais2} onChange={(e)=> setpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona la columna para Dias</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Pais" value={dias2} onChange={(e)=> setdias(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Muertes</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Muertes" value={muertes2} onChange={(e)=> setmuertes(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el Pais a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={spais2} onChange={(e)=> setspais2(e.target.value)}></Form.Control>
              <Form.Label>Dia a predecir</Form.Label>
              <Form.Control name="predict" placeholder="Dia a predecir" value={predict2} onChange={(e)=> setpredict(e.target.value)}></Form.Control>
              
              </Form.Group>
          
              
              <br></br>
              <button onClick={handleClick}>Consultar</button>
              



            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          <h1>{respuestaa}</h1>
          <h1>Graficaa</h1>

          </div>
        </div>

    </div>
        </div>
    );

}

export default Calc2;