
import { useState } from "react"
import styles from "../style_modules/commonStyles.module.css"
import CardInfoTransactionForMakeInPacket from "./cardInfoTransactionForMakeInPacket";

function CardPacketTransactions(){
    const [valueTransaction, setValueTransaction] = useState()
    const [listTransactionsToMake, setListTransactionsToMake] = useState([])
    
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

    const [loading, setLoading] = useState(false)
    const [accountDataParcial, setAccountDataParcial] = useState()
    const [IdBank, setIdBank] = useState()
    const [keyPix, setKeyPix] = useState()
    const [bankSourceMoney, setBankSourceMoney] = useState()

    const addressBank = localStorage.getItem("addressBank")

    const requestInfoAboutUserPix = async (keyPix, IdBank) => {
        try {
            const url =addressBank+"/account/transaction/pix/infos"
            console.log(url)
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "keyPix": keyPix,
                    "bankID": IdBank
                })

            })
            
            setLoading(true)
            if (response.ok) {
                const result = await response.json();
                console.log(result)
                // finalizar a apresentação do loading
                setLoading(false);
                setAccountDataParcial(result)
                const transactionPartObject = {
                    'bankSource': "Eleven",
                    'keyPix': IdBank+"?"+keyPix,
                    'value': valueTransaction,
                    'nameReceptor': result.name
                }
                //adicionar esse objeto na lista
                setListTransactionsToMake([...listTransactionsToMake, transactionPartObject])
                setKeyInserted('')
                setValueTransaction("")
                console.log(listTransactionsToMake)


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


    function deleteTransaction(indexTransaction){
        const transactionsUpdated = listTransactionsToMake.filter((_, i)=> i !==indexTransaction)
        setListTransactionsToMake(transactionsUpdated)
    }   




    function resquestInfoBasicPix(){
        const inputKeyUser = document.getElementById('keyPix').value
        const keyPix = inputKeyUser.substring(2,inputKeyUser.length)
        const IdBank = inputKeyUser.substring(0,1)
        setKeyPix(keyPix)
        setIdBank(IdBank)
        requestInfoAboutUserPix(keyPix, IdBank)

    }


    const [keyInserted, setKeyInserted] = useState('')
    function setTheKey(event){
        let keyCaptured = event.target.value
        setKeyInserted(keyCaptured)
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
                    <input type="text" placeholder="Key Pix" value={keyInserted} onChange={setTheKey} id="keyPix"></input>
                    <input type="text" placeholder="Value" id="value" value={valueTransaction} onChange={selectedOnlyNumber}></input>
                    <button onClick={resquestInfoBasicPix}>add operation</button>
                </div>
                <div className={styles.operationsOfPacketTransactionsArea}>
                    <div className={styles.textExplainCampsArea}>
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
                            <h1>
                                Name Receiver:
                            </h1>
                        </div>
                        
                    </div>
                    <ul>
                        {listTransactionsToMake.map((transactionPart, index) =>
                            <li>
                                <CardInfoTransactionForMakeInPacket transactionInfo={transactionPart} selfIndex={index}  removeTransaction = {deleteTransaction} />
                            </li>
                        )}
                        
                    </ul>
                </div>
                
                <button className={styles.buttonMakePacketTransaction}>Make Transaction</button>
            </div>
        </>
    )
}

export default CardPacketTransactions