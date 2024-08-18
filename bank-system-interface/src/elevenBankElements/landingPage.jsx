import LogoBank from "../common/logoBank"
import styles from "./elevenBank.module.css"
import elevenBankLogo from "../assets/Eleven Bank.svg"
import ButtonCreateAccount from "../common/buttonCreateAccount"
import ButtonLoginAccount from "../common/buttonLoginAccount"
import elevenBankGif from "../assets/globo.gif"
import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"

function LandingPage(){
    const bank = elevenBankLogo
    const gifElevenBank = elevenBankGif
    const {nameBank} =useParams()
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
        document.documentElement.style.setProperty('--button-hover-color', "#615d53");
        document.documentElement.style.setProperty('--input-color', "#fbf9e7");
        document.documentElement.style.setProperty('--input-secondary-color', "#f5f2db");
        document.documentElement.style.setProperty('--letter-color', "#4e4e4e");
        document.documentElement.style.setProperty('--letter-placeholder-color', "#85635c");
        document.documentElement.style.setProperty('--letter-hover-color', "#a9a394");
        document.documentElement.style.setProperty('--letter-hover-color', "#0a3632");
    }

    useEffect(() => {
        document.title = nameBank+" bank";
      }, []); 


    return(
        <>
            <div className={styles.landingPageComponent}>
                <div className={styles.navBarBackground}>
                    <div className={styles.navBarLandingPage}>
                        <div className={styles.logoBankArea}>
                            <LogoBank nameBank={nameBank}/>
                        </div>
                        <div className={styles.buttonLadingPage}>
                            <ButtonCreateAccount  nameBank={nameBank}/>
                            <ButtonLoginAccount  nameBank={nameBank}/>
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