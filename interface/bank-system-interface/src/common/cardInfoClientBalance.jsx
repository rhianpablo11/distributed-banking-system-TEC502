import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'
import {useEffect, useState } from "react"

function CardInfoClientBalance(props){

    const [totalBalance, setTotalBalance] = useState(0)
    const [balance, setBalance] = useState(props.balance)
    const [blockedBalance, setBlockedBalance] = useState(props.blockedBalance)
    function formatCurrency(value) {
        const parts = value.toFixed(2).split('.');
        const integerPart = parts[0];
        const decimalPart = parts[1];
        const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return formattedIntegerPart+","+decimalPart;
    }
    




    
    useEffect(()=>{
        function calculateTotalBalance(){
            const balance = parseFloat(props.balance)
            const blockedBalance = parseFloat(props.blockedBalance)
            setTotalBalance(formatCurrency((balance+blockedBalance)))
        }
        calculateTotalBalance()
        setBalance(formatCurrency(parseFloat(props.balance)))
        setBlockedBalance(formatCurrency(parseFloat(props.blockedBalance)))
        

    },)
    

    return (
        <>
            <div className={styles.infoClientBalanceBlock}>
                <h4>Balance</h4>
                <div className={styles.infoClientsBalanceValuesCards}>
                    <div className={styles.infoClientValueCard}>
                        <h5 style={{'padding-right': '10px'}}>Total Assets:</h5>
                        <h4><p>US$</p>{totalBalance}</h4> 
                    </div>
                    <div className={styles.infoClientValueCard}>
                        <h5 style={{'padding-right': '10px'}}>Available:</h5>
                        <h4><p>US$</p> {balance}</h4> 
                    </div>
                    <div className={styles.infoClientValueCard}>
                        <h5 style={{'padding-right': '20px'}}>Blocked:</h5>
                        <h4><p>US$</p> {blockedBalance}</h4> 
                    </div>
                </div>
            </div>
        </>
    )
}

CardInfoClientBalance.propsTypes = {
    balance: propsTypes.string,
    blockedBalance: propsTypes.string
}

CardInfoClientBalance.defaultProps = {
    balance: "0.00",
    blockedBalance:"0.00"
}


export default CardInfoClientBalance