import { useState } from "react";
import styles from "../style_modules/commonStyles.module.css"
import LogoBank from "./logoBank"


function CardCreateAccount(){
    const createAccount = async ()=>{
        const email = document.getElementById('emailRegister').value;
        const name = document.getElementById('nameRegister').value;
        const telephone = document.getElementById('telephoneRegister').value;
        const cpf = document.getElementById('cpfHoldRegister').value;
        const password = document.getElementById('passwordRegister').value;
        const personalAccount = document.getElementById('emailRegister').value;
        const joinetAccount = document.getElementById('emailRegister').value;
    }

    function verifyFields(){
        console.log('aga')
        const [everyThingOk, setEveryThingOk] = useState(false);
        if(everyThingOk){
            createAccount()
        }else{

        }
    }

    return(
        <>
            <div className={styles.createAccountBase}>
                <div className={styles.logoBankPreLogin}>
                    <LogoBank />
                </div>
                <input className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister"></input>
                <input className={styles.inputPreLogin} type="text" placeholder="Name" id='nameRegister'></input>
                <input className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister'></input>
                <div className={styles.choiceRadioButton}>
                    <h6 className={styles.textInputCheckBox}>Personal Account: </h6>
                    <form>
                        <input className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice"></input>
                        <label for="personalAccountIsTrue">Yes</label>
                        <input className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice"></input>
                        <label for="personalAccountIsFalse">No</label>
                    </form>
                </div>

                <div className={styles.choiceRadioButton}>
                    <h6 className={styles.textInputCheckBox}>Joinet Account: </h6>
                    <form>
                        <input className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice"></input>
                        <label for="personalAccountIsTrue">Yes</label>
                        <input className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice"></input>
                        <label for="personalAccountIsFalse">No</label>
                    </form>
                </div>
                <input className={styles.inputPreLogin} type="text" placeholder="CPF holder" id="cpfHoldRegister"></input>
                <input className={styles.inputPreLogin} type="text" placeholder="Password" id="passwordRegister"></input>
                <input className={styles.inputPreLogin} type="text" placeholder="Confirm Password" id='passwordConfirm'></input>
                <button className={styles.buttonPreLogin} onClick={verifyFields}>
                    Create
                </button>
            </div>        
            <dialog>
                <p>apresentar a info que nao tem todos os campos preenchidos</p>
            </dialog>
        </>
    )
}

export default CardCreateAccount