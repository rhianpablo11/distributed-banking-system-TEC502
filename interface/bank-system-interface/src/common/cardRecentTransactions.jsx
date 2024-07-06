import { useEffect, useState } from "react"
import styles from "../style_modules/commonStyles.module.css"
import CardInfoTransaction from "./cardInfoTransaction"
import propsTypes from 'prop-types'
import CardTransactionInfoDetailed from "./cardTransactionInfoDetailed"

function CardRecentTransactions(props) {
    const [transactions, setTransactions] = useState([])
    useEffect(()=>{
        setTransactions(props.transactions)
    },)

    const [openModalTransaction, setOpenModalTransaction] = useState(false)
    const [transactionToExpand,setTransactionToExpand] = useState()
    return(
        <>
            <div className={styles.recentsTransactionsBlock}>
                <h4>Recent Transactions</h4>
                <div className={styles.listTransactions}>
                    <ul>
                        {transactions.map((transaction) =>

                            <li>
                                <CardInfoTransaction onClick={()=>{setOpenModalTransaction(true)}} transaction={transaction} />
                            </li>)}
                    </ul>
                </div>
                
            </div>
            <CardTransactionInfoDetailed isOpen={openModalTransaction} />
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