import urllib
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

hubInfo = None
chosenHome = None
simulationDuration = 0


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Anthill Search Simulation</h1>'''


@app.route('/getHubInfo', methods=['GET'])
def getHubInfo():
    return jsonify(hubInfo)


@app.route('/addHubInfo', methods=['POST'])
def addHubInfo():
    # Pull down data and convert binary string to regular string
    data = request.get_data().decode('ascii')

    newHubInfo = urllib.parse.parse_qs(data)
    hubInfo = newHubInfo
    print("Added hub info: {}".format(hubInfo))
    return jsonify(hubInfo)


@app.route('/sendResults', methods=['POST'])
def sendResults():
    data = request.get_data().decode('ascii')

    result = urllib.parse.parse_qs(data)
    print("Sent results: {}".format(result))
    return jsonify(result)


app.run()
