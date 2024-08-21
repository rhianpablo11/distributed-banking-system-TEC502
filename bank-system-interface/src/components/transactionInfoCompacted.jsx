import propsTypes from 'prop-types'
import { useEffect, useState } from 'react'

function TransactionInfoCompacted(props){
    const [typeTransaction, setTypeTransaction] = useState('')
    const [moneyDirection, setMoneyDirection] = useState('')
    const [symbolRender, setSymbolRender] = useState(<></>)
    const dateTransactionObject = new Date(props.date_transaction)


    const formatCurrency = (value) => {
        const parts = value.toFixed(2).split('.');
        const integerPart = parts[0];
        const decimalPart = parts[1];
        const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return formattedIntegerPart+","+decimalPart;
    }


    const selectSymbolOperation = () => {
        if(props.type_transaction == 'send_pix' || props.type_transaction == 'send_ted' ){
            //saiu dinheiro da conta externamente
            setMoneyDirection('To')
            return <svg>

                    </svg>
        } else if(props.type_transaction == 'ted' || props.type_transaction == 'pix' || props.type_transaction == 'deposit' ){
            //chegou dinheiro externo
            setMoneyDirection('From')
            return <svg>

                    </svg>
        } else if(props.type_transaction == 'earned_investiment_saving' || props.type_transaction == 'earned_investiment_cdi' ){
            //chegou dinheiro interno - investimento
            setMoneyDirection('From')
            return <svg>

                    </svg>
        } else if(props.type_transaction == 'withdraw_cdi' || props.type_transaction == 'withdraw_saving'){
            //saiu dinheiro interno - tirou do investimento
            setMoneyDirection('To')
            return <svg>

                    </svg>
        } else if(props.type_transaction == 'investiment_saving' || props.type_transaction == 'investiment_cdi' ){
            //saiu dinheiro interno - investiu
            setMoneyDirection('To')
            return <svg>

                    </svg>
        }
    }

    useEffect(()=>{
        setSymbolRender(selectSymbolOperation())
    }, [])

    return(
        <>
            <div>
                <div>
                    {symbolRender}
                </div>
                <div>
                    <h2>{typeTransaction}</h2>
                    <h2>{dateTransactionObject.toLocaleDateString()}</h2>
                </div>
                <div>
                    <h2>{moneyDirection}</h2>
                    <h2>{moneyDirection == 'To' ? props.name_receiver : props.name_source}</h2>
                </div>
                <div>
                    <h4>US$</h4>
                    <h2>{props.value != null ? formatCurrency(props.value) : null}</h2>
                </div>
            </div>
        </>
    )
}

TransactionInfoCompacted.propsTypes ={
    value: propsTypes.number,
    date_transaction: propsTypes.object,
    concluded: propsTypes.string,
    name_source: propsTypes.string,
    type_transaction: propsTypes.string,
    name_receiver: propsTypes.string
}

TransactionInfoCompacted.defaultProps = {
    value: null,
    date_transaction: null,
    concluded: null,
    name_source: null,
    name_receiver: null,
    type_transaction: null
}


export default TransactionInfoCompacted