import styles from "../style_modules/commonStyles.module.css"
import CardInfoTransaction from "./cardInfoTransaction"

function CardRecentTransactions() {
    
    return(
        <>
            <div className={styles.recentsTransactionsBlock}>
                <h4>Recent Transactions</h4>
                <div className={styles.listTransactions}>
                    <CardInfoTransaction />
                    <CardInfoTransaction />
                    <CardInfoTransaction />
                    <CardInfoTransaction />
                    <CardInfoTransaction />
                    <CardInfoTransaction />
                </div>
                
            </div>
        </>
    )
}

export default CardRecentTransactions