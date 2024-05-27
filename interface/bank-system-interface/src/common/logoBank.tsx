import { useState } from "react"
import elevenBankLogo from "../assets/Eleven Bank.svg"
import automobiliLogo from "../assets/Automobili Bank.svg"

function LogoBank(){
    const bank = automobiliLogo
    return(
        <>
            <img  src={bank}></img>
        </>
    )
}

export default LogoBank