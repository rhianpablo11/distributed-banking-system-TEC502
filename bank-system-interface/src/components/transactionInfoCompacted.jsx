import propsTypes from 'prop-types'

function TransactionInfoCompacted(props){

    return(
        <>
            <div>
                {props.value}
            </div>
        </>
    )
}

TransactionInfoCompacted.propsTypes ={
    value: propsTypes.number,
    date_transaction: propsTypes.object,
    concluded: propsTypes.string,
    name_source: propsTypes.string,
    type_transaction: propsTypes.string
}

TransactionInfoCompacted.defaultProps = {
    value: null,
    date_transaction: null,
    concluded: null,
    name_source: null,
    type_transaction: null
}


export default TransactionInfoCompacted