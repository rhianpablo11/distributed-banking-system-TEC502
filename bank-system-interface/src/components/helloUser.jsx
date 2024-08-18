import propsTypes from 'prop-types'


function HelloUser(props){

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


HelloUser.prototype = {
    name: propsTypes.string
}

HelloUser.defaultProps = {
    name: null
}


export default HelloUser