import styles from "../style_modules/commonStyles.module.css"
import { Link } from "react-router-dom";
import propsTypes from 'prop-types'
import { useState } from "react";

function ButtonLoginAccount(props){
    const divStyle = {
        padding: '5px 15px',
        width: "120px"
      };

    const [urlGo, setUrlGo] = useState("/go/"+props.nameBank+"/login")
    return(
        <>
            <div  className={styles.buttonAccount}>
                <Link to={urlGo}>
                    <button style={divStyle}>
                        Login
                    </button>
                </Link>
            </div>
        </>
    )
}

ButtonLoginAccount.propsTypes = {
    nameBank: propsTypes.string
}

ButtonLoginAccount.defaultProps = {
    nameBank: "Unified"
}


export default ButtonLoginAccount