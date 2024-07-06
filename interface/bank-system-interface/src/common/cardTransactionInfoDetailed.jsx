import propsTypes from 'prop-types'
import styles from "../style_modules/commonStyles.module.css"
import { useEffect, useState } from 'react'

function CardTransactionInfoDetailed(props){
    const [transaction, setTransaction] = useState(props.transaction)
    const dateTransactionFormated = new Date(transaction.dateTransaction)
    const teste = Date.UTC(dateTransactionFormated.toLocaleString())
    const [typeTransaction, setTypeTransaction] = useState('')
    const [value, setValue] = useState(props.transaction.value)
    const [transactionError, setTransactionError] = useState(false)
    //se for true é pq saiu, se for false é pq entrou
    const [moneyOutOrReceive, setMoneyOutOrReceive] = useState(false)
   
    function selectTextTransaction(){
        if(transaction.typeTransaction == 'deposit'){
            setMoneyOutOrReceive(false)
            setTypeTransaction('Deposit')
        }
        else if(transaction.typeTransaction =='send Pix'){
            setMoneyOutOrReceive(true)
            setTypeTransaction('Pix send')
        }else if(transaction.typeTransaction =='receive Pix'){
            setMoneyOutOrReceive(false)
            setTypeTransaction('Pix received')
        }

        if(transaction.concluded == true){
            setTransactionError(false)
        } else if(transaction.concluded == "pending"){
            setTransactionError(false)
        } else if(transaction.concluded == "error"){
            setTransactionError(true)
        }

    }

    function formatCurrency(value) {
        const parts = value.toFixed(2).split('.');
        const integerPart = parts[0];
        const decimalPart = parts[1];
        const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return formattedIntegerPart+","+decimalPart;
    }

    useEffect(()=>{
        setTransaction(props.transaction)
        selectTextTransaction()
        setValue(formatCurrency(parseFloat(props.transaction.value)))
    }, [props.transaction])
    
    const [openModal,setOpenModal] = useState(false)
    useEffect(()=>{
        setOpenModal(props.isOpen)
    }, [props.isOpen])
    console.log('klajfklaf')
    if(openModal){
        return (
            <>
                <div className={styles.infoDetailedGeral}>
                    <div className={styles.cardWithDetails}>
                        <div className={styles.titleInfoDetailedGeral}>
                            <h1>
                                Transaction Info
                            </h1>
                            <button onClick={()=>{setOpenModal(false)}}>
                                X
                            </button>
                        </div>
                        <div className={styles.principalInfosAboutTransaction}>
                            <div className={styles.logoAboutTransaction}>
                                {transactionError ? 
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                                            <path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/>
                                        </svg> : moneyOutOrReceive ? 
                                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path fill-rule="evenodd" clip-rule="evenodd" d="M19.2111 2.06722L3.70001 5.94499C1.63843 6.46039 1.38108 9.28612 3.31563 10.1655L8.09467 12.3378C9.07447 12.7831 10.1351 12.944 11.1658 12.8342C11.056 13.8649 11.2168 14.9255 11.6622 15.9053L13.8345 20.6843C14.7139 22.6189 17.5396 22.3615 18.055 20.3L21.9327 4.78886C22.3437 3.14517 20.8548 1.6563 19.2111 2.06722ZM8.92228 10.517C9.85936 10.943 10.9082 10.9755 11.8474 10.6424C12.2024 10.5165 12.5417 10.3383 12.8534 10.1094C12.8968 10.0775 12.9397 10.0446 12.982 10.0108L15.2708 8.17974C15.6351 7.88831 16.1117 8.36491 15.8202 8.7292L13.9892 11.018C13.9553 11.0603 13.9225 11.1032 13.8906 11.1466C13.6617 11.4583 13.4835 11.7976 13.3576 12.1526C13.0244 13.0918 13.057 14.1406 13.4829 15.0777L15.6552 19.8567C15.751 20.0673 16.0586 20.0393 16.1147 19.8149L19.9925 4.30379C20.0372 4.12485 19.8751 3.96277 19.6962 4.00751L4.18509 7.88528C3.96065 7.94138 3.93264 8.249 4.14324 8.34473L8.92228 10.517Z" />
                                        </svg> :
                                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <g clip-rule="evenodd" fill-rule="evenodd">
                                                <path d="m5.00004 14.9968c.41421 0 .75.3358.75.75v2.2532c0 .1381.11193.25.25.25h11.99996c.1381 0 .25-.1119.25-.25v-2.2532c0-.4142.3358-.75.75-.75.4143 0 .75.3358.75.75v2.2532c0 .9665-.7835 1.75-1.75 1.75h-11.99996c-.9665 0-1.75-.7835-1.75-1.75v-2.2532c0-.4142.33579-.75.75-.75z"/>
                                                <path d="m12.2023 4.25c.4142 0 .75.33579.75.75v8.0856c0 .4142-.3358.75-.75.75s-.75-.3358-.75-.75v-8.0856c0-.41421.3358-.75.75-.75z"/>
                                                <path d="m8.32184 10.6256c.28946-.2963.76431-.3019 1.06059-.0124l2.81967 2.7548 2.8198-2.7548c.2962-.2895.7711-.2839 1.0605.0124.2895.2962.284.7711-.0123 1.0605l-3.3438 3.2669c-.2915.2847-.7569.2847-1.0483 0l-3.3438-3.2669c-.29629-.2894-.30182-.7643-.01236-1.0605z"/>
                                            </g>
                                        </svg>
                                        }
                            </div>
                            <div className={styles.textsPrincipalAboutTransaction}>
                                <div style={{"display": "flex", "align-items": 'baseline'}}>
                                    <h1>
                                        Status:
                                    </h1>
                                    <h2>
                                        {transaction.concluded}
                                    </h2>
                                </div>
                                <div style={{"display": "flex", "align-items": 'baseline'}}>
                                    <h1>
                                        Value:
                                    </h1>
                                    <h2>
                                        {value}
                                    </h2>
                                </div>
                                <div style={{"display": "flex", "align-items": 'baseline'}}>
                                    <h1>
                                        Date:
                                    </h1>
                                    <h2>
                                        {dateTransactionFormated.toLocaleString()}
                                    </h2>
                                </div>
                                <div style={{"display": "flex", "align-items": 'baseline'}}>
                                    <h1>
                                        ID Transaction:
                                    </h1>
                                    <h2 style={{'flexDirection': "row"}}>
                                        {transaction.idTransaction}
                                    </h2>
                                </div>
                                    
                            </div>
                        </div>
                        <div className={styles.infosAboutPersonsEnvolved}>
                            <h1 style={{"margin-top":"10px"}}>
                                Sender:
                            </h1>
                            <h2>
                                {transaction.source}
                            </h2>
                            <h1>
                                Bank Sender:
                            </h1>
                            <h2>
                                {transaction.bankSource}
                            </h2>
                            <h1>
                                Receiver:
                            </h1>
                            <h2>
                                {transaction.receptor}
                            </h2>
                            <h1>
                                Bank Receiver:
                            </h1>
                            <h2>
                                {transaction.bankReceptor}
                            </h2>
                        </div>
                    </div>
                    
                </div>
            </>
        )
    } else{
        return null
    }
    
}

CardTransactionInfoDetailed.propsTypes = {
    transaction: propsTypes.object,
    isOpen: propsTypes.bool
}

CardTransactionInfoDetailed.defaultProps = {
    transaction: {
        'source': undefined,
        'receptor':undefined,
        'value': undefined,
        'dateTransaction': undefined,
        'concluded': undefined,
        'typeTransaction': undefined,
        'bankSource': undefined,
        'bankReceptor': undefined,
        "idTransaction": undefined
    },
    isOpen: false
}



export default CardTransactionInfoDetailed