import LogoBank from "./logoBank"
import styles from "../style_modules/commonStyles.module.css"
import personIcon from "../assets/person.svg"
import { useNavigate, useParams } from "react-router-dom"
import logoutIcon from "../assets/logout.svg"
import propsTypes from 'prop-types'
import { useEffect } from "react"

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
    useEffect(()=>{
        if(nameBank == "Eleven"){
            document.documentElement.style.setProperty('--background-color', "#000000");
            document.documentElement.style.setProperty('--background-body-color', "#000000");
            document.documentElement.style.setProperty('--block-color', "#171717");
            document.documentElement.style.setProperty('--secondary-block-color', "#444444");
            document.documentElement.style.setProperty('--button-color', "#252525");
            document.documentElement.style.setProperty('--button-hover-color', "#000000");
            document.documentElement.style.setProperty('--input-color', "#444444");
            document.documentElement.style.setProperty('--input-secondary-color', "#1f1e1e");
            document.documentElement.style.setProperty('--letter-color', "#EEEEEE");
            document.documentElement.style.setProperty('--letter-placeholder-color', "#a0a0a0");
            document.documentElement.style.setProperty('--letter-hover-color', "#444444");
        } else if (nameBank== "Titanium"){
            document.documentElement.style.setProperty('--background-color', "#000000");
            document.documentElement.style.setProperty('--background-body-color', "#040911");
            document.documentElement.style.setProperty('--block-color', "#222831");
            document.documentElement.style.setProperty('--secondary-block-color', "#393E46");
            document.documentElement.style.setProperty('--button-color', "#FD7014");
            document.documentElement.style.setProperty('--button-hover-color', "#742f01");
            document.documentElement.style.setProperty('--input-color', "#555F70");
            document.documentElement.style.setProperty('--input-secondary-color', "#282d36");
            document.documentElement.style.setProperty('--letter-color', "#EEEEEE");
            document.documentElement.style.setProperty('--letter-placeholder-color', "#bbbbbb");
            document.documentElement.style.setProperty('--letter-hover-color', "#393E46");
        } else if (nameBank== "Secret"){
            document.documentElement.style.setProperty('--background-color', "#000000");
            document.documentElement.style.setProperty('--background-body-color', "#DDDDDD");
            document.documentElement.style.setProperty('--block-color', "#F6F6F6");
            document.documentElement.style.setProperty('--secondary-block-color', "#e0e0e0");
            document.documentElement.style.setProperty('--button-color', "#FFCB74");
            document.documentElement.style.setProperty('--button-hover-color', "#e49204");
            document.documentElement.style.setProperty('--input-color', "#e0e0e0");
            document.documentElement.style.setProperty('--input-secondary-color', "#c4c4c4");
            document.documentElement.style.setProperty('--letter-color', "#111111");
            document.documentElement.style.setProperty('--letter-placeholder-color', "#2c2c2c");
            document.documentElement.style.setProperty('--letter-hover-color', "#FFCB74");
        } else if (nameBank== "Formula"){
            document.documentElement.style.setProperty('--background-color', "#000000");
            document.documentElement.style.setProperty('--background-body-color', "#041b19");
            document.documentElement.style.setProperty('--block-color', "#115852");
            document.documentElement.style.setProperty('--secondary-block-color', "#237e76");
            document.documentElement.style.setProperty('--button-color', "#064b45");
            document.documentElement.style.setProperty('--button-hover-color', "#032523");
            document.documentElement.style.setProperty('--input-color', "#237e76");
            document.documentElement.style.setProperty('--input-secondary-color', "#3ca99f");
            document.documentElement.style.setProperty('--letter-color', "#ffffffee");
            document.documentElement.style.setProperty('--letter-placeholder-color', "#f7f7f7");
            document.documentElement.style.setProperty('--letter-hover-color', "#0a3632");
        } else if (nameBank== "Automobili"){
            document.documentElement.style.setProperty('--background-color', "#000000");
            document.documentElement.style.setProperty('--background-body-color', "#cec5b0");
            document.documentElement.style.setProperty('--block-color', "#f2e9d4");
            document.documentElement.style.setProperty('--secondary-block-color', "#fbf9e7");
            document.documentElement.style.setProperty('--button-color', "#a9a394");
            document.documentElement.style.setProperty('--button-hover-color', "#33312b");
            document.documentElement.style.setProperty('--input-color', "#fbf9e7");
            document.documentElement.style.setProperty('--input-secondary-color', "#f5f2db");
            document.documentElement.style.setProperty('--letter-color', "#4e4e4e");
            document.documentElement.style.setProperty('--letter-placeholder-color', "#85635c");
            document.documentElement.style.setProperty('--letter-hover-color', "#a9a394");
            document.documentElement.style.setProperty('--letter-hover-color', "#00000");
        }
    },)
    



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