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

export default function SelfHost() {
    const [iframeState, setIframeState] = useState('hidden')
    const [clientID, setClientID] = useState('')
    const [platform, setPlatform] = useState('')
    const [scene, setScene] = useState('')
    const [serverAvailable, setServerAvailable] = useState(false)
    const [historyMsg, setHistoryMsg] = useState([])
    const [instruction, setInstruction] = useState('')
    const [registerState, setRegisterState] = useState('Not Registered')
    const [iframeUrl, setIframeUrl] = useState(null)

    const iframeStyle = iframeState == 'hidden' ? {display: 'none'} : {
        'width': '100%',
        'height': '100%',
    }

    useEffect(() => {
        queryEnvironment().then(({state, client_id: clientId, env_name: platform, scene_name: scene}) => {
            if (state) {
                setClientID(clientId)
                setPlatform(platform)
                setScene(scene)
            }
        })
        ioQueryRegistered().then(({state, msg}) => {
            if (state) {
                setRegisterState('Registered')
            } else {
                setRegisterState('Not Registered')
            }
        })
    }, [])

    useEffect(() => {
        if (!serverAvailable) {
            queryInited().then((state, msg) => {
                if (state) {
                    setServerAvailable(true)
                } else {
                    setHistoryMsg([...historyMsg, msg])
                }
            })
        }
    }, [serverAvailable, historyMsg])

    function register() {
        setRegisterState('Registering...')
        ioRegister().then(({state, msg}) => {
            if (state) {
                setRegisterState('Registered')
                setHistoryMsg([...historyMsg, msg])
            } else {
                setRegisterState('Register Failed')
                setHistoryMsg([...historyMsg, msg])
            }
        })
    }

    function startTask() {
        ioStartTask(instruction).then(({state, msg}) => {
            setHistoryMsg([...historyMsg, msg])
        })
    }

    function stopTask() {
        ioStopTask().then(({state, msg}) => {
            setHistoryMsg([...historyMsg, msg])
        })
    }

    function queryTaskState() {
        ioQueryTaskState().then(({state, msg}) => {
            setHistoryMsg([...historyMsg, msg])
        })
    }

    function queryIframeUrl() {
        ioQueryIframeUrl().then(({state, msg}) => {
            if (state) {
                setIframeUrl(msg)
            } else {
                setHistoryMsg([...historyMsg, msg])
            }
        })
    }

    function resetScene() {
        ioResetEnv().then(({state, msg}) => {
            if (state) {
                setHistoryMsg([...historyMsg, msg])
            } else {
                setHistoryMsg([...historyMsg, msg])
            }
        })
    }


    return (
        <>
            <form>
                <label>
                    Client-ID: <input type="text" value={clientID} disabled/>
                </label>
                <br/>
                <label>
                    Platform: <input type="text" value={platform} disabled/>
                </label>
                <br/>
                <label>
                    Scene: <input type="text" value={scene} disabled/>
                </label>
                <br/>
                <label>
                    Register State: <span>{registerState}</span>
                </label>
                <br/>
                <label>
                    Instruction: <input type="text" value={instruction} onChange={e => setInstruction(e.target.value)}/>
                </label>
            </form>
            <button onClick={register}>Register</button>
            <button onClick={startTask}>Start Task</button>
            <button onClick={stopTask}>Stop Task</button>
            <button onClick={resetScene}>Reset Scene</button>
            <button onClick={queryTaskState}>Query Task State</button>
            <button onClick={() => {setIframeState(iframeState == 'hidden'? 'show' : 'hidden')}}>Change-Iframe</button>
            <button onClick={queryIframeUrl}>Start Live</button>
            <div>
                <h2>History</h2>
                <ul>
                    {historyMsg.map((msg, index) => <li key={index}>{msg}</li>)}
                </ul>
            </div>
            <iframe style={iframeStyle} src={iframeUrl}></iframe>
        </>
    )
}