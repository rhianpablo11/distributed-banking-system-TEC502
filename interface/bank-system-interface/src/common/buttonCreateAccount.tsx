import styles from "../style_modules/commonStyles.module.css"
import { Link } from "react-router-dom";

function ButtonCreateAccount(){

    return(
        <>
            <div className={styles.buttonAccount}>
                <Link to='/go/signup'>
                    <button>
                        Create Account
                    </button>
                </Link>
            </div>
        </>
    )
}

export default ButtonCreateAccount