import propsTypes from 'prop-types'

function Error(props){

    return (
        <>
        
        </>
    )
}

Error.propsTypes = {
    is_error: propsTypes.bool
}

Error.defaultProps = {
    is_error: null
}

export default Error