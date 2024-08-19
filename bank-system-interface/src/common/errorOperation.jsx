import { useEffect, useState } from "react"
import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'


function ErrorOperation(props){
    const [openingCard, setOpeningCard]=useState(false)

    useEffect(()=>{
        setOpeningCard(props.isOpen)
    }, [props.isOpen])

    const closeModal = () => {
        setOpeningCard(false);
        if (props.onClose) {
            props.onClose(); // Chama a função de callback passada pelo componente pai para alterar a variável de estado
        }
    };

    if(openingCard){
        return(
            <>
                <div className={styles.errorBackground} onClick={closeModal}>
                    <div className={styles.error}>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                            <path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/>
                        </svg>
                    </div>
                    <div className={styles.errorText}>
                        <h1>
                            {props.textShow}
                        </h1>
                    </div>
                </div>
            </>
        )
    } else{
        return null
    }
    
}

ErrorOperation.propsTypes = {
    isOpen: propsTypes.bool,
    textShow: propsTypes.string,
    onClose: propsTypes.func
}

ErrorOperation.defaultProps = {
    isOpen: false,
    textShow: "",
    onClose: null
}


export default ErrorOperation