import propsTypes from 'prop-types'
import { useEffect, useState } from 'react'
import Transaction_info_compacted from './transaction_info_compacted'

function Transaction_simple_list(props){
    const [transactions, setTransactions] = useState([])

    useEffect(()=>{
        setTransactions(props.transactionsList)
        //limitar o tamanho dessa lista
    }, [props.transactionsList])

    return (
        <>
            <div>
                Transactions Recent
                <div>
                    <ul>
                        {transactions.map((transaction, index) => (
                            <li key={index}>
                                <Transaction_info_compacted value={transaction.value} date_transaction={transaction.date_transaction} concluded={transaction.concluded} name_source={transaction.name_source} type_transaction={transaction.type_transaction} />
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </>
    )
}

Transaction_simple_list.propsTypes = {
    transactionsList: propsTypes.array
}

Transaction_simple_list.defaultProps = {
    transactionsList: null
}

export default Transaction_simple_list