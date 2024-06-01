import styles from "../style_modules/commonStyles.module.css"
import qrCodeInter from "../assets/qrCodeInter.jpg"
import { useState } from "react"

function CardDepositMoney(){
    const qrCode = <div className={styles.qrCodeImage}>
                        <img  src={qrCodeInter}></img>
                    </div>
    
    const [valueDepositChoice, setValueDepositChoice] = useState(0)
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
    

    return (
        <>
            <div className={styles.cardDepositMoneyBlock}>
                <h1>
                    Deposit
                </h1>
                <input className={styles.inputDepositValue} type="text" placeholder="Value" id="valueDeposit" value={valueDepositChoice} onChange={selectedOnlyNumber}></input>
                <div className={styles.buttonDeposit}>
                    <button>
                        Money
                    </button>
                    <button>
                        Qr Code
                    </button>
                    <button>
                        Bank Slip
                    </button>
                </div>
                {qrCode}
                <button className={styles.buttonPayDeposit}>
                    Pay
                </button>
            </div>
        </>
    )
}

export default CardDepositMoney