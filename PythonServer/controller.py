import json;
from datetime import datetime, timedelta;
from math import ceil,floor;
from flask import render_template

def ftime(s):
    hours, remainder = divmod(s, 3600);
    minutes, seconds = divmod(remainder, 60);
    return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)



MAXFIXTIME = 24*60*60 #won't fix for more than 24 hours
MAXETOHTIME = 24*60*60 #don't ETOH for more than 24 hour
MAXACETONETIME = 24*60*60 #don't ETOH for more than 24 hour

MAXFLOWRATE = 10 # 10 ml/min


class ControllerState :
    
    def __init__(self):
        self.StartTime= 0 ;
        self.ElapsedTime = timedelta(seconds=0);
        self.RemainingTime = timedelta(seconds=0);
        self.FixTime = timedelta(seconds = 10);
        self.EtOHTime = timedelta(seconds = 10);
        self.AcetoneTime = timedelta(seconds = 10); # 15 minutes
        self.PlayPauseState = "Pause"
        self.ProcessStep = "Fix";
        
        
        self.FixFlowRate = 1;
        self.EtOHRinseFlowRate = 10;
        self.AcetoneRinseFlowRate = 10;
        self.StirBar = 0;
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
        localstate = {
            'PlayPauseState':"Pause",
            
            'ElapsedTime': 0,
            'RemainingTime': 0,
            'FixTime': 0,
            'EtOHTime': 0,
            'AcetoneTime': 0,
            'ServerTime': 0,
            'ServerTimeString': 'blah',
            'ProcessStep':'blah',
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
        
        if(self.Paused):
            localstate['PlayPauseState'] = "Pause";
        else:
            localstate['PlayPauseState'] = "Play";
        localstate['ElapsedTime'] = ftime(self.ElapsedTime.seconds);
        remtime =(self.FixTime +self.EtOHTime + self.AcetoneTime - self.ElapsedTime);
        
        if remtime < timedelta(seconds = 0):
            remtime = timedelta(seconds = 0);
        
        
        localstate['RemainingTime'] = ftime(int(ceil(remtime.seconds+float(remtime.microseconds)/10**6)));
        
        localstate['FixTime']=self.FixTime.seconds;
        localstate['EtOHTime']=self.EtOHTime.seconds;
        localstate['AcetoneTime']=self.AcetoneTime.seconds;
        localstate['ServerTimeString']=datetime.today().strftime("%H:%M:%S");
        localstate['ProcessStep'] = self.ProcessStep;
        
        localstate['FixFlowRate'] = self.FixFlowRate;
        localstate['EtOHRinseFlowRate'] = self.EtOHRinseFlowRate;
        localstate['AcetoneRinseFlowRate'] = self.AcetoneRinseFlowRate;
        localstate['StirBar'] = self.StirBar;
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
        
        # if paused
        if self.Paused:
            self.PlayPauseState = "Pause";
        else:
            self.PlayPauseSTate = "Play";
            self.ElapsedTime  = datetime.today() - self.StartTime;
        
        
        # running a program now - calculate the state from the elapsed time, and over-ride any user state changes
        # based on elapsed time, figure out which stage we're in (fix, etoh, acetone, wait)
        if(self.ElapsedTime < self.FixTime): # in fix stage
            self.ProcessStep = "Fix";
            # no acetone flows in this stage; ETOH gradually approaches 100% of the flow
            self.AcetoneFlowRate = 0;
            self.EtOHFlowRate = self.FixFlowRate * float(self.ElapsedTime.seconds) / float(self.FixTime.seconds);
            self.H2OFlowRate = self.FixFlowRate * (1.0-float(self.ElapsedTime.seconds) / float(self.FixTime.seconds));
        
        elif self.ElapsedTime < self.FixTime+self.EtOHTime: # in ETOH stage
            self.ProcessStep = "EtOHRinse";
            
            # no acetone or H2O - 100% ethanol at ethanol flow rate
            self.AcetoneFlowRate = 0;
            self.H2OFlowRate = 0;
            self.EtOHFlowRate = self.EtOHRinseFlowRate;
        
        
        
        elif self.ElapsedTime < self.FixTime+self.EtOHTime+self.AcetoneTime: # in acetone stage
            self.ProcessStep = "AcetoneRinse";
            # no acetone or H2O - 100% ethanol at ethanol flow rate
            self.AcetoneFlowRate = self.AcetoneRinseFlowRate;
            self.H2OFlowRate = 0;
            self.EtOHFlowRate = 0;
        
        else: # after end
            self.ProcessStep = "End";
            self.H2OFlowRate = 0;
            self.EtOHFlowRate = 0;
            self.AcetoneFlowRate = 0;
        
        #calculate valve on and off based on duty cycles
        
        return
    def playpause(self):
        if self.Paused: # record the start time, then set flag to run
            self.StartTime = datetime.today()-self.ElapsedTime;
            self.Paused=False;
        else:
            self.Paused=True; # pause the process
        self.updatestate();
    
    def reset(self): # set elapsed time to zero, turn on pause flag
        self.Pauseld = True;
        self.ElapsedTime=timedelta(seconds=0);
        self.StartTime=datetime.today();
        self.updatestate();
    
    def setparameters(self, parameters):
        
        p=parameters.get('name');
        value=int(parameters.get('value'));
        print "received message, set "+p+" to " +repr(value);

        if p==u'FixTime':
            if value >= 0 and value < MAXFIXTIME:
                print "setting "+p+" to "+repr(value);
                self.FixTime = timedelta(seconds=value);
        elif p==u'EtOHTime':
            if value >= 0 and value < MAXETOHTIME:
                self.EtOHTime = timedelta(seconds=value);
        elif p==u'AcetoneTime':
            if value >= 0 and value < MAXETOHTIME:
                self.AcetoneTime = timedelta(seconds=value);


        elif p==u'FixFlowRate':
            if value >= 0 and value < MAXFLOWRATE:
                print "setting "+p+" to "+repr(value);
                self.FixFlowRate = value;
        elif p==u'EtOHRinseFlowRate':
            if value >= 0 and value < MAXFLOWRATE:
                self.EtOHRinseFlowRate = value;
        elif p==u'AcetoneFlowRate':
            if value >= 0 and value < MAXFLOWRATE:
                self.AcetoneRinseFlowRate= value;

        elif p==u'StirBar':
            if value >= 0 and value <=1:
                print "setting "+p+" to "+repr(value);
                
                self.StirBar= value;


        self.updatestate();


    def render_templates(self):
        
        localstate = {
            'FixTime': 0,
            'EtOHTime': 0,
            'AcetoneTime': 0,
        
        };
        localstate['FixTime']= render_template("templates.html");
        localstate['EtOHTime']= render_template("templates.html");
        localstate['AcetoneTime']= render_template("templates.html");
        return localstate


state = ControllerState()


