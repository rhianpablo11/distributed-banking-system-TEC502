import { useEffect, useState } from "react"
import AccountInfos from "../../components/accountInfos"
import BalanceInfo from "../../components/balanceInfo"
import Deposit from "../../components/deposit"
import FastPix from "../../components/fastPix"
import HelloUser from "../../components/helloUser"
import TransactionSimpleList from "../../components/transactionsSimpleList"
import { useParams } from "react-router-dom"
import NavbarLogged from "../../components/navbarLogged"
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
                <NavbarLogged />
            </div>
            <div>
                <div>
                    <HelloUser name={userData.name} />
                    <AccountInfos account_number={userData.account_number} />
                </div>
                <div>
                    <BalanceInfo balance={userData.balance} blockedBalance={userData.blocked_balance} cdiBalance={userData.cdi_balance} savingBalance={userData.saving_balance} />
                    <TransactionSimpleList trasactionsList={userData.transactions} />
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