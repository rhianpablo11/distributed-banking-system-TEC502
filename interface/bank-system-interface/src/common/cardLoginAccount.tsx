import { useState } from "react"
import styles from "../style_modules/commonStyles.module.css"
import LogoBank from "./logoBank"
import { useNavigate } from "react-router-dom"

function CardLoginAccount(){
    const navigate = useNavigate()
    const borderNotFillInput ={
        'border': '3px solid red'
    }

    const [styleCampInput, setStyleCampInput] = useState()

    function verifyElementsFilled(){
        const email = document.getElementById("emailRegister").value
        const password = document.getElementById("passwordRegister").value
        if(email=="" || password==""){
            console.log("algo")
            setStyleCampInput(borderNotFillInput)
        } else{
            setStyleCampInput()
            //verificar ainda a requisição ao servidor
            //esse valor apos o logged tem que definir ainda o que sera que vai usar
            return navigate("/logged/598")
        }
        
    }

    return(
        <>
            <div className={styles.createAccountBase}>
                <div className={styles.logoBankLogin}>
                    <LogoBank />
                </div>
                <div className={styles.inputsAreaLogin}>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="email" placeholder="Email" id="emailRegister"></input>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister"></input>
                </div>
                <button className={styles.buttonPreLogin} onClick={verifyElementsFilled}>
                    Login
                </button>
            </div>        
            <dialog>
                <p>apresentar a info que nao tem todos os campos preenchidos</p>
            </dialog>
        </>
    )
}

export default CardLoginAccount