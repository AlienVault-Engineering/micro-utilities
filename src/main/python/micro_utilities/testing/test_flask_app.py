# coding=utf-8
from flask import Flask

app = Flask("test")
app.config['JSON_ADD_STATUS'] = False


@app.route('/health')
def hello_world():
    return 'so healthy it hurts'

