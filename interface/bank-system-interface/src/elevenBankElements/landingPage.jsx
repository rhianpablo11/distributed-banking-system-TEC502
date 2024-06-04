import LogoBank from "../common/logoBank"
import styles from "./elevenBank.module.css"
import elevenBankLogo from "../assets/Eleven Bank.svg"
import ButtonCreateAccount from "../common/buttonCreateAccount"
import ButtonLoginAccount from "../common/buttonLoginAccount"
import elevenBankGif from "../assets/globo.gif"

function LandingPage(){
    const bank = elevenBankLogo
    const gifElevenBank = elevenBankGif



    return(
        <>
            <div className={styles.landingPageComponent}>
                <div className={styles.navBarBackground}>
                    <div className={styles.navBarLandingPage}>
                        <div className={styles.logoBankArea}>
                            <LogoBank />
                        </div>
                        <div className={styles.buttonLadingPage}>
                            <ButtonCreateAccount />
                            <ButtonLoginAccount />
                        </div>
                    </div>
                </div>
                <div className={styles.principalArea}>
                    <div className={styles.textPrincipalArea}>
                        <h1 className={styles.submainSentence}>
                            The new concept of
                        </h1>
                        <h1 className={styles.mainSentence}>
                            Tech Bank.
                        </h1>
                        <h3 className={styles.subtitle}>
                            For personal or<br></br>
                            executive uses
                        </h3>
                        <h6 className={styles.infoAboutConsortium}>
                            part of the national banking consortium
                        </h6>
                    </div>
                    <div className={styles.gifArea}>
                        <img src={gifElevenBank}></img>
                    </div>
                </div>
            </div>
        </>
    )
}

export default LandingPage