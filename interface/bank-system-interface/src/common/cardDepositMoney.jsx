import styles from "../style_modules/commonStyles.module.css"
import qrCodeInter from "../assets/qrCodeInter.jpg"
import { useState } from "react"
import propsTypes from 'prop-types'
import Loading from "./loading";


function CardDepositMoney(props){
    const qrCode = <div className={styles.qrCodeImage}>
                        <img  src={qrCodeInter}></img>
                    </div>
    
    const buttonOptionSelected = {
        'background': '#000000'
    }

    const buttonOptionNotSelected = {
        'background': '#444444'
    }


    const [valueDepositChoice, setValueDepositChoice] = useState("")
    const [methodDeposit, setMethodDeposit] = useState("")
    const [isButtonClicked, setIsButtonClicked] = useState(true)
    const [loading, setLoading] = useState(false)

    function selectedOnlyNumber(event){
        let valueCaptured = event.target.value.replace(/[^0-9.]/g, '')
        const partsValue = valueCaptured.split('.');
        if (partsValue.length > 2) {
            valueCaptured = partsValue[0] + '.' + partsValue.slice(1).join('');
        }
        if (partsValue.length === 2) {
            partsValue[1] = partsValue[1].substring(0, 2);
            valueCaptured = partsValue.join('.');
        }
        console.log(props.cpfCNPJ_user)
        setValueDepositChoice(valueCaptured)
    }
    


    function selectOptionDeposit(event){
        const optionSelected = event.target.value
        setIsButtonClicked(!isButtonClicked)
        console.log(methodDeposit)
        if(isButtonClicked){
            if(optionSelected == "money"){
                setMethodDeposit("money")
            } else if(optionSelected == "qrCode"){
                setMethodDeposit("qrCode")
            } else if(optionSelected == "bank slip"){
                setMethodDeposit("bankSlip")
            } 
        } else{
            setMethodDeposit("none")
        }
        
    }
    
    const addressBank = localStorage.getItem("addressBank")

    

    const makeDeposit = async () => {
        try {
            const url =addressBank+"/account/deposit"
            console.log(url)
            const response = await fetch(url, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "cpfCNPJ1": props.cpfCNPJ_user,
                    "value": valueDepositChoice,
                    "method": methodDeposit
                })

            })
            
            setLoading(true)
            if (response.ok) {
                const result = await response.json();
                console.log(result)
                // finalizar a apresentação do loading
                setLoading(false);

            } else {
                // Caso a resposta não esteja ok, lança apresentação de senha incorreta
                throw new Error('Network response was not ok');
            }
        } catch (error) {
          //indicar que ocorreu um erro
          //setNotBankConnection(true);
        } finally {
          // finalizar a apresentação do loading
          setLoading(false);
        }
      };

    function canMakeDeposit(){
        if(valueDepositChoice != ""){
            console.log("oie")
            makeDeposit()
            setValueDepositChoice("")
        } 
        //colocar o avliso de qu nao tem nada la e entao nao pode fazer o deposito
    }

    return (
        <>
            <div className={styles.cardDepositMoneyBlock}>
                <h1>
                    Deposit
                </h1>
                <input className={styles.inputDepositValue} type="text" placeholder="Value" id="valueDeposit" value={valueDepositChoice} onChange={selectedOnlyNumber}></input>
                <div className={styles.buttonDeposit}>
                    <button style={methodDeposit=="money" ? buttonOptionSelected : buttonOptionNotSelected} value="money" onClick={selectOptionDeposit}>
                        Money
                    </button>
                    <button style={methodDeposit=="qrCode" ? buttonOptionSelected : buttonOptionNotSelected} value="qrCode" onClick={selectOptionDeposit}>
                        Qr Code
                    </button>
                    <button style={methodDeposit=="bankSlip" ? buttonOptionSelected : buttonOptionNotSelected} value="bank slip" onClick={selectOptionDeposit}>
                        Bank Slip
                    </button>
                </div>
                {methodDeposit=="qrCode" ? qrCode : ""}
                <button onClick={canMakeDeposit} className={styles.buttonPayDeposit}>
                    Pay
                </button>
                <Loading isOpen={loading} />
            </div>
        </>
    )
}



CardDepositMoney.propsTypes = {
    cpfCNPJ_user: propsTypes.string
}

CardDepositMoney.defaultProps = {
    cpfCNPJ_user: "undefined"
}

export default CardDepositMoney