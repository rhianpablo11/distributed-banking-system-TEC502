import { useState } from "react"


function RequestDocumentUserCreateAccount(){
    const [documentInserted, setDocumentInserted] = useState('')

    //fazer um call to verify if this document exists with someone user

    return(
        <>
            <div>
                <h3>Your Document</h3>
                <input required  type="text" placeholder="xxx.xxx.xxx-xx/xx.xxx.xxx/000x-xx" value={documentInserted} onChange={()=>{setDocumentInserted(event.target.value)}}></input>
            </div>
            <button>
                Next
            </button>
        </>
    )
}


export default RequestDocumentUserCreateAccount