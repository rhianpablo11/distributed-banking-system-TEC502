import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"
import styles from "../style_modules/commonStyles.module.css"
import LogoBank from "./logoBank"
import propsTypes from 'prop-types'
import { useParams } from "react-router-dom"
import Loading from "./loading";
import ErrorOperation from "./errorOperation";

function CardCreateAccount(props){
    const navigate = useNavigate()
    const [everyThingOk, setEveryThingOk] = useState(false);
    const {nameBank} =useParams()
    console.log(nameBank)
    const borderNotFillInput ={
        'border': '3px solid #ba1111'
    }
    const cpfError = <>
        <p>CPF inserido é invalido</p>
    </>
    const CNPJError = <>
        <p>CNPJ inserido é invalido</p>
    </>

    const passwordUnequal = <>
            <p>Passwords do not match</p>
        </>

    const passwordLenght = <>
            <p>Passwords it's short</p>
        </>

    const CpfEqual = <>
            <p>CPF cannot be the same</p>
        </>

    const [styleCampInput, setStyleCampInput] = useState()
    const [styleCampInputPassword, setStyleCampInputPassword] = useState()
    const [valueCpfCNPJ1isValid, setValueCpfCNPJ1isInvalid] = useState()
    const [valueCpfCNPJ2isValid, setValueCpfCNPJ2isInvalid] = useState()
    const [mensageErrorAboutCpfCNPJ, setMensageErrorAboutCpfCNPJ] = useState()
    const [passwordIsEqual, setPasswordIsEqual] = useState(true)
    const [cpfIsEqual, setCpfIsEqual] = useState(false)
    const [passwordInInterval, setPasswordInInterval] = useState(true)
    const [email, setEmail] = useState('')
    const [name1, setName1] = useState('')
    const [name2, setName2] = useState('')
    const [telephone, setTelephone] = useState('')
    const [valueCpfHolder, setValueCpfHolder] = useState("")
    const [valueCpfHolder2, setValueCpfHolder2] = useState("")
    const [personalAccount, setPersonalAccount] = useState("none")
    const [isJoinetAccount, setJoinetAccount] = useState("none")
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const addressBank = localStorage.getItem(nameBank)
    const [userData, setUserData] = useState()
    const [isError, setIsError] = useState(false)
    const [errorMensage,setErrorMensage] = useState()
    const closeErrorModal = () => {
        setIsError(false);
    };




    const createAccount = async () => {
        try {
            setLoading(true)
            const url =addressBank+"/operations"
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "operation": "create",
                    "clientCpfCNPJ": valueCpfHolder,
                    "dataOperation": {
                        "name1": name1,
                        "cpfCNPJ1": valueCpfHolder,
                        "name2": name2,
                        "cpfCNPJ2": valueCpfHolder2,
                        "email": email,
                        "password":password,
                        "telephone": telephone,
                        "isFisicAccount": personalAccount,
                        "isJoinetAccount": isJoinetAccount
                    }
                })

            })
            
            
            if (response.ok) {
                const result = await response.json();
                console.log(result)
                // finalizar a apresentação do loading
                setLoading(false);
                setUserData(result)
                console.log('oi')
                console.log(userData)
                console.log("url: "+ "/logged/"+nameBank+"/"+result.accountNumber)

                return navigate("/logged/"+nameBank+"/"+result.accountNumber)
            } else {
                // Caso a resposta não esteja ok, lança apresentação de senha incorreta
                setLoading(false)
                setIsError(true)
                console.log('OI EU')
                const auxTemp = await response.text()
                setErrorMensage(auxTemp)
                throw new Error('Network response was not ok');
            }
        } catch (error) {
          //indicar que ocorreu um erro
          //setNotBankConnection(true);
        } finally {
          // finalizar a apresentação do loading
          setLoading(false);
        }
      };

    

    function verifyFields(){
        const email = document.getElementById('emailRegister').value;
        const name = document.getElementById('nameRegister').value;
        const telephone = document.getElementById('telephoneRegister').value;
        let cpf1=''
        let cpf2 =""
        let name2 =""

        if(personalAccount== "true" && isJoinetAccount== "true"){
            cpf1 = document.getElementById('cpfHoldRegister').value;
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
                } else{
                    setStyleCampInput()
                    setStyleCampInputPassword()
                }
            }
            else{
                setStyleCampInput(borderNotFillInput)
                setStyleCampInputPassword(borderNotFillInput)
            }
        } else if(personalAccount=="true"){
            if(isJoinetAccount== "true"){
                
                if(cpf1.length <14){
                    setMensageErrorAboutCpfCNPJ(cpfError)
                    setValueCpfCNPJ1isInvalid(true)
                } else if(cpf1.length ==14){
                    setValueCpfCNPJ1isInvalid(false)
                }

                if(cpf2.length <14){
                    setMensageErrorAboutCpfCNPJ(cpfError)
                    setValueCpfCNPJ2isInvalid(true)
                } else if(cpf2.length ==14){
                    setValueCpfCNPJ2isInvalid(false)
                } 
                if(cpf1!=cpf2){
                    setCpfIsEqual(false)
                } else{
                    setCpfIsEqual(true)
                }

                if(password.length<8){
                    setPasswordInInterval(false)
                } else{
                    setPasswordInInterval(true)
                }
                if(password !=checkedPassword){
                    setPasswordIsEqual(false)
                    setStyleCampInput()
                    setStyleCampInputPassword(borderNotFillInput)
                } else if(cpf2.length ==14 && cpf1.length ==14 && password ==checkedPassword && cpf1 != cpf2 && password.length>=8){
                    setPasswordIsEqual(true)
                    setStyleCampInput()
                    setStyleCampInputPassword()
                    //verificar ainda a requisição ao servidor
                    //esse valor apos o logged tem que definir ainda o que sera que vai usar
                    
                    return createAccount()
                }
            } else{
                if(cpf1.length <14){
                    setMensageErrorAboutCpfCNPJ(cpfError)
                    setValueCpfCNPJ1isInvalid(true)
                } else if(cpf1.length ==14){
                    setValueCpfCNPJ1isInvalid(false)
                }

                if(password.length<8){
                    setPasswordInInterval(false)
                } else{
                    setPasswordInInterval(true)
                }

                if(password !=checkedPassword){
                    setPasswordIsEqual(false)
                    setStyleCampInput()
                    setStyleCampInputPassword(borderNotFillInput)
                }
                else if(cpf1.length ==14 && password ==checkedPassword && password.length>=8){
                    setPasswordIsEqual(true)
                    setStyleCampInput()
                    setStyleCampInputPassword()
                    //verificar ainda a requisição ao servidor
                    //esse valor apos o logged tem que definir ainda o que sera que vai usar
                    
                    return createAccount()
                }
            }
        } else{
            console.log(cpf1.length)
            console.log(
                "operation =>" +"create",
                "clientCpfCNPJ =>"+ valueCpfHolder,
                "dataOperation =>",
                    "name1 =>"+ name1,
                    "cpfCNPJ1 =>" +valueCpfHolder,
                    "name2 =>" +name2,
                    "cpfCNPJ2 =>"+ valueCpfHolder2,
                    "email =>" +email,
                    "password =>"+password,
                    "telephone =>"+ telephone,
                    "isFisicAccountv"+ personalAccount,
                    "isJoinetAccount =>"+ isJoinetAccount
                )
            if(cpf1.length <18){
                setMensageErrorAboutCpfCNPJ(CNPJError)
                setValueCpfCNPJ1isInvalid(true)
            } else if(cpf1.length ==18){
                setValueCpfCNPJ1isInvalid(false)
            }

            if(password.length<8){
                setPasswordInInterval(false)
            } else{
                setPasswordInInterval(true)
            }

            if(password !=checkedPassword){
                setPasswordIsEqual(false)
                setStyleCampInput()
                setStyleCampInputPassword(borderNotFillInput)
            } else if(password ==checkedPassword && cpf1.length ==18 && password.length>=8){
                setPasswordIsEqual(true)
                setStyleCampInput()
                setStyleCampInputPassword()
                //verificar ainda a requisição ao servidor
                //esse valor apos o logged tem que definir ainda o que sera que vai usar
                return createAccount()
            }
        }
          
    }

    function infosAboutPassword(event){
        const password = event.target.value
        if(password.length<8){
            setStyleCampInputPassword({
                'border': '3px solid #ba1111'
            })
        } else{
            setStyleCampInputPassword({
                'border': '3px solid #008000'
            })
        }

    }

    

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
    console.log(email)
    if(personalAccount =="none"){
        return(
            <>
                <div className={styles.createAccountBase}>
                    <div className={styles.logoBankPreLogin}>
                        <LogoBank nameBank = {nameBank} />
                    </div>
                    <input className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister" value={email} onChange={()=>setEmail(event.target.value)} ></input>
                    <input className={styles.inputPreLogin} type="text" placeholder="Name" id='nameRegister' value={name1} onChange={()=>setName1(event.target.value)} ></input>
                    <input className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister'  value={telephone} onChange={()=>setTelephone(event.target.value)} ></input>
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
                            <LogoBank nameBank = {nameBank} />
                        </div>
                        <input className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister" value={email} onChange={()=>setEmail(event.target.value)} ></input>
                        <input className={styles.inputPreLogin} type="text" placeholder="Name" id='nameRegister' value={name1} onChange={()=>setName1(event.target.value)} ></input>
                        <input className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister' value={telephone} onChange={()=>setTelephone(event.target.value)} ></input>
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
                            <LogoBank nameBank = {nameBank}  />
                        </div>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister" value={email} onChange={()=>setEmail(event.target.value)} ></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name Holder" id='nameRegister' value={name1} onChange={()=>setName1(event.target.value)} ></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister' value={telephone} onChange={()=>setTelephone(event.target.value)} ></input>
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
                        {valueCpfCNPJ1isValid ? mensageErrorAboutCpfCNPJ : <></>}
                        {cpfIsEqual ? CpfEqual : <></>}
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name Holder 2" id='nameRegister2' value={name2} onChange={()=>setName2(event.target.value)} ></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="CPF holder 2" id="cpfHoldRegister2" value={valueCpfHolder2} onChange={cpfCNPJCamp2}></input>
                        {valueCpfCNPJ2isValid ? mensageErrorAboutCpfCNPJ : <></>}
                        {cpfIsEqual ? CpfEqual : <></>}
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister" onChange={infosAboutPassword}></input>
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Confirm Password" id='passwordConfirm'  value={password} onChange={()=>setPassword(event.target.value)} ></input>
                        {passwordIsEqual ? <></> : passwordUnequal}
                        {passwordInInterval ? <></> : passwordLenght}
                        <button className={styles.buttonPreLogin} onClick={verifyFields}>
                            Create
                        </button>
                        
                    </div>        
                    <dialog>
                        <p>apresentar a info que nao tem todos os campos preenchidos</p>
                    </dialog>
                    <Loading isOpen={loading} />
                    <ErrorOperation isOpen={isError} textShow={errorMensage} onClose={closeErrorModal} />
                </>
            )
        } else if(isJoinetAccount == "false"){
            return(
                <>
                    <div className={styles.createAccountBase}>
                        <div className={styles.logoBankPreLogin}>
                            <LogoBank nameBank = {nameBank}  />
                        </div>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister" value={email} onChange={()=>setEmail(event.target.value)} ></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name Holder" id='nameRegister' value={name1} onChange={()=>setName1(event.target.value)} ></input>
                        <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister' value={telephone} onChange={()=>setTelephone(event.target.value)} ></input>
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
                        {valueCpfCNPJ1isValid ? mensageErrorAboutCpfCNPJ : <></>}
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister" onChange={infosAboutPassword}></input>
                        <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Confirm Password" id='passwordConfirm' value={password} onChange={()=>setPassword(event.target.value)} ></input>
                        {passwordIsEqual ? <></> : passwordUnequal}
                        {passwordInInterval ? <></> : passwordLenght}
                        <button className={styles.buttonPreLogin} onClick={verifyFields}>
                            Create
                        </button>
                        
                    </div>        
                    <dialog>
                        <p>apresentar a info que nao tem todos os campos preenchidos</p>
                    </dialog>
                    <Loading isOpen={loading} />
                    <ErrorOperation isOpen={isError} textShow={errorMensage} onClose={closeErrorModal} />
                </>
            )
        }
        
    } else if(personalAccount =="false"){
        return(
            <>
                <div className={styles.createAccountBase}>
                    <div className={styles.logoBankPreLogin}>
                        <LogoBank nameBank = {nameBank} />
                    </div>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Email" id="emailRegister" value={email} onChange={()=>setEmail(event.target.value)} ></input>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Name" id='nameRegister' value={name1} onChange={()=>setName1(event.target.value)} ></input>
                    <input style={styleCampInput} className={styles.inputPreLogin} type="text" placeholder="Telephone" id='telephoneRegister' value={telephone} onChange={()=>setTelephone(event.target.value)} ></input>
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
                    {valueCpfCNPJ1isValid ? mensageErrorAboutCpfCNPJ : <></>}
                    <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Password" id="passwordRegister" onChange={infosAboutPassword}></input>
                    <input style={styleCampInputPassword} className={styles.inputPreLogin} type="password" placeholder="Confirm Password" id='passwordConfirm'  value={password} onChange={()=>setPassword(event.target.value)} ></input>
                    {passwordIsEqual ? <></> : passwordUnequal}
                    {passwordInInterval ? <></> : passwordLenght}
                    <button className={styles.buttonPreLogin} onClick={verifyFields}>
                        Create
                    </button>
                    
                </div>        
                <dialog>
                    <p>apresentar a info que nao tem todos os campos preenchidos</p>
                </dialog>
                <Loading isOpen={loading} />
                <ErrorOperation isOpen={isError} textShow={errorMensage} onClose={closeErrorModal} />
            </>
        )
    }


}


CardCreateAccount.propsTypes = {
    nameBank: propsTypes.string
}

CardCreateAccount.defaultProps = {
    nameBank: "Unified"
}

export default CardCreateAccount