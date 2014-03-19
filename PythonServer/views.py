from hellotest import app
from controller import state
import json

@app.route('/PerfusionController/PythonServer/state.json')
def getstate():
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/playpause')
def playpause():
    state.playpause();
    return json.dumps(state.getstate())


@app.route('/PerfusionController/PythonServer/reset')
def reset():
    state.reset();
    return json.dumps(state.getstate())


@app.route('/PerfusionController/PythonServer/updateparameters')
def setparameters():
    state.updateparameters();
    return json.dumps(state.getstate())
