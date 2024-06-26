import LogoBank from "./logoBank"
import styles from "../style_modules/commonStyles.module.css"
import personIcon from "../assets/person.svg"
import { useNavigate, useParams } from "react-router-dom"
import logoutIcon from "../assets/logout.svg"
import propsTypes from 'prop-types'

function NavBarInternal(props){
    const navigate = useNavigate()
    const {nameBank, accountNumber} = useParams()
    function goTransactions(){
        return navigate("/logged/"+nameBank+"/"+accountNumber+"/transactions")
    }

    function goDashboard(){
        return navigate("/logged/"+nameBank+"/"+accountNumber)
    }
    
    function goLandingPage(){
        return navigate("/"+nameBank)
    }

    return(
        <>
            <div className={styles.navBarGeral}>
                <div className={styles.navBarInternal}>
                    <div className={styles.navBarLogoArea}>
                        <LogoBank nameBank={nameBank}/>
                    </div>
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
                    <div className={styles.navBarButtons}>
                        <button onClick={goLandingPage}>
                            <img src={logoutIcon}></img>
                        </button>
                        <a href="#" className={styles.personIconNavBar}>
                            <img src={personIcon}></img>
                        </a>
                    </div>
                    
                    
                </div>
            </div>
            
        </>
    )
}


NavBarInternal.propsTypes = {
    nameBank: propsTypes.string
}

NavBarInternal.defaultProps = {
    nameBank: "Unified"
}


export default NavBarInternal