import styles from "../style_modules/commonStyles.module.css"
import NavBarInternal from "./navBarInternal"
import CardHelloUser from "./cardHelloUser"
import CardDepositMoney from "./cardDepositMoney"
import CardAccountInfo from "./cardAccountInfo"
import CardFastPix from "./cardFastPix"
import CardInfoClientBalance from "./cardInfoClientBalance"
import CardRecentTransactions from "./cardRecentTransactions"

function  BackgroundLogged(){

    

    return (
        <>  
            <div className={styles.backGround}>
                <NavBarInternal />
                <div className={styles.divGeral}>
                    <div className={styles.centralParteDashboard}>
                        <div className={styles.cardsLeft}>
                            <CardHelloUser />
                            <CardDepositMoney />
                            
                        </div>
                        <div className={styles.cardsCenter}>
                            <CardInfoClientBalance />
                            <CardRecentTransactions />
                        </div>
                        <div className={styles.cardsRight}>
                            <CardAccountInfo />
                            <CardFastPix />
                        </div>
                    </div>
                </div>
            </div>
            
            
        </>
    )
}

export default BackgroundLogged