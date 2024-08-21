import Cookies from 'js-cookie'
var address_bank_selected = ''

export function set_address_bank_selected (address){
    address_bank_selected = address
}

export function get_address_bank_selected (){
    return 'http://localhost:10000'
}

export function get_url_to_require_account_data (){
    return address_bank_selected+'/account/logged'
}

export function save_cookie_token(token_to_save){
    const expirationDate = new Date();
    expirationDate.setSeconds(expirationDate.getSeconds() + 5);
    Cookies.set("token", token_to_save, {expires: 1})
    return null
}

export function get_token(){
    return Cookies.get('token')
}

export function remove_token(){
    Cookies.remove('token')
}


export function formatCurrency(value){
    const parts = value.toFixed(2).split('.')
    const integerPart = parts[0]
    const decimalPart = parts[1]
    const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.')
    return formattedIntegerPart+","+decimalPart
}
