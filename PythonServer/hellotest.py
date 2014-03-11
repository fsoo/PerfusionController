from flask import Flask
app = Flask(__name__)

import json
import threading
paused=0;

from datetime import datetime, timedelta;

class ControllerState :
    
    def __init__(self):
        self.StartTime=0;
        self.ElapsedTime = timedelta(seconds=0);
        self.FixTime = timedelta(seconds = 10);
        self.EtOHTime = timedelta(seconds = 10);
        self.AcetoneTime = timedelta(seconds = 10); # 15 minutes
        self.CurrentState = "Pause";
        
        
        self.FixFlowRate = 1;
        self.EtOHRinseFlowRate = 10;
        self.AcetoneRinseFlowRate = 10;
        self.Stirbar = 0;
        self.AlertEmail = "";
        
        self.H2OFlowRate = 0; # ml/min
        self.EtOHFlowRate = 0; # ml/min
        self.AcetoneFlowRate = 0; # ml/min

        self.H2OValveOpen = False;
        self.EtOHValveOpen = False;
        self.AcetoneValveOpen = False;
        self.WasteValveOpen = False;
        
        self.H2OLevel = 0;
        self.EtOHLevel = 0;
        self.AcetoneLevel = 0;
        self.WasteLevel = 0;
        
        
        self.Valvecycletime = 10; # 10 seconds
        self.Paused = True; # starts by not running
        self.ServerTime = datetime.today().strftime("HH:MM:SS"); # initialize to local time
        
    def getstate(self):
        self.updatestate();
        localstate = { 'ElapsedTime': 0,
            'FixTime': 0,
            'EtOHTime': 0,
            'AcetoneTime': 0,
            'ServerTime': 0,
            'ServerTimeString': 'blah',
            'CurrentState':'blah',
            'FixFlowRate': 0,
            'EtOHRinseFlowRate' : 0,
            'AcetoneRinseFlowRate':0,
            'StirBar':0,
            'H2OFlowRate':0,
            'EtOHFlowRate':0,
            'AcetoneFlowRate':0,
            'H2OValveOpen':0,
            'EtOHValveOpen':0,
            'AcetoneValveOpen':0,
            'WasteValveOpen':0,
            'H2OLevel':0,
            'EtOHLevel':0,
            'AcetoneLevel':0,
            'WasteLevel':0

        }
        
        localstate['ElapsedTime'] = self.ElapsedTime.seconds;
        localstate['FixTime']=self.FixTime.seconds;
        localstate['EtOHTime']=self.EtOHTime.seconds;
        localstate['AcetoneTime']=self.AcetoneTime.seconds;
        localstate['ServerTimeString']=datetime.today().strftime("%H:%M:%S");
        localstate['CurrentState'] = self.CurrentState;
        
        localstate['FixFlowRate'] = self.FixFlowRate;
        localstate['EtOHRinseFlowRate'] = self.EtOHRinseFlowRate;
        localstate['AcetoneRinseFlowRate'] = self.AcetoneRinseFlowRate;
        localstate['StirBar'] = self.Stirbar;
        localstate['H2OFlowRate'] = self.H2OFlowRate;
        localstate['EtOHFlowRate'] = self.EtOHFlowRate;
        localstate['AcetoneFlowRate'] = self.AcetoneFlowRate;
        localstate['H2OValveOpen'] = self.H2OValveOpen;
        localstate['EtOHValveOpen'] = self.EtOHValveOpen;
        localstate['AcetoneValveOpen'] = self.AcetoneValveOpen;
        localstate['WasteValveOpen'] = self.WasteValveOpen;
        localstate['H2OLevel'] = self.H2OLevel;
        localstate['EtOHLevel'] = self.EtOHLevel;
        localstate['AcetoneLevel'] = self.AcetoneLevel;
        localstate['WasteLevel'] = self.WasteLevel;
        
        
        return localstate;

    def updatestate(self):
        #regardless of paused or unpaused, set the wall clock
        self.ServerTime = datetime.today();
        
        # if paused, don't do anything
        if self.Paused:
            self.CurrentState = "Pause";
            
            return
        else:
            self.ElapsedTime = datetime.today() - self.StartTime;
            # running a program now - calculate the state from the elapsed time, and over-ride any user state changes
            # based on elapsed time, figure out which stage we're in (fix, etoh, acetone, wait)
            if(self.ElapsedTime < self.FixTime): # in fix stage
                self.CurrentState = "Fix";
                # no acetone flows in this stage; ETOH gradually approaches 100% of the flow
                self.AcetoneFlowRate = 0;
                self.EtOHFlowRate = self.FixFlowRate * float(self.ElapsedTime.seconds) / float(self.FixTime.seconds);
                self.H2OFlowRate = self.FixFlowRate * (1.0-float(self.ElapsedTime.seconds) / float(self.FixTime.seconds));
                
            elif self.ElapsedTime < self.FixTime+self.EtOHTime: # in ETOH stage
                self.CurrentState = "EtOHRinse";
                
                # no acetone or H2O - 100% ethanol at ethanol flow rate
                self.AcetoneFlowRate = 0;
                self.H2OFlowRate = 0;
                self.EtOHFlowRate = self.EtOHRinseFlowRate;
                
            
            
            elif self.ElapsedTime < self.FixTime+self.EtOHTime+self.AcetoneTime: # in acetone stage
                self.CurrentState = "AcetoneRinse";
                # no acetone or H2O - 100% ethanol at ethanol flow rate
                self.AcetoneFlowRate = self.AcetoneRinseFlowRate;
                self.H2OFlowRate = 0;
                self.EtOHFlowRate = 0;
            
            else: # after end
                self.CurrentState = "End";
                self.H2OFlowRate = 0;
                self.EtOHFlowRate = 0;
                self.AcetoneFlowRate = 0;
    
        #calculate valve on and off based on duty cycles
    
        return
    def play(self):
        if self.Paused: # record the start time, then set flag to run
            self.StartTime = datetime.today()-self.ElapsedTime;
            self.Paused=False;
        self.updatestate();

    def pause(self): # set pause flag on
        if not self.Paused:
            self.Paused=True;
        self.updatestate();

    def reset(self): # set elapsed time to zero, turn on pause flag
        self.Pauseld = True;
        self.ElapsedTime=timedelta(seconds=0);
        self.StartTime=datetime.today();
        self.updatestate();


state = ControllerState()

@app.route('/PerfusionController/PythonServer/state.json')
def getstate():
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/play')
def play():
    state.play();
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/pause')
def pause():
    state.pause();
    return json.dumps(state.getstate())


@app.route('/PerfusionController/PythonServer/reset')
def reset():
    state.reset();
    return json.dumps(state.getstate())


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)


