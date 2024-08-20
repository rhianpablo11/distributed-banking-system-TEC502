import { useState } from "react"
import LogoBank from "./logoBank"
import { useNavigate, useParams } from "react-router-dom"
import { get_address_bank_selected, get_token, save_cookie_token } from "../utils/constants"

function LoginForm(){
    const [accountNumberInserted, setAccountNumberInserted] = useState()
    const [passwordInserted, setPasswordInserted] = useState()
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(false)
    const [errorType, setErrorType] = useState('')
    const {nameBank} = useParams()
    const navigate = useNavigate()
    
    const formatAccountNumber = (event) => {
        let valueCaptured = event.target.value.replace(/\D/g, '');

        //remove zeros at left, this can result in future bugs if account number 00000 exists 
        valueCaptured = valueCaptured.replace(/^0+(?!$)/, '');

        if (valueCaptured.length > 5) {
            valueCaptured = valueCaptured.substring(0, 5);
        }
    
        setAccountNumberInserted(valueCaptured);
    }


    const sendRequestLogin = async () => {
        if(passwordInserted != '' && accountNumberInserted !=''){
            try{
                setIsLoading(true)
                const urlCommunicate = get_address_bank_selected()+'/account/login'
                const response = await fetch(urlCommunicate, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "account_number": parseInt(accountNumberInserted),
                        "password": passwordInserted
                    })
                })
                console.log('kafho'+accountNumberInserted)
                setIsLoading(false)
                if(response.ok){
                    const responseJson = await response.json()
                    save_cookie_token(responseJson['token'])
                    setIsLoading(false)
                    navigate('/Eleven/dashboard-temp')
                } else if(response.status == 406){
                    setErrorType('password')
                } else if(response.status == 404){
                    setErrorType('account')
                }
            } catch(error){
                setIsLoading(false)
                setIsError(true)
            }
        }
    }


    return (
        <>
            <div>
                <LogoBank nameBank={nameBank} />
                <input required type="text" placeholder="Account Number" incorrect={errorType == 'account' ? true : false} value={accountNumberInserted} onChange={formatAccountNumber}></input>
                <input required type="password" placeholder="Password"   incorrect={errorType == 'password' ? true : false} value={passwordInserted} onChange={()=>setPasswordInserted(event.target.value)} ></input>
                <button onClick={sendRequestLogin}>
                    Login
                </button>
            </div>
        </>
    ) 
}

export default LoginForm
