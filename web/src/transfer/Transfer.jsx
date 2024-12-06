import { useState, useEffect} from "react"
import { 
    startVideo as ioStartVideo,
    stopVideo as ioStopVideo

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
    const [videoUrl, setVideoUrl] = useState('')

    useEffect(() => {
        function startVideo() {
            ioStartVideo().then(({state, msg}) => {
                if (state) {
                    setHistoryMsg(h => [...h, msg])
                    setVideoUrl(`http://121.48.161.147:33601/getVideo?${new Date().getTime()}`)
                } else {
                    setHistoryMsg(h => [...h, msg])
                }
            })
        }

        function stopVideo() {
            ioStopVideo().then(({state, msg}) => {
                setHistoryMsg(h => [...h, msg])
            })
        }

        startVideo()
        return stopVideo
    }, [setHistoryMsg])

    return (
        <div className="w-full h-full flex items-center justify-center">
          <img className="w-full h-auto object-cover" src={videoUrl}></img>
        </div>
    )
}