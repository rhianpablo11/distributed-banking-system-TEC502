import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { get_address_bank_selected, set_address_bank_selected } from "../../utils/constants"
import Loading from "../../components/loading"
import Error from "../../components/error"



function RequestWhichBank(){
    const navigate = useNavigate()
    const [address_banks, set_address_banks] = useState([])
    const [name_banks, set_name_banks] = useState([])
    const [bank_selected, set_bank_selected] = useState()
    const [is_loading, set_is_loading] = useState(false)
    const [is_error_in_connection, set_is_error_in_connection] = useState(false)


    useEffect(()=>{
        set_address_banks([import.meta.env.VITE_REACT_ADDRESS_BANK_0,import.meta.env.VITE_REACT_ADDRESS_BANK_1, import.meta.env.VITE_REACT_ADDRESS_BANK_2, import.meta.env.VITE_REACT_ADDRESS_BANK_3, import.meta.env.VITE_REACT_ADDRESS_BANK_4])
        set_name_banks([import.meta.env.VITE_REACT_NAME_BANK_0,import.meta.env.VITE_REACT_NAME_BANK_1, import.meta.env.VITE_REACT_NAME_BANK_2, import.meta.env.VITE_REACT_NAME_BANK_3, import.meta.env.VITE_REACT_NAME_BANK_4])
    },[])


    const verify_connection = async () => {
        const address_selected = get_address_bank_selected()
        if(address_selected == ''){
            return false
        } else{
            set_is_loading(true)
            try{
                const urlToConnect = address_selected+'/bank'
                const response = await fetch(urlToConnect, {
                    method: 'GET'
                })
                console.log(response)
                if(response.ok){
                    set_is_loading(false)
                    return true
                } else{
                    return false
                }
            } catch(error){
                set_is_loading(false)
                return false
            } 
                
        }
    }


    const redirect_to_bank_page = async () => {
        set_address_bank_selected(address_banks[name_banks.indexOf(bank_selected)])
        const result_of_connection =  await verify_connection()
        if(result_of_connection){
            navigate('/'+bank_selected)
        } else{
            set_is_error_in_connection(true)
        }
    }


    return (<>
            <div>
                <div>
                    <div>
                        <h1>Unified</h1>
                        <h3>Banks</h3>
                    </div>
                    <div>
                        <h6>National banking consortium</h6>
                    </div>
                    <div>
                        <h1>Please select which bank to connect</h1>
                        <select value={bank_selected} onChange={()=>set_bank_selected(event.target.value)}>
                            <option>Select bank</option>
                            {name_banks.map((bank_name, index)=>(
                                <option key={index} value={bank_name}>{bank_name}</option>
                            ))}
                        </select>
                        <button onClick={redirect_to_bank_page}>
                            Go to bank page
                        </button>
                    </div>
                </div>
                <Loading is_loading={is_loading} />
                <Error is_error={is_error_in_connection}/>
            </div>
        </>)
}

export default RequestWhichBank