import styles from "../style_modules/commonStyles.module.css"

function ButtonLoginAccount(){
    const divStyle = {
        padding: '5px 15px',
        width: "120px"
      };
    return(
        <>
            <div  className={styles.buttonAccount}>
                <button style={divStyle}>
                    Login
                </button>
            </div>
        </>
    )
}

export default ButtonLoginAccount