import React, {useState} from 'react'
import {CalcItems } from "./Navitems"
import {Link} from "react-router-dom"
import "./Dropdown.css"

function Dropdown(){
    const [dropdown, setDropdown] = useState(false); 
    return(
        
        <>
        <ul 
        className={dropdown ? "calculos-submenu clicked" : "calculos-submenu"} 
        onClick={ () => setDropdown(!dropdown)}
        >
        {CalcItems.map ((item) =>{
            return(
                <li key ={item.id}>
                    <Link to={item.path} 
                    className ={item.cName} 
                    onClick={ () => setDropdown(false)}
                    >
                    {item.title}
                    </Link>
                </li>
            )
        })}
        </ul>
        </>
    )

}

export default Dropdown;