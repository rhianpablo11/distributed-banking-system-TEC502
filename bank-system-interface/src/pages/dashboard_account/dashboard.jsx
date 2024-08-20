import { useEffect, useState } from "react"
import AccountInfos from "../../components/accountInfos"
import BalanceInfo from "../../components/balanceInfo"
import Deposit from "../../components/deposit"
import FastPix from "../../components/fastPix"
import HelloUser from "../../components/helloUser"
import TransactionSimpleList from "../../components/transactionsSimpleList"
import { useParams } from "react-router-dom"
import NavbarLogged from "../../components/navbarLogged"
import { get_address_bank_selected, get_token, save_cookie_token } from "../../utils/constants"
import CurrentTime from "../../components/currentTime"

function Dashboard(){
    const {nameBank} = useParams()
    const [userData, setUserData] = useState({
        'balance': null,
        'account_number': null,
        'blocked_balance': null,
        'transactions': [{
            'value': null,
            'date_transaction': null,
            'concluded': null, 
            'name_source': null,
            'type_transaction': null
        }],
        'cdi_balance': null,
        'saving_balance': null,
        'name': null,
        'document': null,
        'telephone': null,
        'email': null,
        'is_company': null,
        'client_since': null,
        'banks_with_account': null

    })
    const [isServerErrorOcorred, setIsServerErrorOcorred] = useState(false)


    useEffect(()=>{
        const requestInfoAccount = async () => {
            try{
                const urlCommunicate = get_address_bank_selected()+'/account/logged'
                console.log(get_token())
                const response = await fetch(urlCommunicate, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${get_token()}`
                    }
                })

                if(response.ok){
                    setIsServerErrorOcorred(false)
                    const dataReceivedJson = await response.json()
                    setUserData(dataReceivedJson['account_info'])
                    console.log(userData)
                    save_cookie_token(dataReceivedJson['token_jwt'])
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
                <NavbarLogged />
            </div>
            <div>
                <div>
                    <HelloUser name={userData.name} />
                    <AccountInfos account_number={userData.account_number} />
                </div>
                <div>
                    <BalanceInfo balance={userData.balance} blockedBalance={userData.blocked_balance} cdiBalance={userData.cdi_balance} savingBalance={userData.saving_balance} />
                    <TransactionSimpleList transactionsList={userData.transactions} />
                </div>
                <div>
                    <CurrentTime />
                    <Deposit account_number={userData.account_number} />
                    <FastPix account_number={userData.account_number} />
                </div>
            </div>
        </>
    )
}

export default Dashboard