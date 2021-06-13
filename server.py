import random

from flask import Flask, jsonify, request

import evaluator
import getModel

app = Flask(__name__)

@app.route('/')

def index():
    return "Welcome to Anomaly detection server"

global model
model = getModel.get_model(None)
print("Model loaded....................................100%")

def getFileName(frameCount):
    filename = "000.tif" 
    cntstr = str(frameCount)
    if len(cntstr) == 1:
        filename = "00"+cntstr+".tif"
    elif len(cntstr) == 2:
        filename = "0"+cntstr+".tif"
    else:
        filename = cntstr+".tif"
    return filename

@app.route("/getRecustructionCost", methods=["POST"])
def post():
    data = request.json
    filename = getFileName(data["frame"])
    cost = evaluator.getSingleFrameCost(model, filename)
    print(model, data["frame"])
    return jsonify({"rc": cost, "frame": data["frame"]})

if __name__ == '__main__':
    app.run(debug=True)

