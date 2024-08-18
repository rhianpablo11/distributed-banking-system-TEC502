import { useEffect, useState } from "react"
import Account_infos from "../../components/account_infos"
import Balance_info from "../../components/balance_info"
import Deposit from "../../components/deposit"
import Fast_pix from "../../components/fast_pix"
import Hello_user from "../../components/hello_user"
import Transaction_simple_list from "../../components/transactions_simple_list"
import { useParams } from "react-router-dom"
import Navbar_logged from "../../components/navbar_logged"
import { get_address_bank_selected } from "../../utils/constants"
import CurrentTime from "../../components/currentTime"

function Dashboard(){
    const {nameBank} = useParams()
    const [userData, setUserData] = useState()
    const [isServerErrorOcorred, setIsServerErrorOcorred] = useState(false)

    
    useEffect(()=>{
        const requestInfoAccount = async () => {
            try{
                const response = await fetch(get_address_bank_selected(), {
                    method: 'POST'
                })

                if(response.ok){
                    setIsServerErrorOcorred(true)
                    const dataReceivedJson = await response.json()
                    setUserData(dataReceivedJson)
                } else{
                    setIsServerErrorOcorred(true)
                }
                
            } catch(error) {
                setIsServerErrorOcorred(true)
            }
        }

        requestInfoAccount()

        const interval = setInterval(requestInfoAccount, 1000)
        return () => clearInterval(interval)
    }, [])


    return (
        <>
            <div>
                <Navbar_logged />
            </div>
            <div>
                <div>
                    <Hello_user name={userData.name} />
                    <Account_infos account_number={userData.account_number} />
                </div>
                <div>
                    <Balance_info balance={userData.balance} blockedBalance={userData.blocked_balance} cdiBalance={userData.cdi_balance} savingBalance={userData.saving_balance} />
                    <Transaction_simple_list trasactionsList={userData.transactions} />
                </div>
                <div>
                    <CurrentTime />
                    <Deposit account_number={userData.account_number} />
                    <Fast_pix account_number={userData.account_number} />
                </div>
            </div>
        </>
    )
}

export default Dashboard