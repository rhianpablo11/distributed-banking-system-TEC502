import { useState } from "react"
import elevenBankLogo from "../assets/Eleven Bank.svg"
import automobiliLogo from "../assets/Automobili Bank.svg"
import { useNavigate } from "react-router-dom"


function LogoBank(){
    const bank = elevenBankLogo
    const navigate = useNavigate()
    function goToLanding(){
        return navigate("/")
    }

    return(
        <>
            <img onClick={goToLanding} src={bank}></img>
        </>
    )
}

export default LogoBank