import React, {useState} from "react";
import "./pages.css"
import {Form,Button} from 'react-bootstrap'
import {jsPDF} from 'jspdf'


function  Calc1 (){
  
  const [fecha2, setfecha] = useState("")
  const [casos2, setcasos] = useState("")
  const [fpais2, setfpais] = useState("")
  const [npais2, setnpais] = useState("")
  const [respuestaa, setrespuesta] = useState("")
  const [grafica2, setgrafica] = useState();
   // Para el manejo de archivo
  const [contenidoArchvio, setcontenido]= useState("")
  const [tipoarchivo, setipoarchivo] = useState("")


    const pdfGenerate = (event) =>{
      event.preventDefault();
      var doc = new jsPDF('landscape','px','a4','false');
      doc.addImage(grafica2,'PNG',65,20,500,400)
      doc.save('reporte.pdf')
      

    }


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
        reporte: 1,
        content: contenidoArchvio,
        tipoa: tipoarchivo,
        casos:casos2,
        fecha: fecha2,
        pais: fpais2,
        npais: npais2
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
   
    <strong className="Calc">Tendencia de la infección por Covid-19 en un País.</strong>

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
              <Form.Label>Selecciona la columna para Pais</Form.Label>
              <Form.Control name="pais" placeholder="Columna para Pais" value={fpais2} onChange={(e)=> setfpais(e.target.value)}></Form.Control>
              <Form.Label>Selecciona columna para Fecha</Form.Label>
              <Form.Control name="dias" placeholder="Columna para Fecha" value={fecha2} onChange={(e)=> setfecha(e.target.value)}></Form.Control>
              </Form.Group>
              <h3>Datos</h3>
              <Form.Group>
              <Form.Label>Ingresa el pais a calcular</Form.Label>
              <Form.Control name="npais" placeholder="Nombre del pais" value={npais2} onChange={(e)=> setnpais(e.target.value)}></Form.Control>
              
              </Form.Group>
              
              <br></br>
              <Button className="botones" onClick={handleClick}>Consultar</Button>
            
            </Form>
         
          </div>
        </div>
        <div className ="col no-gutters">
          <div className = "rightside">
          
          <b>Reporte</b>
          <br></br>
          <img  src={grafica2}/>  
          <br></br>
          <Button className="botones"onClick={getgrafica}>Mostrar Grafica</Button>
          <h3>{respuestaa}</h3>
          <br></br>
          <Button className="botones" onClick={pdfGenerate}>Descargar PDF</Button>
          </div>
        </div>

    </div>
</div>



  )  
  
}

export default Calc1;