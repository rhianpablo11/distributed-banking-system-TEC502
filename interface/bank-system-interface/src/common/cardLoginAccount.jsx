import { useState } from "react"
import styles from "../style_modules/commonStyles.module.css"
import LogoBank from "./logoBank"
import { useNavigate } from "react-router-dom"
import propsTypes from 'prop-types'
import Loading from "./loading"
import { useParams } from "react-router-dom"
import ErrorOperation from "./errorOperation";

function CardLoginAccount(props){
    const navigate = useNavigate()
    const {nameBank} =useParams()
    const borderNotFillInput ={
        'border': '3px solid #ba1111'
    }

    const [styleCampInput, setStyleCampInput] = useState()

    const [userData, setUserData] = useState()

    const addressBank = localStorage.getItem(nameBank)

    const [loading, setLoading] = useState(false)

    const [isError, setIsError] = useState(false)
    const [errorMensage,setErrorMensage] = useState()
    const closeErrorModal = () => {
        setIsError(false);
    };


    const requestUser = async (email, password) => {
        try {
            setLoading(true)
            const url =addressBank+"/account/login"
            console.log(url)
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "email": email,
                    "password": password
                })

            })
            
            
            
            if (response.ok) {
                const result = await response.json();
                console.log(result)
                // finalizar a apresentação do loading
                setLoading(false);
                setUserData(result)
                //vai para a pagina correta
                console.log(userData.accountNumber)
                return navigate("/logged/"+nameBank+"/"+result.accountNumber)
            } else {
                // Caso a resposta não esteja ok, lança apresentação de senha incorreta
                setLoading(false)
                setIsError(true)
                console.log('OI EU')
                const auxTemp = await response.text()
                setErrorMensage(auxTemp)
                throw new Error('Network response was not ok');
            }
        } catch (error) {
          //indicar que ocorreu um erro
          //setNotBankConnection(true);
          setLoading(false);
        } finally {
          // finalizar a apresentação do loading
          setLoading(false);
        }
      };


    function verifyElementsFilled(){
        const email = document.getElementById("emailRegister").value
        const password = document.getElementById("passwordRegister").value
        if(email=="" || password==""){
            
            setStyleCampInput(borderNotFillInput)
        } else{
            setStyleCampInput()
            //verificar ainda a requisição ao servidor
            //esse valor apos o logged tem que definir ainda o que sera que vai usar
            
            requestUser(email,password)
        }
        
    }

    return(
        <>
            <div className={styles.createAccountBase}>
                <div className={styles.logoBankPreLogin}>
                    <LogoBank nameBank = {nameBank} />
                </div>
                <div className={styles.inputsAreaLogin}>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="email" placeholder="Email" id="emailRegister"></input>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister"></input>
                </div>
                <button className={styles.buttonPreLogin} onClick={verifyElementsFilled}>
                    Login
                </button>
            </div>
            <Loading isOpen={loading}/>      
            <ErrorOperation isOpen={isError} textShow={errorMensage} onClose={closeErrorModal} />
            <dialog>
                <p>apresentar a info que nao tem todos os campos preenchidos</p>
            </dialog>
        </>
    )
}


CardLoginAccount.propsTypes = {
    nameBank: propsTypes.string
}

CardLoginAccount.defaultProps = {
    nameBank: "Unified"
}

export default CardLoginAccount