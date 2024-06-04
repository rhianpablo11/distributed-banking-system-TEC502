import CardCreateAccount from "../common/cardCreateAccount"
import CardLoginAccount from "../common/cardLoginAccount"
import styles from "./elevenBank.module.css"
import { useParams } from "react-router-dom"

function ElevenBankBackgroundLogin(){

    const {type_sing_in} = useParams()

    function componentToRender(){
        if(type_sing_in =="login"){
            return(
                <CardLoginAccount />
            )
        } else{
            return(
                <CardCreateAccount />
            )
        }
    }

    return(
        <>
            <div className={styles.backgroundGoPage}>
                {componentToRender()}
            </div>
        </>
    )
}

export default ElevenBankBackgroundLogin