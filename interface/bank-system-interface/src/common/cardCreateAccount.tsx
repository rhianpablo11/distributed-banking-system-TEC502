import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"
import styles from "../style_modules/commonStyles.module.css"
import LogoBank from "./logoBank"


function CardCreateAccount(){
    const navigate = useNavigate()
    const [everyThingOk, setEveryThingOk] = useState(false);
    const borderNotFillInput ={
        'border': '3px solid #ba1111'
    }

    const [styleCampInput, setStyleCampInput] = useState()
    const [styleCampInputPassword, setStyleCampInputPassword] = useState()

    

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
        const email = document.getElementById('emailRegister').value;
        const name = document.getElementById('nameRegister').value;
        const telephone = document.getElementById('telephoneRegister').value;
        let cpf1=''
        let cpf2 =""
        let name2 =""

        if(personalAccount== "true" && isJoinetAccount== "true"){
            const cpf1 = document.getElementById('cpfHoldRegister').value;
            cpf2 = document.getElementById('cpfHoldRegister2').value;
            name2 = document.getElementById('nameRegister2').value;
        } 
        else if(personalAccount== "true" && isJoinetAccount== "false"){
            cpf1 = document.getElementById('cpfHoldRegister').value;
        } 
        else if(personalAccount== "false"){
            cpf1 = document.getElementById('cpfHoldRegister').value;
        }
        const password = document.getElementById('passwordRegister').value;
        const checkedPassword = document.getElementById('passwordConfirm').value;

        
        if(email =="" || name=="" || telephone == "" || cpf1=="" || password == "" || checkedPassword == ""){
            console.log("algo")
            if(isJoinetAccount== "true"){
                if(cpf2=="" || name2==""){
                    setStyleCampInput(borderNotFillInput)
                    setStyleCampInputPassword(borderNotFillInput)
                }else if(password !=checkedPassword){
                    setStyleCampInput()
                    setStyleCampInputPassword(borderNotFillInput)
                }
                else{
                    setStyleCampInput()
                    setStyleCampInputPassword()
                    //verificar ainda a requisição ao servidor
                    //esse valor apos o logged tem que definir ainda o que sera que vai usar
                    return navigate("/logged/598")
                }
            }else{
                setStyleCampInput(borderNotFillInput)
                setStyleCampInputPassword(borderNotFillInput)
            }
        }else if(password !=checkedPassword){
            setStyleCampInput()
            setStyleCampInputPassword(borderNotFillInput)
        } else{
            setStyleCampInput()
            setStyleCampInputPassword()
            //verificar ainda a requisição ao servidor
            //esse valor apos o logged tem que definir ainda o que sera que vai usar
            return navigate("/logged/598")
        }
    }

    const [valueCpfHolder, setValueCpfHolder] = useState("")
    const [valueCpfHolder2, setValueCpfHolder2] = useState("")
    const [personalAccount, setPersonalAccount] = useState("none")
    const [isJoinetAccount, setJoinetAccount] = useState("none")

    function isPersonalAccount(event){
        console.log(event.target.value)
        setPersonalAccount(event.target.value)
    }

    function isJoinet(event){
        setJoinetAccount(event.target.value)
    }

    function cpfCNPJCamp(event){
        console.log(personalAccount)
        let valueCPF = event.target.value.replace(/\D/g, '')
        if(personalAccount == "true"){
            
            if (valueCPF.length <= 11) {
            
                valueCPF = valueCPF.replace(/(\d{3})(\d)/, '$1.$2');
                valueCPF = valueCPF.replace(/(\d{3})(\d)/, '$1.$2');
                valueCPF = valueCPF.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
              } else {
                valueCPF = valueCPF.substring(0, 11); // Limita o comprimento a 11 dígitos
              }
              
        } else if(personalAccount == "false"){
            console.log("console"+personalAccount)
            if (valueCPF.length <= 14) {
                
                valueCPF = valueCPF.replace(/^(\d{2})(\d)/, '$1.$2');
                valueCPF = valueCPF.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
                valueCPF = valueCPF.replace(/\.(\d{3})(\d)/, '.$1/$2');
                valueCPF = valueCPF.replace(/(\d{4})(\d)/, '$1-$2');
            } else {
                valueCPF = valueCPF.substring(0, 14); // Limita o comprimento a 14 dígitos
            }
        }
        
        setValueCpfHolder(valueCPF)
    }

    function cpfCNPJCamp2(event){
        let valueCPF = event.target.value.replace(/\D/g, '')
        if (valueCPF.length <= 11) {
            
        valueCPF = valueCPF.replace(/(\d{3})(\d)/, '$1.$2');
        valueCPF = valueCPF.replace(/(\d{3})(\d)/, '$1.$2');
        valueCPF = valueCPF.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        } else {
        valueCPF = valueCPF.substring(0, 11); // Limita o comprimento a 11 dígitos
        }
        setValueCpfHolder2(valueCPF)
    }

    if(personalAccount =="none"){
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
                            <input className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                            <label for="personalAccountIsTrue">Yes</label>
                            <input className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                            <label for="personalAccountIsFalse">No</label>
                        </form>
                    </div>
                </div>        
                <dialog>
                    <p>apresentar a info que nao tem todos os campos preenchidos</p>
                </dialog>
            </>
        )
    } else if(personalAccount =="true"){
        if(isJoinetAccount == "none"){
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
                                <input className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                                <label for="personalAccountIsTrue">Yes</label>
                                <input className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                                <label for="personalAccountIsFalse">No</label>
                            </form>
                        </div>
    
                        <div className={styles.choiceRadioButton}>
                            <h6 className={styles.textInputCheckBox}>Joinet Account: </h6>
                            <form>
                                <input className={styles.inputRadiosPreLogin} id="joinetAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isJoinet}></input>
                                <label for="joinetAccountIsTrue">Yes</label>
                                <input className={styles.inputRadiosPreLogin} id="joinetAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isJoinet}></input>
                                <label for="joinetAccountIsFalse">No</label>
                            </form>
                        </div>
    
                    </div>        
                </>
            )
        } else if(isJoinetAccount == "true"){
            return(
                <>
                    <div className={styles.createAccountBase}>
                        <div className={styles.logoBankPreLogin}>
                            <LogoBank />
                        </div>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister"></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name Holder" id='nameRegister'></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister'></input>
                        <div className={styles.choiceRadioButton}>
                            <h6 className={styles.textInputCheckBox}>Personal Account: </h6>
                            <form>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                                <label for="personalAccountIsTrue">Yes</label>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                                <label for="personalAccountIsFalse">No</label>
                            </form>
                        </div>
    
                        <div className={styles.choiceRadioButton}>
                            <h6 className={styles.textInputCheckBox}>Joinet Account: </h6>
                            <form>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="joinetAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isJoinet}></input>
                                <label for="joinetAccountIsTrue">Yes</label>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="joinetAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isJoinet}></input>
                                <label for="joinetAccountIsFalse">No</label>
                            </form>
                        </div>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="CPF holder 1" id="cpfHoldRegister" value={valueCpfHolder} onChange={cpfCNPJCamp}></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name Holder 2" id='nameRegister2'></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="CPF holder 2" id="cpfHoldRegister2" value={valueCpfHolder2} onChange={cpfCNPJCamp2}></input>
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister"></input>
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Confirm Password" id='passwordConfirm'></input>
                        <button className={styles.buttonPreLogin} onClick={verifyFields}>
                            Create
                        </button>
                    </div>        
                    <dialog>
                        <p>apresentar a info que nao tem todos os campos preenchidos</p>
                    </dialog>
                </>
            )
        } else if(isJoinetAccount == "false"){
            return(
                <>
                    <div className={styles.createAccountBase}>
                        <div className={styles.logoBankPreLogin}>
                            <LogoBank />
                        </div>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister"></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name Holder" id='nameRegister'></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister'></input>
                        <div className={styles.choiceRadioButton}>
                            <h6 className={styles.textInputCheckBox}>Personal Account: </h6>
                            <form>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                                <label for="personalAccountIsTrue">Yes</label>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                                <label for="personalAccountIsFalse">No</label>
                            </form>
                        </div>
    
                        <div className={styles.choiceRadioButton}>
                            <h6 className={styles.textInputCheckBox}>Joinet Account: </h6>
                            <form>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="joinetAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isJoinet}></input>
                                <label for="joinetAccountIsTrue">Yes</label>
                                <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="joinetAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isJoinet}></input>
                                <label for="joinetAccountIsFalse">No</label>
                            </form>
                        </div>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="CPF holder" id="cpfHoldRegister" value={valueCpfHolder} onChange={cpfCNPJCamp}></input>
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister"></input>
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Confirm Password" id='passwordConfirm'></input>
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
        
    } else if(personalAccount =="false"){
        return(
            <>
                <div className={styles.createAccountBase}>
                    <div className={styles.logoBankPreLogin}>
                        <LogoBank />
                    </div>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister"></input>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name" id='nameRegister'></input>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister'></input>
                    <div className={styles.choiceRadioButton}>
                        <h6 className={styles.textInputCheckBox}>Personal Account: </h6>
                        <form>
                            <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="personalAccountIsTrue" value="true" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                            <label for="personalAccountIsTrue">Yes</label>
                            <input style={styleCampInput} className={styles.inputRadiosPreLogin} id="personalAccountIsFalse" value="false" type="radio" name="personalAccountChoice" onChange={isPersonalAccount}></input>
                            <label for="personalAccountIsFalse">No</label>
                        </form>
                    </div>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="CNPJ holder" id="cpfHoldRegister" value={valueCpfHolder} onChange={cpfCNPJCamp}></input>
                    <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister"></input>
                    <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Confirm Password" id='passwordConfirm'></input>
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


}

export default CardCreateAccount