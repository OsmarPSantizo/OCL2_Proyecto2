import React, {useState} from 'react';
import {Link} from "react-router-dom"
import * as Icons from "react-icons/fa"
import "./Navbar.css"
import {navItems} from "./Navitems"
import Button from "./Button"
import Dropdown from './Dropdown';

function Navbar(){
    const[dropdown,setDropdown]= useState(false);

    return (
        <>
        <nav className="navbar">
            <Link to="/" className="Navbar-logo">
               DataScience
                
            </Link>
            <ul className="nav-items">
                {navItems.map((item)=>{
                    if(item.title === "Calculos"){
                        return(
                            <li key={item.id} className={item.cName}
                                onMouseEnter={() => setDropdown(true)}  
                                onMouseLeave={() => setDropdown(false)}>
                                <Link to={item.path}>{item.title}</Link>
                                {dropdown&& <Dropdown/>}

                            </li>
                            ) 
                    }

                    return(
                    <li key={item.id} className={item.cName}>
                        <Link to={item.path}>{item.title}</Link>
                    </li>
                    )
                })}
            </ul>
            <Button/>
        </nav>
        </>
    );
}

export default Navbar
