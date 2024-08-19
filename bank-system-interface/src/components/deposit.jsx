import propsTypes from 'prop-types'
import { useState } from 'react'
import Loading from './loading'
import Error from './error'
import { get_address_bank_selected } from '../utils/constants'


function Deposit(props){
    const [methodDeposit, setMethodDeposit] = useState('')
    const [valueDeposit, setValueDeposit] = useState(0)
    const [handleClickButton, setHandleClickButton] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(false)

    const qrCodeElement = <div>
                            qrCode image
                        </div>


    const selectOnlyNumber = (event) => {
        let valueCaptured = event.target.value.replace(/[^0-9.]/g, '')
        const partsValue = valueCaptured.split('.')

        if (partsValue[0]) {
            partsValue[0] = partsValue[0].replace(/^0+(?!$)/, '');
        }

        if (partsValue.length === 2) {
            partsValue[1] = partsValue[1].substring(0, 2);
        }

        valueCaptured = partsValue.join('.')
        setValueDeposit(valueCaptured)
        
    }



    const markOptionDepositSelected = (event) =>{
        const optionMarked = event.target.value
        setHandleClickButton(!handleClickButton)
        if(handleClickButton){
            setMethodDeposit(optionMarked)
        } else{
            setMethodDeposit(null)
        }
    }


    const sendRequestDeposit = async () => {
        if(valueDeposit > 0){
            try{
                const urlCommunicate = get_address_bank_selected()+'/account/deposit/'+parseFloat(valueDeposit).toFixed(2)
                setIsLoading(true)
                const response = await fetch(urlCommunicate, {
                    method: 'POST'
                })

                if(response.ok){
                    setIsLoading(false)
                } else{
                    setIsLoading(false)
                    setIsError(true)
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
                <h1>Deposit</h1>
                <input onChange={selectOnlyNumber} value={valueDeposit} placeholder='Value to deposit' type='text'></input>
                <div>
                    <button onClick={markOptionDepositSelected} >
                        money
                    </button>
                    <button onClick={markOptionDepositSelected} >
                        bank slip
                    </button>
                    <button onClick={markOptionDepositSelected}>
                        qr
                    </button>
                </div>
                {methodDeposit == 'qr code' ? qrCodeElement : null}
                <button onClick={sendRequestDeposit}>
                    Pay
                </button>
                <Loading />
                <Error />
            </div>
        </>
    )
}

Deposit.propsTypes = {
    account_number: propsTypes.number
}

Deposit.defaultProps = {
    account_number: null
}

export default Deposit
