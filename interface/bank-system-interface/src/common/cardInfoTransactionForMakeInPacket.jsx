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
            </div>
        </>
    )
}

export default CardInfoTransactionForMakeInPacket