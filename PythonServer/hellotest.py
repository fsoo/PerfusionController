from flask import Flask
app = Flask(__name__)

@app.route('/Cochlear/PythonServer/')
def hello():
    return 'Hello World Again!'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)