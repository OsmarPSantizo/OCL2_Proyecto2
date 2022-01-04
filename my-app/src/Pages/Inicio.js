import React from "react";
import "./pages.css";

function Inicio(){
    return(
        <div className="titulo">
   
        <strong className="Calc">Este proyecto tiene como objetivo aprender a utilizar regresiones lineales para entrenar modelos y así lograr hacer predicciones o ver tendencias sobre distintos datos.</strong>
        <br></br>
        <strong className="Calc">El programa solo acepta archivos .csv.</strong>
        <strong className="Calc">Para ver los reportes disponibles haga click en el boton de Calculos y rellene los parámetros</strong>
        </div>
    );

}

export default Inicio;