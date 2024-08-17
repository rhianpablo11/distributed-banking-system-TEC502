import propsTypes from 'prop-types'

function Specific_balance_info(props){

    return(
        <>
        
        </>
    )
}

Specific_balance_info.propsTypes = {
    type_balance: propsTypes.string,
    value: propsTypes.number
}

Specific_balance_info.defaultProps = {
    type_balance: null,
    value: null
}

export default Specific_balance_info