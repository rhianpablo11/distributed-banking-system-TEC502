import { useState } from "react"


function RequestInfosUser(){
    const [emailInserted, setEmailInserted] = useState('')
    const [nameInserted, setNameInserted] = useState('')
    const [telephoneInserted, setTelephoneInserted] = useState('')
    const [dateInserted, setDateInserted] = useState('')

    //call function to verify if email or telephone associated a other user

    return(
        <>
            <div>
                <h3>Your Name</h3>
                <input required  type="text" placeholder="Fulano de Tal" value={nameInserted} onChange={()=>{setNameInserted(event.target.value)}}></input>
            </div>
            <div>
                <h3>Your Email</h3>
                <input required  type="email" placeholder="youremail@email.com" value={emailInserted} onChange={()=>{setEmailInserted(event.target.value)}}></input>
            </div>
            <div>
                <h3>Your Telephone</h3>
                <input required  type="telephone" placeholder="11 95652-1033" value={telephoneInserted} onChange={()=>{setTelephoneInserted(event.target.value)}}></input>
            </div>
            <div>
                <h3>Your Birth Date</h3>
                <input required  type="date"  value={dateInserted} onChange={()=>{setDateInserted(event.target.value)}}></input>
            </div>
            <button>
                Next
            </button>
        </>
    )
}

export default RequestInfosUser