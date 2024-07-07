import { useState, useEffect } from "react"
import styles from "../style_modules/requestAgencyBank.module.css"
import { useNavigate } from "react-router-dom"
import Loading from "./loading"
import ErrorOperation from "./errorOperation";

function CardRequestAgencyBank(){
    //fazer o request para pegar o nome do banco
    const navigate = useNavigate()
    //para ficar loading enquanto espera o banco responder a requisição
    const [loading, setLoading] = useState(false)
    //se nao conseguir conectar c o banco vai para true
    const [notBankConnection, setNotBankConnection] = useState(false)
    //para salvar o endereço colocado dentro do input
    const [addressBank, setAddressBank] = useState("")
    //avisar que nao preencheu o input
    const [addressSeted, setAddressSeted] = useState(true)
    const [addressTyped, setAddressTyped] = useState("")
    const [isError, setIsError] = useState(false)
    const [errorMensage,setErrorMensage] = useState()
    const closeErrorModal = () => {
        setIsError(false);
    };



    function goBank(bankName){
        return navigate("/"+bankName)
    }


    function setAddress(){
        const address = document.getElementById('agencyNumber').value
        if(address == ""){
            setAddressSeted(false)
        } else{
            const url = "http://"+address+"/bank"
            const urlBank = "http://"+address
            localStorage.setItem("addressBank", urlBank)
            localStorage.setItem('ipBank', address)
            setAddressBank(url)
            setAddressTyped(address)
            requestBankName()
        }
        
    }

    const requestBankName = async () => {
        try {
            setLoading(true)
            console.log('parte 0')
            const response = await fetch(addressBank)
            console.log(response)
            console.log('parte 1')

            if (response.ok) {
                console.log(response)
                const result = await response.json()
                console.log(result)
                console.log('parte 2')
                // finalizar a apresentação do loading
                setLoading(false);
                const urlBank = "http://"+ addressTyped
                localStorage.setItem(result.nameBank, urlBank)
                console.log("oi oi")
                navigate("/"+result.nameBank)
                
            } else {
                // Caso a resposta não esteja ok, lança um erro
                setLoading(false)
                setIsError(true)
                console.log('OI EU')
                const auxTemp = await response.text()
                setErrorMensage(auxTemp)
                throw new Error('Network response was not ok');
            }
        } catch (error) {
          //indicar que ocorreu um erro
          setNotBankConnection(true);
        } finally {
          // finalizar a apresentação do loading
          setLoading(false);
        }
      };


    return (
        <>
            <div className={styles.requestAgencyComponent}>
                <div className={styles.backgroundRequestAgencyComponent}>
                    <div className={styles.logoUnifiedBank}>
                        <h1>Unified</h1>
                        <h3>Banks</h3>
                    </div>
                    <div className={styles.subtitleLogoUnifiedBank}> 
                        <h6>National banking consortium</h6>
                    </div>
                    <div className={styles.inputAgencyNumber}>
                        <h1>Please enter the number of the desired agency.</h1>
                        <input type="text" placeholder="Agency Number" id="agencyNumber"></input>
                        <button onClick={setAddress}>Go to Bank Page</button>
                    </div>
                </div>
                <Loading isOpen = {loading} />
                <ErrorOperation isOpen={isError} textShow={errorMensage} onClose={closeErrorModal} />
            </div>
        
        </>
    )
}

export default CardRequestAgencyBank