import propsTypes from 'prop-types'
import { useEffect, useState } from 'react'
import Specific_balance_info from './specific_balance_info'


function Balance_info(props){
    const [haveCdiInvestiment, setHaveCdiInvestiment] = useState(false)
    const [haveSavingInvestiment, setHaveSavingInvestiment] = useState(false)
    const [totalBalance, setTotalBalance] = useState(0)

    useEffect(()=>{
        const verifyBalanceInvestiments = () => {
            if(props.cdiBalance > 0){
                setHaveCdiInvestiment(true)
            } else{
                setHaveCdiInvestiment(false)
            }

            if(props.savingBalance > 0){
                setHaveSavingInvestiment(true)
            } else{
                setHaveSavingInvestiment(false)
            }
        }

        verifyBalanceInvestiments()

    }, [props.cdiBalance, props.savingBalance])


    useEffect(()=>{
        const calculateTotalBalance = () =>{
            setTotalBalance(props.balance + props.blockedBalance + props.cdiBalance + props.savingBalance) 
        }

        calculateTotalBalance()

    }, [props.balance, props.blockedBalance])


    

    return (
        <>
            <div>
                Balance account info
                <Specific_balance_info typeBalance={'Total Assets'} value={totalBalance} />
                <Specific_balance_info typeBalance={'Available'} value={props.balance} />
                <Specific_balance_info typeBalance={'Blocked'} value={props.blockedBalance} />
                {haveCdiInvestiment ? <Specific_balance_info typeBalance={'CDI investiment'} value={props.cdiBalance} /> : null }
                {haveSavingInvestiment ? <Specific_balance_info typeBalance={'Saving investiment'} value={props.savingBalance} /> : null}
            </div>
        </>
    )
}

Balance_info.propsTypes = {
    balance: propsTypes.number,
    blockedBalance: propsTypes.number,
    cdiBalance: propsTypes.number,
    savingBalance: propsTypes.number
}

Balance_info.defaultProps = {
    balance: 0.00,
    blockedBalance: 0.00,
    cdiBalance: 0.00,
    savingBalance: 0.00
}

export default Balance_info