async function queryInited() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'msg': 'Inited'
    }
}

async function queryEnvironment() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'client_id': 123,
        'platform': 'omnigibson',
        'scene': 'ToT'
    }
}

async function register() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'msg': 'Registered'
    }
}

async function startTask() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'msg': 'Task Started'
    }
}

async function stopTask() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'msg': 'Task Stopped'
    }
}

async function queryTaskState() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'msg': 'Task Running'
    }
}

async function queryIframeUrl() {
    await new Promise(resolve => setTimeout(resolve, 3000))
    return {
        'state': true,
        'msg': 'http://127.0.0.1:5500/index.html'
    }
}

export { queryInited , queryEnvironment, register, startTask , stopTask , queryTaskState, queryIframeUrl  }