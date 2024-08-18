import propsTypes from 'prop-types'
import { useEffect, useState } from 'react'
import SpecificBalanceInfo from './specificBalanceInfo'


function BalanceInfo(props){
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
                <SpecificBalanceInfo typeBalance={'Total Assets'} value={totalBalance} />
                <SpecificBalanceInfo typeBalance={'Available'} value={props.balance} />
                <SpecificBalanceInfo typeBalance={'Blocked'} value={props.blockedBalance} />
                {haveCdiInvestiment ? <SpecificBalanceInfo typeBalance={'CDI investiment'} value={props.cdiBalance} /> : null }
                {haveSavingInvestiment ? <SpecificBalanceInfo typeBalance={'Saving investiment'} value={props.savingBalance} /> : null}
            </div>
        </>
    )
}

BalanceInfo.propsTypes = {
    balance: propsTypes.number,
    blockedBalance: propsTypes.number,
    cdiBalance: propsTypes.number,
    savingBalance: propsTypes.number
}

BalanceInfo.defaultProps = {
    balance: 0.00,
    blockedBalance: 0.00,
    cdiBalance: 0.00,
    savingBalance: 0.00
}

export default BalanceInfo