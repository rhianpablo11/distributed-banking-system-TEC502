import propsTypes from 'prop-types'

function LogoBank(props){

    return (
        <>
            <div>
                <h1>{props.nameBank}</h1>
                <h3>bank</h3>
            </div>
        </>
    )
}

LogoBank.propsTypes = {
    nameBank: propsTypes.string
}

LogoBank.defaultProps = {
    nameBank: null
}

export default LogoBank