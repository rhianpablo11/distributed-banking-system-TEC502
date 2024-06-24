import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'



function CardAccountInfo(props){
    
    const agency = localStorage.getItem('ipBank')

    return(
        <>
            <div className={styles.accountInfoGeral}>
                <h1>
                    Account Info
                </h1>
                <div className={styles.accountData}>
                    <h6>Ag: </h6>{agency}
                </div>
                <div className={styles.accountData}>
                    <h6>Iban: </h6> {props.accountNumber}
                </div>
               
            </div>
        </>
    )
}

CardAccountInfo.propsTypes = {
    accountNumber: propsTypes.string
}

CardAccountInfo.defaultProps = {
    accountNumber: "0000"
}



export default CardAccountInfo