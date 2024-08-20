import propsTypes from 'prop-types'

function FastPix(props){
    
    return (
        <>
            <div>
                <h1>Fast Pix</h1>
                <div>
                    <input></input>
                </div>
            </div>
        </>
    )
}

FastPix.propsTypes = {
    account_number: propsTypes.number
}

FastPix.defaultProps = {
    account_number: null
}

export default FastPix