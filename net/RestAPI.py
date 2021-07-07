import urllib
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

# Create some test data for our catalog in the form of a list of dictionaries.
agents = [
    {'id': 0,
     'pos': [650, 300],
     'state': 'AT_NEST',
     'assignedSite': 'hub'},
]

hubInfo = None


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Anthill Search Simulation</h1>'''


@app.route('/getAgents', methods=['GET'])
def getAgents():
    return jsonify(agents)


@app.route('/getHubInfo', methods=['GET'])
def getHubInfo():
    return jsonify(hubInfo)


@app.route('/addAgent', methods=['POST'])
def addAgent():
    # Pull down data and convert binary string to regular string
    data = request.get_data().decode('ascii')

    # Parse data from HTML arguments string to a dictionary
    newAgent = urllib.parse.parse_qs(data)

    # Restructure the data a little bit
    for k, v in newAgent.items():
        newAgent[k] = v[0]

    # Add new book to existing book dictionary
    agents.append(newAgent)
    print("Added new agent: {}".format(newAgent))
    return jsonify(agents)


@app.route('/addHubInfo', methods=['POST'])
def addHubInfo():
    # Pull down data and convert binary string to regular string
    data = request.get_data().decode('ascii')

    newHubInfo = urllib.parse.parse_qs(data)
    hubInfo = newHubInfo
    print("Added hub info: {}".format(hubInfo))
    return jsonify(hubInfo)


app.run()
