import { useEffect } from "react"


function CurrentTime(){


    useEffect(()=>{
        

        const interval = setInterval(, 1000)
        return () => clearInterval(interval)
    }, [])

    return(
        <>
            <div>
                <h2>Current Time:</h2>
                <h3></h3>
            </div>
        </>
    )
}


export default CurrentTime