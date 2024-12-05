async function queryInited() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
        'state': true,
        'msg': 'Inited'
    }
}

async function queryEnvironment() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
        'state': true,
        'client_id': 123,
        'platform': 'omnigibson',
        'scene': 'ToT',
        'live_type': 'selfhost'
    }
}

async function queryRegistered() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    const choice = Math.random() > 0.5 ? true : false
    if (choice) {
        return {
            'state': true,
            'msg': 'Registered'
        }
    }
    else {
        return {
            'state': false,
            'msg': 'Not Registered'
        }
    }
}

async function register() {
    await new Promise(resolve => setTimeout(resolve, 2000))
    return {
        'state': true,
        'msg': 'Registered'
    }
}

async function startTask() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
        'state': true,
        'msg': 'Task Started'
    }
}

async function stopTask() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
        'state': true,
        'msg': 'Task Stopped'
    }
}

async function queryTaskState() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
        'state': true,
        'msg': 'Task Running'
    }
}

async function resetEnv() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
        'state': true,
        'msg': 'Environment Reset'
    }
}

export { 
    queryInited, 
    queryRegistered,
    queryEnvironment,
    register, 
    startTask, 
    stopTask, 
    queryTaskState, 
    resetEnv
}