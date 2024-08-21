import { useState } from "react"


function CreateAccountForm(){
    const [isJointAccount, setIsJointAccount] = useState(false)
    const [isCompany, setIsCompany] = useState(false)
    const [quantityOfPeoplesForJointAccount, setQuantityOfPeoplesForJointAccount] = useState(0)
    const [listDataUsers, setListDataUsers] =useState([])

    /*
    fluxo:
        1. pede documento
            1.1 ja verifica se é cnpj ou cpf
        2. verifica se o usuario existe
            2.1 se ja existir pergunta se quer criar uma conta conjunta
            2.1.1 pergunta quantas pessoas quer criar, e vai passando os forms p cada um
        3. se n existir vai pedir as info de documento e tals
        4. cria a conta
    */

    return (
        <>
            <div>
                
            </div>
        </>
    )
}


export default CreateAccountForm