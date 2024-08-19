import { useEffect, useState } from "react"


function CurrentTime(){
    const [timeCurrent, setTimeCurrent] = useState(new Date())
    const [timeCurrentFormated, setTimeCurrentFormated] = useState('')

    const addZero = (num) => {
        if(num<10){
            return '0'+num
        } else{
            return num
        }
    }

    const formatTime = () => {
        const hours = timeCurrent.getHours()
        const minutes = timeCurrent.getMinutes()
        const seconds = timeCurrent.getSeconds()
        setTimeCurrentFormated(`${addZero(hours)}:${addZero(minutes)}:${addZero(seconds)}`)
    }

    
    useEffect(()=>{
        formatTime()
        const interval = setInterval(()=>{setTimeCurrent(new Date)}, 1000)
        return () => {clearInterval(interval)}
    }, [timeCurrent])

    return(
        <>
            <div>
                <h2>Current Time:</h2>
                <h3>{timeCurrentFormated}</h3>
            </div>
        </>
    )
}


export default CurrentTime