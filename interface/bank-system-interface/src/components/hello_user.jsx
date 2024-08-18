import propsTypes from 'prop-types'


function Hello_user(props){

    return(
        <>
            <div>
                <h3>Hello,</h3>
                <h2>{props.name}</h2>
                <h3>Welcome back</h3>
            </div>
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