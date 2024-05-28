import styles from "../style_modules/commonStyles.module.css"

function ButtonLoginAccount(){
    const divStyle = {
        color: 'white',
        padding: '5px 30px',
        
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