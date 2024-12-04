import Config from './config.js'

async function queryInited() {
    const resp = await fetch(`${Config.BaseURL}/queryInited`, {
        method: 'GET'
    })
    return await resp.json()
}

async function queryEnvironment() {
    const resp = await fetch(`${Config.BaseURL}/queryEnvironment`, {
        method: 'GET'
    })
    return await resp.json()
}

async function queryRegistered() {
    const resp = await fetch(`${Config.BaseURL}/queryRegistered`, {
        method: 'GET'
    })
    return await resp.json()
}

async function register() {
    const resp = await fetch(`${Config.BaseURL}/register`, {
        method: 'POST'
    })
    return await resp.json()
}

async function startTask(instruction) {
    const resp = await fetch(`${Config.BaseURL}/startTask`, {
        method: 'POST',
        body: JSON.stringify({ instruction }),
    })
    return await resp.json()
}

async function stopTask() {
    const resp = await fetch(`${Config.BaseURL}/stopTask`, {
        method: 'POST'
    })
    return await resp.json()
}

async function queryTaskState() {
    const resp = await fetch(`${Config.BaseURL}/queryTaskState`, {
        method: 'GET'
    })
    return await resp.json()
}

async function queryIframeUrl() {
    const resp = await fetch(`${Config.BaseURL}/queryIframeUrl`, {
        method: 'GET'
    })
    return await resp.json()
}

async function resetEnv() {
    const resp = await fetch(`${Config.BaseURL}/resetScene`, {
        method: 'POST'
    })
    return await resp.json()
}

async function startVideo() {
    const resp = await fetch(`${Config.BaseURL}/startPushVideo`, {
        method: 'POST'
    })
    return await resp.json()
}

async function stopVideo() {
    const resp = await fetch(`${Config.BaseURL}/stopPushVideo`, {
        method: 'POST'
    })
    return await resp.json()
}

export { 
    queryInited, 
    queryRegistered, 
    queryEnvironment, 
    register, 
    startTask,
    stopTask, 
    queryTaskState, 
    queryIframeUrl, 
    resetEnv,
    startVideo,
    stopVideo
}
