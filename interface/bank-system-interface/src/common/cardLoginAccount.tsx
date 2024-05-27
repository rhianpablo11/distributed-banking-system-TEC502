import styles from "../style_modules/commonStyles.module.css"
import LogoBank from "./logoBank"

function CardLoginAccount(){

    return(
        <>
            <div className={styles.createAccountBase}>
                <div className={styles.logoBankLogin}>
                    <LogoBank />
                </div>
                <div className={styles.inputsAreaLogin}>
                    <input className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister"></input>
                    <input className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister"></input>
                </div>
                <button className={styles.buttonPreLogin} >
                    Login
                </button>
            </div>        
            <dialog>
                <p>apresentar a info que nao tem todos os campos preenchidos</p>
            </dialog>
        </>
    )
}

export default CardLoginAccount