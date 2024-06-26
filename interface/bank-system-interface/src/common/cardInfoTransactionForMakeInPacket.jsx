import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'
import { useState } from "react"

function CardInfoTransactionForMakeInPacket(props){

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
                    <h1>US$ {props.transactionInfo.value}</h1>
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