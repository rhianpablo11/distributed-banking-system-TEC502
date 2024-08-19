import styles from "../style_modules/commonStyles.module.css"
import { Link } from "react-router-dom";
import propsTypes from 'prop-types'
import { useState } from "react";

function ButtonCreateAccount(props){

    const [urlGo, setUrlGo] = useState("/go/"+props.nameBank+"/signup")

    return(
        <>
            <div className={styles.buttonAccount}>
                <Link to={urlGo}>
                    <button>
                        Create Account
                    </button>
                </Link>
            </div>
        </>
    )
}

ButtonCreateAccount.propsTypes = {
    nameBank: propsTypes.string
}

ButtonCreateAccount.defaultProps = {
    nameBank: "Unified"
}

export default ButtonCreateAccount