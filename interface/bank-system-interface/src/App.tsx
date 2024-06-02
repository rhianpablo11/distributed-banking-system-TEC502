import LandingPage from "./elevenBankElements/landingPage"
import CardFastPix  from "./common/cardFastPix.tsx"
import LogoBank from "./common/logoBank.tsx"
import CardCreateAccount from "./common/cardCreateAccount.tsx"
import CardLoginAccount from "./common/cardLoginAccount.tsx"
import ButtonCreateAccount from "./common/buttonCreateAccount.tsx"
import ButtonLoginAccount from "./common/buttonLoginAccount.tsx"
import BackgroundLogged from "./common/backgroundLogged.tsx"
import { ReactDOM } from "react"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import ElevenBankBackgroundLogin from "./elevenBankElements/elevenBankBackgroundLogin.tsx"

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
