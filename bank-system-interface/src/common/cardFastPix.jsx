import { useState } from "react";
import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'
import Loading from "./loading";
import { useParams } from "react-router-dom"
import ErrorOperation from "./errorOperation";


function CardFastPix(props){
    const {nameBank, accountNumber} =useParams()
    const [cpfOrCNPJ, setCpfCNPJ] = useState("CNPJ")
    const [valueSendPix, setvalueSendPix] = useState("")
    const [clientReceiverFound, setClientReceiverFound ] = useState(false)
    const [clientData, setClientData] = useState({
        'name': undefined,
        'cpfCNPJ1': undefined,
        'bank': undefined
    })
    const styleInputValue = {
        'text-align': 'end',
        'padding-right': '10px'
    }


    const [isError, setIsError] = useState(false)
    const [errorMensage,setErrorMensage] = useState()
    const closeErrorModal = () => {
        setIsError(false);
    };


    const dataAboutKeyPix =<>
                               <div className={styles.fastPixInfoReceiver}>
                                    <div className={styles.fastPixInfoReceiverData}>
                                        <h4>Name: </h4>
                                        <h3>{clientData.name} </h3>
                                    </div>
                                    <div className={styles.fastPixInfoReceiverData}>
                                        <h4>{cpfOrCNPJ}: </h4>
                                        <h3>{clientData.cpfCNPJ1}</h3>
                                    </div>
                                    <div className={styles.fastPixInfoReceiverData}>
                                        <h4>Bank: </h4>
                                        <h3>{clientData.bank} Bank</h3>
                                    </div>
                                </div>
                                <div className={styles.inputArea}>
                                    <div className={styles.inputKeyPix}>
                                        <input className={styles.inputValuePix} placeholder="Value:" type="text" value={valueSendPix} onChange={selectedOnlyNumber}></input>
                                    </div>
                                </div>
                                <button onClick={sendMoneyWithPix}>
                                    Send
                                </button>
                            </>

    const loadingSendMoneyWithPix = <>
                                        <div>
                                            //colocar parada para ficar carregando enquanto manda o Pix
                                            ai se se der erro ja apresenta, ou se nao essa parte de carregamento some
                                        </div>
                                    </>
    

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


    const [IdBank, setIdBank] = useState()
    const [keyPix, setKeyPix] = useState()

    function searchInformationReceiverPix(){
        const inputKeyUser = document.getElementById('keyInserted').value
        const keyPix = inputKeyUser.substring(2,inputKeyUser.length)
        const IdBank = inputKeyUser.substring(0,1)
        setKeyPix(keyPix)
        setIdBank(IdBank)
        console.log(keyPix, IdBank);
        requestInfoAboutUserPix(keyPix, IdBank)
    }

    const [loading, setLoading] = useState(false)
    const addressBank = localStorage.getItem(nameBank)

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
            console.log(response)
            setLoading(true)
            
            if (response.ok) {
                const result = await response.json();
                console.log(result)
                // finalizar a apresentação do loading
                setLoading(false);
                setClientData(result)
                setClientReceiverFound(true)
            } else {
                // Caso a resposta não esteja ok, lança apresentação de senha incorreta
                setLoading(false);
                setClientReceiverFound(false)
                setKeyPixInserted("")
                setIsError(true)
                const auxTemp = await response.text()
                setErrorMensage(auxTemp)
                throw new Error('Network response was not ok');
            }
        } catch (error) {
          //indicar que ocorreu um erro
          //setNotBankConnection(true);
          setKeyPixInserted("")
          setLoading(false)
        } finally {
          // finalizar a apresentação do loading
          setLoading(false);
        }
        
    };

    
    const sendPix = async (keyPix, IdBank, value) => {
        try {
            setLoading(true)
            const url =addressBank+"/operations"
            console.log(url)
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "operation": "sendPix",
                    "clientCpfCNPJ": props.cpfCNPJ_user,
                    "dataOperation": {
                        "value": value,
                        "keyPix": keyPix,
                        "idBank": IdBank,
                        "bankNameReceiver":clientData.bank,
                        "nameReceiver": clientData.name
                    }
                })

            })
            
            
            if (response.ok) {
                const result = await response.json();
                console.log(result)
                // finalizar a apresentação do loading
                setLoading(false)
                setKeyPixInserted("")
                setClientReceiverFound(false)
            } else {
                // Caso a resposta não esteja ok, lança apresentação de senha incorreta
                setLoading(false)
                setKeyPixInserted("")
                setClientReceiverFound(false)
                setIsError(true)
                const auxTemp = await response.text()
                setErrorMensage(auxTemp)
                throw new Error('Network response was not ok');
            }
        } catch (error) {
          //indicar que ocorreu um erro
          //setNotBankConnection(true);
          setKeyPixInserted("")
          setLoading(false)
        } finally {
          // finalizar a apresentação do loading
          setLoading(false);
          setKeyPixInserted("")
          setClientReceiverFound(false)
        }
    };

    
    function sendMoneyWithPix(){
        if(valueSendPix != ''){
            sendPix(keyPix, IdBank, valueSendPix)
        }
    }

 
    const [keyPixInserted, setKeyPixInserted] = useState()

    return (
        <>
            <div className={styles.fastPixBlock}>
                <h1>Fast Pix</h1>
                <div className={styles.inputArea}>
                    <div className={styles.inputKeyPix}>
                        <input placeholder="Key:" type="text" id='keyInserted' value={keyPixInserted} onChange={()=>setKeyPixInserted(event.target.value)}></input>
                    </div>
                </div>
                <button onClick={searchInformationReceiverPix}>
                    Search
                </button>
                {clientReceiverFound ? dataAboutKeyPix : null}
                <Loading isOpen={loading} />
                <ErrorOperation isOpen={isError} textShow={errorMensage} onClose={closeErrorModal} />
            </div>
            
            
        </>
    )
}

CardFastPix.propsTypes = {
    cpfCNPJ_user: propsTypes.string
}

CardFastPix.defaultProps = {
    cpfCNPJ_user: "undefined"
}


export default CardFastPix 