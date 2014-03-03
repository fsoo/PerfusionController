from flask import Flask
app = Flask(__name__)

import json
from time import strftime, localtime;

import threading
paused=0;

class ControllerState :
    StartTime = "00:00:00"
    ElapsedTime = "00:00:00"
    FixTime = "08:00:00"
    EtOHTime = "00:15:00"
    AcetoneTime = "00:15:00"
    TotalTime = "08:30:00"
    ServerTime =strftime("%H:%M:%S",localtime())
    def getstate(self):
        localstate = { 'ElapsedTime': self.ElapsedTime,
            'FixTime': self.FixTime,
            'EtOHTime':self.EtOHTime,
            'AcetoneTime':self.AcetoneTime,
            'TotalTime': self.TotalTime,
            'ServerTime':strftime("%H:%M:%S",localtime())};
        return localstate

state = ControllerState()


def updatestate():
    localstate = { 'ElapsedTime':'01:00:00',
    'FixTime':'01:00:00',
    'EtOHTime':'01:00:00',
    'AcetoneTime':'01:00:00',
    'TotalTime':'01:00:00',
    'ServerTime':strftime("%H:%M:%S",localtime())};
    return localstate


@app.route('/PerfusionController/PythonServer/state.json')
def hello():
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/play')
def play():
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/reset')
def reset():
    print updatestate()
    return json.dumps(state.getstate())


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)


