import styles from "../style_modules/commonStyles.module.css"
import { Link } from "react-router-dom";

function ButtonLoginAccount(){
    const divStyle = {
        padding: '5px 15px',
        width: "120px"
      };
    return(
        <>
            <div  className={styles.buttonAccount}>
                <Link to='/go/login'>
                    <button style={divStyle}>
                        Login
                    </button>
                </Link>
            </div>
        </>
    )
}

export default ButtonLoginAccount