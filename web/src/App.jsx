import { useState, useEffect } from "react";
import SelfHost from "./selfhost/SelfHost";
import Transfer from "./transfer/Transfer";

import {
  queryInited as ioQueryInited, 
  queryRegistered as ioQueryRegistered,
  queryEnvironment as ioQueryEnvironment,
  register as ioRegister, 
  startTask as ioStartTask, 
  stopTask as ioStopTask, 
  queryTaskState as ioQueryTaskState,
  resetEnv as ioResetEnv,
} from './io/selfhost_utils'

const RegisterState = {
  NotRegistered: "Not Registered",
  Registered: "Registered",
  Registering: "Registering...",
}

function App() {
  const [historyMsg, setHistoryMsg] = useState([]);
  const [page_type, setPage_type] = useState("transfer");
  const [registerState, setRegisterState] = useState(RegisterState.NotRegistered);
  const [envInfo, setEnvInfo] = useState({client_id: '', env_name: '', scene_name: ''});
  const [serverAvailable, setServerAvailable] = useState(false);


  useEffect(() => {
    (async () => {
      const {state: server_state, msg: server_msg} = await ioQueryInited()
      setServerAvailable(server_state)
      setHistoryMsg(h => [...h, server_msg])

      if (server_state) {
        ioQueryEnvironment().then(({state, client_id: clientId, env_name: platform, scene_name: scene}) => {
          setHistoryMsg(h => [...h, `Query Environment: ${state ? 'Success' : 'Failed'}`, `Client ID: ${clientId}`, `Platform: ${platform}`, `Scene: ${scene}`])
          if (state) {
            setEnvInfo({client_id: clientId, env_name: platform, scene_name: scene})
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
  })

  return (
    <main className="h-screen flex flex-row">
      {/* Viewer Part */}
      <section className="flex-1 bg-gray-100 flex flex-col">
        {/* Video Display */}
        <div className="flex-1 bg-black flex items-center justify-center text-white">
          <div>Video Display Area</div>
        </div>
        
        {/* Input and Button */}
        <div className="flex items-center justify-center p-4">
          <input className="flex-1 border border-gray-400 rounded p-2 mr-2" placeholder="Enter text here..." />
          <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Search
          </button>
        </div>
      </section>

      {/* Operation Part */}
      <section className="w-80 bg-gray-300 flex flex-col p-4 shadow-lg">
        <h2 className="text-lg font-semibold mb-4">System Information</h2>

        <form className="space-y-3">
          <div className="flex justify-between">
            <label>Client-ID:</label>
            <input type="text" value={123} disabled className="border border-gray-400 rounded p-1 bg-gray-200" />
          </div>
          <div className="flex justify-between">
            <label>Platform:</label>
            <input type="text" value={456} disabled className="border border-gray-400 rounded p-1 bg-gray-200" />
          </div>
          <div className="flex justify-between">
            <label>Scene:</label>
            <input type="text" value={789} disabled className="border border-gray-400 rounded p-1 bg-gray-200" />
          </div>
          <div className="flex justify-between">
            <label>Register State:</label>
            <span className="font-semibold">{125236}</span>
          </div>
        </form>

        <hr className="my-4" />

        <div className="flex flex-col space-y-3">
          <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
            Perform Action 1
          </button>
          <button className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
            Perform Action 2
          </button>
        </div>
      </section>
    </main>
  );
}

export default App;
