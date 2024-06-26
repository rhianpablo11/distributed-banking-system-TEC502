import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'
import { useEffect, useState } from "react"

function CardInfoTransactionForMakeInPacket(props){
    const [value, setValue] = useState(props.transactionInfo.value)

    function formatCurrency(value) {
        const parts = value.toFixed(2).split('.');
        const integerPart = parts[0];
        const decimalPart = parts[1];
        const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return formattedIntegerPart+","+decimalPart;
    }

    useEffect(()=>{
        setValue(formatCurrency(parseFloat(props.transactionInfo.value)))
    },)



    const [clicked, setClicked] = useState(true)
    const setTransaction = (e) =>{
        if(clicked){
            props.removeTransaction(props.selfIndex)
            setClicked(false)
        } else{
            setClicked(true)
        }
        
    }

    return(
        <>

            <div className={styles.cardAboutTransactionMountedGeral}>
                <div className={styles.infoOperationArea}>
                    <h1 style={{'font-weight': '600', 'font-size': '1.8rem', 'padding': '3px'}}>
                        {props.transactionInfo.bankSource}
                    </h1>
                    <h2>bank</h2>
                </div>
                <div className={styles.infoOperationArea}>
                    <h1 >{props.transactionInfo.keyPix}</h1>
                </div>
                <div className={styles.infoOperationArea}>
                    <h1>US$ {value}</h1>
                </div>
                <div className={styles.infoOperationArea}>
                    <h1>{props.transactionInfo.nameReceptor}</h1>
                </div>
                <div className={styles.buttonRemoveTransaction}>
                    <button onClick={setTransaction}>
                        <h1>
                            -
                        </h1>
                    </button>
                </div>
            </div>
            
        </>
    )
}


CardInfoTransactionForMakeInPacket.propsTypes = {
    transactionInfo: propsTypes.object,
}

CardInfoTransactionForMakeInPacket.defaultProps = {
    transactionInfo: {
        'bankSource':"Eleven",
        'keyPix':"undefined",
        'value':"undefined",
        'nameReceptor':"undefined"
    }
}

export default CardInfoTransactionForMakeInPacket