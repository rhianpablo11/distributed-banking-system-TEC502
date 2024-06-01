import styles from "../style_modules/commonStyles.module.css"
import NavBarInternal from "./navBarInternal"
import CardHelloUser from "./cardHelloUser"
import CardDepositMoney from "./cardDepositMoney"

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

                        </div>
                        <div className={styles.cardsRight}>

                        </div>
                        
                        
                    </div>
                </div>
            </div>
            
            
        </>
    )
}

export default BackgroundLogged