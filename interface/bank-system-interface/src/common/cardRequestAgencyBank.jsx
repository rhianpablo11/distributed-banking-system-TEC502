import { useState, useEffect } from "react"
import styles from "../style_modules/commonStyles.module.css"
import { useNavigate } from "react-router-dom"
import Loading from "./loading"

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

    function goBank(bankName){
        return navigate("/"+bankName)
    }


    function setAddress(){
        const address = document.getElementById('agencyNumber').value
        if(address == ""){
            setAddressSeted(false)
        } else{
            const url = "http://localhost:"+address+"/bank"
            const urlBank = "http://localhost:"+address
            localStorage.setItem("addressBank", urlBank)
            localStorage.setItem('ipBank', address)
            setAddressBank(url)
            requestBankName()
        }
        
    }

    const requestBankName = async () => {
        try {
            setLoading(true)
            const response = await fetch(addressBank)
            
            if (response.ok) {
                const result = await response.json();
                
                // finalizar a apresentação do loading
                setLoading(false);
                goBank(result.nameBank)
                
            } else {
                // Caso a resposta não esteja ok, lança um erro
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
            </div>
        
        </>
    )
}

export default CardRequestAgencyBank