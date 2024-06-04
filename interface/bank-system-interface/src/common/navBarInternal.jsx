import LogoBank from "./logoBank"
import styles from "../style_modules/commonStyles.module.css"
import personIcon from "../assets/person.svg"

function NavBarInternal(){

    return(
        <>
            <div className={styles.navBarGeral}>
                <div className={styles.navBarInternal}>
                    <LogoBank />
                    <div className={styles.navBarInternalTexts}>
                        <h4>
                            <a href="#">
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
                            <a href="#">
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