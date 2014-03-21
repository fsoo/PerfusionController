#!./venv/bin/python -i
from hellotest import app
from controller import state
app.run(debug = True, host='0.0.0.0', port=8080)
