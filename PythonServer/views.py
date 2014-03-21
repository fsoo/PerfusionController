from flask import render_template
from flask_wtf import Form
from wtforms import SelectField
from flask import request

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


# forms handling



class ProcessTimeForm(Form):
    timing = SelectField(u'Time',choices=[{'3600','1:00:00','3600','1:00:00','3600','1:00:00','3600','1:00:00'}]);


@app.route('/PerfusionController/PythonServer/forms')
def fixtimeform():
    return  json.dumps(state.render_templates());


@app.route('/PerfusionController/PythonServer/updateparameters', methods =['POST', 'GET'])
def setparameters():
    print request.form;
    state.setparameters(request.form);
    
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/preset', methods =['POST', 'GET'])
def setpreset():
    state.processpresetmessage(request.form);
    return json.dumps(state.getstate())

@app.route('/PerfusionController/PythonServer/presetselector')
def presetselector():
    return  json.dumps(state.render_presetselector());
