import propsTypes from 'prop-types'
import { useEffect, useState } from 'react'
import { formatCurrency } from '../utils/constants'

function SpecificBalanceInfo(props){
    const [valueFormated, setValueFormated] = useState(0.00)

    useEffect(()=>{
        if(props.value != null){
            setValueFormated(formatCurrency(props.value))
        }
    }, [props.value])

    return(
        <>
            <div>
                <h1>{props.typeBalance}</h1>
                <h5>US$</h5>
                <h2>{valueFormated}</h2>
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