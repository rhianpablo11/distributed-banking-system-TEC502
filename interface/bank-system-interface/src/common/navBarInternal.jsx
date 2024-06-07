import LogoBank from "./logoBank"
import styles from "../style_modules/commonStyles.module.css"
import personIcon from "../assets/person.svg"
import { useNavigate } from "react-router-dom"


function NavBarInternal(){
    const navigate = useNavigate()

    function goTransactions(){
        return navigate("/logged/598/transactions")
    }

    function goDashboard(){
        return navigate("/logged/598")
    }
    

    return(
        <>
            <div className={styles.navBarGeral}>
                <div className={styles.navBarInternal}>
                    <LogoBank />
                    <div className={styles.navBarInternalTexts}>
                        <h4>
                            <a href="#" onClick={goDashboard}>
                                dashboard
                            </a>
                        </h4>
                        <h4>
                            <a href="#">
                                extract
                            </a>
                        </h4>
                        <h4>
                            <a href="#">
                                payments
                            </a>
                        </h4>
                        <h4>
                            <a href="#" onClick={goTransactions}>
                                transfers
                            </a>
                        </h4>
                        
                    </div>
                    <a href="#" className={styles.personIconNavBar}>
                        <img src={personIcon}></img>
                    </a>
                    
                </div>
            </div>
            
        </>
    )
}

export default NavBarInternal