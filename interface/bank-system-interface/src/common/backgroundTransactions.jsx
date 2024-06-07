import { useNavigate } from "react-router-dom"
import styles from "../style_modules/commonStyles.module.css"
import { useState } from "react"
import NavBarInternal from "./navBarInternal"
import CardHelloUser from "./cardHelloUser"
import CardAccountInfo from "./cardAccountInfo"
import CardInfoClientBalance from "./cardInfoClientBalance"
import CardPacketTransactions from "./cardPacketTransactions"

function BackgroundTransactions(){
    const navigate = useNavigate()


    return (
        <>
            <div className={styles.generalPart}>
                <div>
                    <NavBarInternal />
                </div>
                <div className={styles.divGeral}>
                    <div className={styles.centralParteDashboard}>
                        <div className={styles.cardRightTransactionsPage}>
                            <div style={{'margin-bottom': '15px'}}>
                                <CardHelloUser/>
                            </div>
                            <div style={{'margin-bottom': '15px'}}>
                                <CardAccountInfo />
                            </div>
                            <CardInfoClientBalance />
                        </div>
                        <div className={styles.cardsLeftTransactionPage}>
                            <CardPacketTransactions />
                        </div>
                    </div>
                    
                </div>
                
            </div>
            

        </>
    )
}

export default BackgroundTransactions