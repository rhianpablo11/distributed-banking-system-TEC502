import propsTypes from 'prop-types'


function Hello_user(props){

    return(
        <>
        </>
    )
}


Hello_user.prototype = {
    name: propsTypes.string
}

Hello_user.defaultProps = {
    name: null
}


export default Hello_user