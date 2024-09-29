from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    d = {"a":2}
    return jsonify(d)