from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')

def index():
    return "Welcome to Anomaly detection server"

@app.route("/getRecustructionCost", methods=["GET"])
def get():
    return jsonify({"rc": 100})

if __name__ == '__main__':
    app.run(debug=True)

