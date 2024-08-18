import propsTypes from 'prop-types'

function Specific_balance_info(props){

    return(
        <>
            <div>
                <h4>{props.typeBalance}</h4>
                <h2>{props.value}</h2>
            </div>
        </>
    )
}

Specific_balance_info.propsTypes = {
    typeBalance: propsTypes.string,
    value: propsTypes.number
}

Specific_balance_info.defaultProps = {
    typeBalance: null,
    value: null
}

export default Specific_balance_info