import { useState } from "react"
import propsTypes from 'prop-types'

function RequestPersonalOrJointAccount(props){
    const [isPersonalAccount, setIsPersonalAccount] = useState(false)
    const [isJointAccount, setIsJointAccount] = useState(false)
    const [quantityOfPeoplesForJointAccount, setQuantityOfPeoplesForJointAccount] = useState(0)
    
    const blockWantJointAccount = <>
                                    <div>
                                        <input></input>
                                    </div>
                                </>

    const blockHowManyUsersInJointAccount = <>
                                    <div>
                                        <input></input>
                                    </div>
                                </>


    return (
        <>
            <div>
                {props.alreadyAccount ? blockWantJointAccount : null}
            </div>
        </>
    )
}

RequestPersonalOrJointAccount.propsTypes = {
    alreadyAccount: propsTypes.bool
}


export default RequestPersonalOrJointAccount