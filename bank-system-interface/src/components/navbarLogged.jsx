import LogoBank from "./logoBank"
import { useNavigate, useParams } from "react-router-dom"


function NavbarLogged(){
    const {nameBank} = useParams()
    const navigate = useNavigate()

    return (
        <>
            <div>
                <LogoBank nameBank={nameBank} />
            </div>
            <div>
                <h5>
                    <a >
                        dashboard
                    </a>
                </h5>
                <h5>
                    <a >
                        extract
                    </a>
                </h5>
                <h5>
                    <a >
                        payments
                    </a>
                </h5>
                <h5>
                    <a >
                        transfers
                    </a>
                </h5>
            </div>
            <div>
                <button>
                    Logout
                </button>
                <button >
                    Management User
                </button>
            </div>
        </>
    )
}

export default NavbarLogged