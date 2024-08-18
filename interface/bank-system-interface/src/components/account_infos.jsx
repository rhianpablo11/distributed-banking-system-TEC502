import propsTypes from 'prop-types'

function Account_infos(props){
    
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

Account_infos.propsTypes = {
    account_number: propsTypes.number
}


Account_infos.defaultProps = {
    account_number: null
}


export default Account_infos