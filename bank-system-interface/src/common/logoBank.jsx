import { useEffect, useState } from "react"
import elevenBankLogo from "../assets/Eleven Bank.svg"
import automobiliLogo from "../assets/Automobili Bank.svg"
import { useNavigate } from "react-router-dom"
import propsTypes from 'prop-types'
import styles from "../style_modules/commonStyles.module.css"
import { useParams } from "react-router-dom"
import { useLocation } from 'react-router-dom';


function LogoBank(props){
    const navigate = useNavigate()
    const {nameBank} =useParams()
    function goToLanding(){
        return navigate("/")
    }
    const location = useLocation();
    const initialStyleH1 = {
        'color': "white"
    }
    const internalStyleH1 ={
        'color': 'var(--letter-color)'
    }
    const internalStyleH2 = {
        'color': 'var(--letter-placeholder-color)'
    }
    const [styleToRenderH1, setStyleToRenderH1] = useState(initialStyleH1)
    const [styleToRenderH2, setStyleToRenderH2] = useState(initialStyleH1)
    const pathToCompare = '/'+nameBank
    useEffect(()=>{
        if(location.pathname != pathToCompare){
            setStyleToRenderH1(internalStyleH1)
            setStyleToRenderH2(internalStyleH2)
        }
    },[])
    
    return(
        <>
            <div className={styles.logoBankStyle} onClick={goToLanding} >
                <h1 style={styleToRenderH1}>{props.nameBank}</h1>
                <h2 style={styleToRenderH2}>bank</h2>
            </div>
            
        </>
    )
}

LogoBank.propsTypes = {
    nameBank: propsTypes.string
}

LogoBank.defaultProps = {
    nameBank: "Unified"
}

export default LogoBank