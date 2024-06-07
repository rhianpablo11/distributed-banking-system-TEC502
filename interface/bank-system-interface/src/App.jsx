import LandingPage from "./elevenBankElements/landingPage"
import CardFastPix  from "./common/cardFastPix.jsx"
import LogoBank from "./common/logoBank.jsx"
import CardCreateAccount from "./common/cardCreateAccount.jsx"
import CardLoginAccount from "./common/cardLoginAccount.jsx"
import ButtonCreateAccount from "./common/buttonCreateAccount.jsx"
import ButtonLoginAccount from "./common/buttonLoginAccount.jsx"
import BackgroundLogged from "./common/backgroundLogged.jsx"
import { ReactDOM } from "react"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import ElevenBankBackgroundLogin from "./elevenBankElements/elevenBankBackgroundLogin.jsx"
import BackgroundTransactions from "./common/backgroundTransactions.jsx"

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />
  },
  {
    path: "/go/:type_sing_in",
    element: <ElevenBankBackgroundLogin />
  },
  {
    path: "/logged/:account_number",
    element: <BackgroundLogged />
  }, 
  {
    path: "/logged/:account_number/transactions",
    element: <BackgroundTransactions />
  }
])

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App
