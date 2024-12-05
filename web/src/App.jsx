import { useState, useEffect } from "react";
import SelfHost from "./selfhost/SelfHost";
import Transfer from "./transfer/Transfer";
import HistoryMessages from "./common/HistoryMessages";

import {
  queryInited as ioQueryInited, 
  queryRegistered as ioQueryRegistered,
  queryEnvironment as ioQueryEnvironment,
  register as ioRegister, 
  startTask as ioStartTask, 
  stopTask as ioStopTask, 
  queryTaskState as ioQueryTaskState,
  resetEnv as ioResetEnv,
} from './io/fake_utils'

const RegisterState = {
  NotRegistered: "Not Registered",
  Registered: "Registered",
  Registering: "Registering...",
}

const TaskState = {
  Stopped: "Stopped",
  Running: "Running",
  Waiting: "...",
}

const VideoState = {
  Paused: "Paused",
  Living: "Living",
}

const VideoType = {
  SelfHost: "selfhost",
  Transfer: "transfer",
}

function App() {
  const [historyMsg, setHistoryMsg] = useState([]);
  const [videoType, setVideoType] = useState(VideoType.Transfer);
  const [registerState, setRegisterState] = useState(RegisterState.NotRegistered);
  const [envInfo, setEnvInfo] = useState({client_id: '', env_name: '', scene_name: ''});
  const [serverAvailable, setServerAvailable] = useState(false);
  const [taskState, setTaskState] = useState(TaskState.Stopped);
  const [videoState, setVideoState] = useState(VideoState.Paused);


  useEffect(() => {
    (async () => {
      const {state: server_state, msg: server_msg} = await ioQueryInited()
      setServerAvailable(server_state)
      setHistoryMsg(h => [...h, server_msg])

      if (server_state) {
        ioQueryEnvironment().then(({state, client_id: clientId, platform, scene: scene, live_type}) => {
          setHistoryMsg(h => [...h, `Query Environment: ${state ? 'Success' : 'Failed'}`, `Client ID: ${clientId}`, `Platform: ${platform}`, `Scene: ${scene}`])
          if (state) {
            console.log('setEnvInfo', {client_id: clientId, env_name: platform, scene_name: scene, live_type})
            setEnvInfo({client_id: clientId, env_name: platform, scene_name: scene,})
            setVideoType(live_type)
          }
        })

        ioQueryRegistered().then(({state, msg}) => {
          setHistoryMsg(h => [...h, msg])
          if (state) {
              setRegisterState(RegisterState.Registered)
          } else {
              setRegisterState(RegisterState.NotRegistered)
          }
        })
      }
    })()
  }, [])

  function register() {
    setRegisterState(RegisterState.Registering)
    ioRegister().then(({state, msg}) => {
      setHistoryMsg(h => [...h, msg])
      if (state) {
        setRegisterState(RegisterState.Registered)
      } else {
        setRegisterState(RegisterState.NotRegistered)
      }
    })
  }

  // Task Functions
  const start_task_btn = <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600" onClick={startTask}> Execute </button>
  const stop_task_btn = <button className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600" onClick={stopTask}> Stop </button>
  const waiting_task_btn = <button className="bg-gray-500 text-white px-4 py-2 rounded" disabled> Waiting... </button>
  const task_btn = 
    (taskState === TaskState.Stopped) ? start_task_btn : 
    (taskState === TaskState.Running) ? stop_task_btn : 
    waiting_task_btn


  function startTask() {
    setTaskState(TaskState.Waiting)
    ioStartTask().then(({state, msg}) => {
      setHistoryMsg(h => [...h, msg])
      if (state) {
        setTaskState(TaskState.Running)
      }
    })
  }

  function stopTask() {
    setTaskState(TaskState.Waiting)
    ioStopTask().then(({state, msg}) => {
      setHistoryMsg(h => [...h, msg])
      if (state) {
        setTaskState(TaskState.Stopped)
      }
    })
  }

  // Reset Environment
  function resetEnv() {
    ioResetEnv().then(({state, msg}) => {
      setHistoryMsg(h => [...h, msg])
    })
  }

  // Video Functions
  const video = 
    (videoState === VideoState.Paused) ? <div>Video Display Area</div> :
    (videoType === VideoType.SelfHost) ? <SelfHost setHistoryMsg={setHistoryMsg} /> :
    <Transfer setHistoryMsg={setHistoryMsg} />

  function startVideo() {
    setVideoState(VideoState.Living)
  }

  function stopVideo() {
    setVideoState(VideoState.Paused)
  }

  return (
    <main className="h-screen flex flex-row">
      {/* Viewer Part */}
      <section className="flex-1 bg-gray-100 flex flex-col">
        {/* Video Display */}
        <div className="flex-1 bg-black flex items-center justify-center text-white">
          {video}
        </div>
        
        {/* Input and Button */}
        <div className="flex items-center justify-center p-4">
          <input className="flex-1 border border-gray-400 rounded p-2 mr-2" placeholder="Enter text here..." />
          {task_btn}
        </div>
      </section>

      {/* Operation Part */}
      <section className="w-80 bg-gray-300 flex flex-col p-4 shadow-lg">
        <h2 className="text-lg font-semibold mb-4">System Information</h2>

        <form className="space-y-3">
          <div className="flex justify-between">
            <label>Client-ID:</label>
            <input type="text" value={envInfo.client_id} disabled className="border border-gray-400 rounded p-1 bg-gray-200" />
          </div>
          <div className="flex justify-between">
            <label>Platform:</label>
            <input type="text" value={envInfo.env_name} disabled className="border border-gray-400 rounded p-1 bg-gray-200" />
          </div>
          <div className="flex justify-between">
            <label>Scene:</label>
            <input type="text" value={envInfo.scene_name} disabled className="border border-gray-400 rounded p-1 bg-gray-200" />
          </div>
          <div className="flex justify-between">
            <label>Register State:</label>
            <span className="font-semibold">{registerState}</span>
          </div>
        </form>

        <hr className="my-4" />

        <div className="flex flex-col space-y-3">
          <button 
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600" 
            disabled={registerState !== RegisterState.NotRegistered || !serverAvailable}
            onClick={register}
          >
            Register 
          </button>
          <button 
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            onClick={resetEnv}
          >
            resetScene
          </button>


          <button
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            onClick={startVideo}
          >
            Start Video
          </button>
          <button
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            onClick={stopVideo}
          >
            Stop Video
          </button>
        </div>

        <hr className="my-4" />

        <HistoryMessages messages={historyMsg} />
      </section>
    </main>
  );
}

export default App;
