import styles from "../style_modules/commonStyles.module.css"
import CardInfoTransaction from "./cardInfoTransaction"
import propsTypes from 'prop-types'

function CardRecentTransactions(props) {
    
    return(
        <>
            <div className={styles.recentsTransactionsBlock}>
                <h4>Recent Transactions</h4>
                <div className={styles.listTransactions}>
                    <ul>
                        {props.transactions.map((transaction) =>

                            <li>
                                <CardInfoTransaction transaction={transaction} />
                            </li>)}
                    </ul>
                </div>
                
            </div>
        </>
    )
}

CardRecentTransactions.propsTypes = {
    transactions: propsTypes.array
}

CardRecentTransactions.defaultProps = {
    transactions: []
}


export default CardRecentTransactions