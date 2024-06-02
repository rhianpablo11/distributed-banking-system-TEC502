import styles from "../style_modules/commonStyles.module.css"

function CardAccountInfo(){

    return(
        <>
            <div className={styles.accountInfoGeral}>
                <h1>
                    Account Info
                </h1>
                <div className={styles.accountData}>
                    <h6>Ag: </h6>172.16.103.10
                </div>
                <div className={styles.accountData}>
                    <h6>Iban: </h6>0001
                </div>
               
            </div>
        </>
    )
}

export default CardAccountInfo