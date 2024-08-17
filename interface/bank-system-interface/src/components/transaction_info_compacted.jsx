import propsTypes from 'prop-types'

function Transaction_info_compacted(props){

    return(
        <>
        
        </>
    )
}

Transaction_info_compacted.propsTypes ={
    value: propsTypes.number,
    date_transaction: propsTypes.object,
    concluded: propsTypes.string,
    name_source: propsTypes.string,
    type_transaction: propsTypes.string
}

Transaction_info_compacted.defaultProps = {
    value: null,
    date_transaction: null,
    concluded: null,
    name_source: null,
    type_transaction: null
}


export default Transaction_info_compacted