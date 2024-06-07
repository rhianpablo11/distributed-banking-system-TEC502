import styles from "../style_modules/commonStyles.module.css"
import { useNavigate } from "react-router-dom"

function CardRequestAgencyBank(){
    //fazer o request para pegar o nome do banco
    const navigate = useNavigate()
    function goBank(){
        return navigate("/elevenBank")
    }
    return (
        <>
            <div className={styles.requestAgencyComponent}>
                <div className={styles.backgroundRequestAgencyComponent}>
                    <div className={styles.logoUnifiedBank}>
                        <h1>Unified</h1>
                        <h3>Banks</h3>
                    </div>
                    <div className={styles.subtitleLogoUnifiedBank}> 
                        <h6>National banking consortium</h6>
                    </div>
                    <div className={styles.inputAgencyNumber}>
                        <h1>Please enter the number of the desired agency.</h1>
                        <input type="text" placeholder="Agency Number"></input>
                        <button onClick={goBank}>Go to Bank Page</button>
                    </div>
                </div>
                
            </div>
        
        </>
    )
}

export default CardRequestAgencyBank