import propsTypes from 'prop-types'

function AccountInfos(props){
    
    return (
        <>
            <div>
                <h1>Account Number</h1>
                <div>
                    <h2>{props.account_number}</h2>
                </div>
            </div>
        </>
    )
}

AccountInfos.propsTypes = {
    account_number: propsTypes.number
}


AccountInfos.defaultProps = {
    account_number: null
}


export default AccountInfos