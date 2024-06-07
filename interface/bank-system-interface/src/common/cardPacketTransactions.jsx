
import { useState } from "react"
import styles from "../style_modules/commonStyles.module.css"
import CardInfoTransactionForMakeInPacket from "./cardInfoTransactionForMakeInPacket";

function CardPacketTransactions(){
    const [valueTransaction, setValueTransaction] = useState()
    
    
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
        setValueTransaction(valueCaptured)
    }


    return(
        <>
            <div className={styles.superiorPartTransactions}>
                <h1>
                    Mount Packet of Transactions:
                </h1>
                <div className={styles.constructTrasaction}>
                    <select>
                            <option value=''>Select your bank source money</option>
                            <option value='elevenBank'>Eleven Bank</option>
                    </select>
                    <input type="text" placeholder="Key Pix" id="keyPix"></input>
                    <input type="text" placeholder="Value" id="value" value={valueTransaction} onChange={selectedOnlyNumber}></input>
                    <button>add operation</button>
                </div>
                <div className={styles.operationsOfPacketTransactionsArea}>
                    <div className={styles.textExplainCamps}>
                        <h1>
                            Bank Name:
                        </h1>
                        <h1>
                            Key Pix:
                        </h1>
                        <h1>
                            Value:
                        </h1>
                    </div>
                    <ul>
                        <li>
                            <CardInfoTransactionForMakeInPacket />
                        </li>
                        <li>
                            <CardInfoTransactionForMakeInPacket />
                        </li>
                        <li>
                            <CardInfoTransactionForMakeInPacket />
                        </li>
                        <li>
                            <CardInfoTransactionForMakeInPacket />
                        </li>
                    </ul>
                    
                </div>
            </div>
        </>
    )
}

export default CardPacketTransactions