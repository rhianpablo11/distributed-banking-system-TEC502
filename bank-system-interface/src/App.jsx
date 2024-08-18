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
import CardRequestAgencyBank from "./common/cardRequestAgencyBank.jsx"
import RequestWhichBank from "./pages/request_bank/requestWhichBank.jsx"
import Dashboard from "./pages/dashboard_account/dashboard.jsx"

const router = createBrowserRouter([
  {
    path: "/",
    element: <CardRequestAgencyBank />
  },
  {
    path: '/dashboard-temp',
    element: <Dashboard />
  },
  {
    path: '/request-name-bank',
    element: <RequestWhichBank />
  },
  {
    path: "/:nameBank",
    element: <LandingPage />
  },
  {
    path: "/go/:nameBank/:type_sing_in",
    element: <ElevenBankBackgroundLogin />
  },
  {
    path: "/logged/:nameBank/:accountNumber",
    element: <BackgroundLogged />
  }, 
  {
    path: "/logged/:nameBank/:accountNumber/transactions",
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
