import styles from "../style_modules/commonStyles.module.css"
import NavBarInternal from "./navBarInternal"
import CardHelloUser from "./cardHelloUser"
import CardDepositMoney from "./cardDepositMoney"
import CardAccountInfo from "./cardAccountInfo"
import CardFastPix from "./cardFastPix"
import CardInfoClientBalance from "./cardInfoClientBalance"
import CardRecentTransactions from "./cardRecentTransactions"
import { useParams } from "react-router-dom"
import {useState ,useEffect } from "react"


function  BackgroundLogged(){
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


    return (
        <>  
            <div className={styles.backGround}>
                <NavBarInternal nameBank = {nameBank} />
                <div className={styles.divGeral}>
                    <div className={styles.centralParteDashboard}>
                        <div className={styles.cardsLeft}>
                            <CardHelloUser nameUser ={userData.name1}  />
                            <CardDepositMoney cpfCNPJ_user={userData.cpfCNPJ1} />
                            
                        </div>
                        <div className={styles.cardsCenter}>
                            <CardInfoClientBalance balance={userData.balance} blockedBalance={userData.blockedBalance} />
                            <CardRecentTransactions transactions={userData.transactions} />
                        </div>
                        <div className={styles.cardsRight}>
                            <CardAccountInfo accountNumber={userData.accountNumber} />
                            <CardFastPix cpfCNPJ_user={userData.cpfCNPJ1} />
                        </div>
                    </div>
                </div>
            </div>
            
            
        </>
    )
}

export default BackgroundLogged