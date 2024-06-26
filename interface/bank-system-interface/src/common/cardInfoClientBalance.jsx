import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'
import {useEffect, useState } from "react"

function CardInfoClientBalance(props){

    const [totalBalance, setTotalBalance] = useState(0)

    
        
    
    useEffect(()=>{
        function calculateTotalBalance(){
            const balance = parseFloat(props.balance)
            const blockedBalance = parseFloat(props.blockedBalance)
            setTotalBalance((balance+blockedBalance))
        }
        calculateTotalBalance()
    },)
    

    return (
        <>
            <div className={styles.infoClientBalanceBlock}>
                <h4>Balance</h4>
                <div className={styles.infoClientsBalanceValuesCards}>
                    <div className={styles.infoClientValueCard}>
                        <h5>Total Assets:</h5>
                        <h4><p>US$</p>{totalBalance}</h4> 
                    </div>
                    <div className={styles.infoClientValueCard}>
                        <h5>Available:</h5>
                        <h4><p>US$</p> {props.balance}</h4> 
                    </div>
                    <div className={styles.infoClientValueCard}>
                        <h5>Blocked:</h5>
                        <h4><p>US$</p> {props.blockedBalance}</h4> 
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