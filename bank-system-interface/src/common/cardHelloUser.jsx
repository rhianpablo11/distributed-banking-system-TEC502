import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'


function CardHelloUser(props){

    return(
        <>
            <div className={styles.cardHelloUserBlock}>
                <h4>Hi,</h4>
                <h1>
                    {props.nameUser}
                </h1>
                <h3>Welcome Back</h3>
            </div>
        </>
    )
}

CardHelloUser.propsTypes = {
    nameUser: propsTypes.string
}

CardHelloUser.defaultProps = {
    nameUser: "Undefined"
}


export default CardHelloUser