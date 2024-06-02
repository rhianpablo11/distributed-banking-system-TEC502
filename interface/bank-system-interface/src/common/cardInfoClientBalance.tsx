import styles from "../style_modules/commonStyles.module.css"

function CardInfoClientBalance(){

    return (
        <>
            <div className={styles.infoClientBalanceBlock}>
                <h4>Balance</h4>
                <div className={styles.infoClientsBalanceValuesCards}>
                    <div className={styles.infoClientValueCard}>
                        <h5>Total Assets:</h5>
                        <h4><p>US$</p> 5,000.00</h4> 
                    </div>
                    <div className={styles.infoClientValueCard}>
                        <h5>Available:</h5>
                        <h4><p>US$</p> 5,000.00</h4> 
                    </div>
                    <div className={styles.infoClientValueCard}>
                        <h5>Blocked:</h5>
                        <h4><p>US$</p> 10,000.00</h4> 
                    </div>
                </div>
            </div>
        </>
    )
}

export default CardInfoClientBalance