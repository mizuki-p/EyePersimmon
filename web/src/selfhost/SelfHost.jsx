import { useState, useEffect } from "react"
import { 
    queryInited, 
    queryRegistered as ioQueryRegistered,
    queryEnvironment,
    register as ioRegister, 
    startTask as ioStartTask, 
    stopTask as ioStopTask, 
    queryTaskState as ioQueryTaskState,
    queryIframeUrl as ioQueryIframeUrl,
    resetEnv as ioResetEnv

} from '../io/selfhost_utils'
// import { 
//     queryInited, 
//     queryEnvironment,
//     register as ioRegister, 
//     startTask as ioStartTask, 
//     stopTask as ioStopTask, 
//     queryTaskState,
//     queryIframeUrl as ioQueryIframeUrl
// } from '../io/fake_utils'

export default function SelfHost({ setHistoryMsg }) {
    const [iframeUrl, setIframeUrl] = useState(null)

    useEffect(() => {
        ioQueryIframeUrl().then(({state, msg}) => {
            if (state) {
                setIframeUrl(msg)
            } else {
                setHistoryMsg(h => [...h, msg])
            }
        })

        return () => {
            setIframeUrl(null)
        }
    }, [setHistoryMsg])

    return (
        <iframe 
            src={iframeUrl}
            className="w-full h-full"
            frameBorder="0"
            allowFullScreen
        ></iframe>
    )
}