import propsTypes from 'prop-types'
import { useEffect, useState } from 'react'
import TransactionInfoCompacted from './transactionInfoCompacted'

function TransactionSimpleList(props){
    const [transactions, setTransactions] = useState([{
        'value': null,
        'date_transaction': null,
        'concluded': null, 
        'name_source': null,
        'type_transaction': null
    }])

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
                                <TransactionInfoCompacted value={transaction.value} date_transaction={transaction.date_transaction} concluded={transaction.concluded} name_source={transaction.name_source} type_transaction={transaction.type_transaction} />
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </>
    )
}

TransactionSimpleList.propsTypes = {
    transactionsList: propsTypes.array
}

TransactionSimpleList.defaultProps = {
    transactionsList: null
}

export default TransactionSimpleList