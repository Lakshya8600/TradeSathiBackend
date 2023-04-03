from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def hello_wod():
    return "Helllsdfjsd"


@app.route("/getsuddenpt7", methods=["POST", "GET"])
def hello_world():
    if request.method == "GET":
        with app.app_context():
            with open("Results/suddenpt7.txt", "r") as file:
                val = file.read()
                return val


@app.route("/getsudden2per", methods=["POST", "GET"])
def helo_wrld():
    if request.method == "GET":
        with app.app_context():
            with open("Results/sudden2per.txt", "r") as file:
                val = file.read()
                return val


@app.route("/getvwap", methods=["POST", "GET"])
def helod():
    if request.method == "GET":
        with app.app_context():
            with open("Results/vwap.txt", "r") as file:
                val = file.read()
                return val


@app.route("/getrsi30", methods=["POST", "GET"])
def hello_w():
    if request.method == "GET":
        with app.app_context():
            with open("Results/rsi30.txt", "r") as file:
                val = file.read()
                return val


@app.route("/getrsi70", methods=["POST", "GET"])
def helworld():
    if request.method == "GET":
        with app.app_context():
            with open("Results/rsi70.txt", "r") as file:
                val = file.read()
                return val

@app.route("/minute", methods=["POST", "GET"])
def helwld():
    if request.method == "GET":
        with app.app_context():
            with open("Results/minute.txt", "r") as file:
                val = file.read()
                return val


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
