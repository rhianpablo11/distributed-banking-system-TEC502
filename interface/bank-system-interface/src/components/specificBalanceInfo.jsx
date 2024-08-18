import propsTypes from 'prop-types'

function SpecificBalanceInfo(props){

    return(
        <>
            <div>
                <h4>{props.typeBalance}</h4>
                <h2>{props.value}</h2>
            </div>
        </>
    )
}

SpecificBalanceInfo.propsTypes = {
    typeBalance: propsTypes.string,
    value: propsTypes.number
}

SpecificBalanceInfo.defaultProps = {
    typeBalance: null,
    value: null
}

export default SpecificBalanceInfo