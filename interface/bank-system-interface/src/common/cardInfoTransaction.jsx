import styles from "../style_modules/commonStyles.module.css"
import sendImg from "../assets/send.svg"


function CardInfoTransaction(){
    
    return (
        <>
            <div className={styles.infoTransactionBlockList}>
                <div className={styles.iconAboutMoneyTransaction}>
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M19.2111 2.06722L3.70001 5.94499C1.63843 6.46039 1.38108 9.28612 3.31563 10.1655L8.09467 12.3378C9.07447 12.7831 10.1351 12.944 11.1658 12.8342C11.056 13.8649 11.2168 14.9255 11.6622 15.9053L13.8345 20.6843C14.7139 22.6189 17.5396 22.3615 18.055 20.3L21.9327 4.78886C22.3437 3.14517 20.8548 1.6563 19.2111 2.06722ZM8.92228 10.517C9.85936 10.943 10.9082 10.9755 11.8474 10.6424C12.2024 10.5165 12.5417 10.3383 12.8534 10.1094C12.8968 10.0775 12.9397 10.0446 12.982 10.0108L15.2708 8.17974C15.6351 7.88831 16.1117 8.36491 15.8202 8.7292L13.9892 11.018C13.9553 11.0603 13.9225 11.1032 13.8906 11.1466C13.6617 11.4583 13.4835 11.7976 13.3576 12.1526C13.0244 13.0918 13.057 14.1406 13.4829 15.0777L15.6552 19.8567C15.751 20.0673 16.0586 20.0393 16.1147 19.8149L19.9925 4.30379C20.0372 4.12485 19.8751 3.96277 19.6962 4.00751L4.18509 7.88528C3.96065 7.94138 3.93264 8.249 4.14324 8.34473L8.92228 10.517Z" />
                    </svg>
                </div>
                <div className={styles.infoTechnicalAboutTransaction}>
                    <h2 style={{'font-size': '1.5rem', 'font-weight': '500'}}>Pix Enviado</h2>
                    <h2 >25/12/2024 - 12:54</h2>
                </div>
                <div className={styles.infoTechnicalAboutTransaction}>
                    <h2 style={{'font-size': '1.5rem', 'font-weight': '500'}}>To:</h2>
                    <h2 style={{'padding-left':'15px'}}>Rhian Pablo A Almeida hian Pablo A Almeida</h2>
                </div>
                <div className={styles.infoValueAboutTransaction}>
                    <h2 style={{'font-size': '1.5rem', 'font-weight': '500'}}>Value:</h2>
                    <div className={styles.infoValueAboutTransactionValueArea}>
                        <p>US$</p>
                        <h2 style={{'padding-left':'5px'}}>50000000000000.00</h2>
                    </div>

                </div>
            </div>
        </>
    )
}

export default CardInfoTransaction