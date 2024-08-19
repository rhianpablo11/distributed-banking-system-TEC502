import { useParams } from "react-router-dom"
import styles from "../style_modules/commonStyles.module.css"
import { useState, useEffect } from "react"
import NavBarInternal from "./navBarInternal"
import CardHelloUser from "./cardHelloUser"
import CardAccountInfo from "./cardAccountInfo"
import CardInfoClientBalance from "./cardInfoClientBalance"
import CardPacketTransactions from "./cardPacketTransactions"

function BackgroundTransactions(){
    const {nameBank, accountNumber} =useParams()
    const [userData, setUserData] = useState({
        'name1': undefined,
        'cpfCNPJ1': undefined,
        'balance': undefined,
        'blockedBalance': undefined,
        'accountNumber': undefined,
        'transactions': undefined
    })
    const addressBank = localStorage.getItem(nameBank)

    //requisitar os dados daquele user
    useEffect(() =>{
        const requestUser = async () => {
            try {
                const url =addressBank+"/account/data/"+accountNumber
                
                const response = await fetch(url, {
                    method: 'GET'
                })
                
                if (response.ok) {
                    const result = await response.json();
                    
                    // finalizar a apresentação do loading
                    setUserData(result)
                    
                } else {
                    // Caso a resposta não esteja ok, lança apresentação de senha incorreta
                    throw new Error('Network response was not ok');
                }
            } catch (error) {
              //indicar que ocorreu um erro
              //setNotBankConnection(true);
            }
        };
        
        requestUser()
        
        const interval = setInterval(requestUser, 1000)
        return () => clearInterval(interval)

    },[])

    console.log(userData)

    

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
                                <CardHelloUser nameUser ={userData.name1}  />
                            </div>
                            <div style={{'margin-bottom': '15px'}}>
                                <CardAccountInfo  accountNumber={userData.accountNumber} />
                            </div>
                            <CardInfoClientBalance  balance={userData.balance} blockedBalance={userData.blockedBalance}  />
                        </div>
                        <div className={styles.cardsLeftTransactionPage}>
                            <CardPacketTransactions cpfCNPJ_user={userData.cpfCNPJ1}  listBanksAccount = {userData.banksList}  />
                        </div>
                    </div>
                    
                </div>
                
            </div>
            

        </>
    )
}

export default BackgroundTransactions