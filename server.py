import pickle
import random

from flask import Flask, jsonify, request

import Config
import evaluator
import getModel

app = Flask(__name__)

@app.route('/')

def index():
    return "Welcome to Anomaly detection server"

model = getModel.get_model(None)
print("Model loaded....................................100%")
with open('./cachedpadding', 'rb') as pickle_file:
    pulpCache = pickle.load(pickle_file)

with open(Config.RESULT_PATH+"/cachedThresholds", 'rb') as pickle_file:
    thresholds = pickle.load(pickle_file)

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
    single_test_case_name = data["test_case"]
    test_set_path = data["test_set_path"]
    cost = float(evaluator.getSingleFrameCost(model, filename, single_test_case_name, test_set_path)) - pulpCache[single_test_case_name]
    return jsonify({"rc": cost, "frame": data["frame"], "threshold": Config.THRESHOLD_VALUE})

if __name__ == '__main__':
    app.run(debug=True)

