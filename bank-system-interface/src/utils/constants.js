var address_bank_selected = ''
export function set_address_bank_selected (address){
    address_bank_selected = address
}

export function get_address_bank_selected (){
    return address_bank_selected
}

export function get_url_to_require_account_data (){
    return address_bank_selected+'/account/logged'
}