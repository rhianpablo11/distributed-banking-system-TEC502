import styles from "../style_modules/commonStyles.module.css"
import propsTypes from 'prop-types'


function Loading(props){
    if(props.isOpen){
        return(
            <>
                <div className={styles.loadingBackground}>
                    <div className={styles.loader}>
                        <div className={styles.loaderSquare}></div>
                        <div className={styles.loaderSquare}></div>
                        <div className={styles.loaderSquare}></div>
                        <div className={styles.loaderSquare}></div>
                        <div className={styles.loaderSquare}></div>
                        <div className={styles.loaderSquare}></div>
                        <div className={styles.loaderSquare}></div>
                    </div>
                </div>
            </>
        )
    } else{
        return null
    }
    
}

Loading.propsTypes = {
    isOpen: propsTypes.bool,
    isBigElement: propsTypes.bool
}

Loading.defaultProps = {
    isOpen: false,
    isBigElement: false
}


export default Loading