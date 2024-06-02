import { useState } from "react";
import styles from "../style_modules/commonStyles.module.css"

function CardFastPix(){
    
    const [cpfOrCNPJ, setCpfCNPJ] = useState("CNPJ")
    
    const styleInputValue = {
        'text-align': 'end',
        'padding-right': '10px'
    }

    
    const [valueSendPix, setvalueSendPix] = useState("")

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


        setvalueSendPix(valueCaptured)
    }


    return (
        <>
            <div className={styles.fastPixBlock}>
                <h1>Fast Pix</h1>
                <div className={styles.inputArea}>
                    <div className={styles.inputKeyPix}>
                        <input placeholder="Key:" type="text"></input>
                    </div>
                </div>
                <button>
                    Search
                </button>
                <div className={styles.fastPixInfoReceiver}>
                    <div className={styles.fastPixInfoReceiverData}>
                        <h4>Name: </h4>
                        <h3>Rhian Pablo </h3>
                    </div>
                    <div className={styles.fastPixInfoReceiverData}>
                        <h4>{cpfOrCNPJ}: </h4>
                        <h3>00.416.968/0001-01</h3>
                    </div>
                    <div className={styles.fastPixInfoReceiverData}>
                        <h4>Bank: </h4>
                        <h3>Automobili Bank</h3>
                    </div>
                </div>
                <div className={styles.inputArea}>
                    <div className={styles.inputKeyPix}>
                        <input className={styles.inputValuePix} placeholder="Value:" type="text" value={valueSendPix} onChange={selectedOnlyNumber}></input>
                    </div>
                </div>
                <button>
                    Send
                </button>
            </div>
            
        </>
    )
}

export default CardFastPix 