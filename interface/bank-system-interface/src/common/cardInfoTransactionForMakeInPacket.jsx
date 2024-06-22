import styles from "../style_modules/commonStyles.module.css"

function CardInfoTransactionForMakeInPacket(){
    
    return(
        <>

            <div className={styles.cardAboutTransactionMountedGeral}>
                <div className={styles.infoOperationArea}>
                    <h1 style={{'font-weight': '700', 'font-size': '1.8rem', 'padding': '3px'}}>Eleven Bank</h1>
                </div>
                <div className={styles.infoOperationArea}>
                    <h1 >4?11122233344455</h1>
                </div>
                <div className={styles.infoOperationArea}>
                    <h1>12000.00</h1>
                </div>
                <div className={styles.infoOperationArea}>
                    <h1>Rhian Pablo</h1>
                </div>
                <div className={styles.buttonRemoveTransaction}>
                    <button>
                        <h1>
                            -
                        </h1>
                    </button>
                </div>
            </div>
            
        </>
    )
}

export default CardInfoTransactionForMakeInPacket