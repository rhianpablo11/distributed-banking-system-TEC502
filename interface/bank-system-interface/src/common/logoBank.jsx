import { useState } from "react"
import elevenBankLogo from "../assets/Eleven Bank.svg"
import automobiliLogo from "../assets/Automobili Bank.svg"
import { useNavigate } from "react-router-dom"
import propsTypes from 'prop-types'
import styles from "../style_modules/commonStyles.module.css"


function LogoBank(props){
    const navigate = useNavigate()
    function goToLanding(){
        return navigate("/")
    }


    return(
        <>
            <div className={styles.logoBankStyle} onClick={goToLanding} >
                <h1>{props.nameBank}</h1>
                <h2>bank</h2>
            </div>
            
        </>
    )
}

LogoBank.propsTypes = {
    nameBank: propsTypes.string
}

LogoBank.defaultProps = {
    nameBank: "Automobili"
}

export default LogoBank