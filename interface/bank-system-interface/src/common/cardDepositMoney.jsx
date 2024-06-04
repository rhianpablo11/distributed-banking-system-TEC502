import styles from "../style_modules/commonStyles.module.css"
import qrCodeInter from "../assets/qrCodeInter.jpg"
import { useState } from "react"

function CardDepositMoney(){
    const qrCode = <div className={styles.qrCodeImage}>
                        <img  src={qrCodeInter}></img>
                    </div>
    
    const buttonOptionSelected = {
        'background': '#000000'
    }



    const [valueDepositChoice, setValueDepositChoice] = useState("")
    const [methodDeposit, setMethodDeposit] = useState("")

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
        setValueDepositChoice(valueCaptured)
    }
    
    function selectOptionDeposit(event){
        const optionSelected = event.target.value
        if(optionSelected == "money"){
            setMethodDeposit("money")
        } else if(optionSelected == "qrCode"){
            setMethodDeposit("qrCode")
        } else if(optionSelected == "bank slip"){
            setMethodDeposit("bankSlip")
        } 
    }
    

    return (
        <>
            <div className={styles.cardDepositMoneyBlock}>
                <h1>
                    Deposit
                </h1>
                <input className={styles.inputDepositValue} type="text" placeholder="Value" id="valueDeposit" value={valueDepositChoice} onChange={selectedOnlyNumber}></input>
                <div className={styles.buttonDeposit}>
                    <button style={methodDeposit=="money" ? buttonOptionSelected : {}} value="money" onClick={selectOptionDeposit}>
                        Money
                    </button>
                    <button style={methodDeposit=="qrCode" ? buttonOptionSelected : {}} value="qrCode" onClick={selectOptionDeposit}>
                        Qr Code
                    </button>
                    <button style={methodDeposit=="bankSlip" ? buttonOptionSelected : {}} value="bank slip" onClick={selectOptionDeposit}>
                        Bank Slip
                    </button>
                </div>
                {methodDeposit=="qrCode"? qrCode : ""}
                <button className={styles.buttonPayDeposit}>
                    Pay
                </button>
            </div>
        </>
    )
}

export default CardDepositMoney