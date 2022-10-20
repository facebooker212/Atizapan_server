from flask import Flask, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.json_util import dumps
from flask_bootstrap import Bootstrap
import subprocess
import datetime
import os
import urllib
import json

app = Flask(__name__)
Bootstrap(app)

# Initialize client
client = MongoClient()

# Load environment variables
load_dotenv()

# Create connection to mongoDB
mongouri = "mongodb://Admin:" + urllib.parse.quote_plus(os.environ["PSSWD"]) + "@127.0.0.1:27017/"
client = MongoClient(mongouri)

db = client['atizapanCoords']


# Default page
@app.route('/')
def index():
    return render_template('index.html')


# Submit information
@app.route('/subcoord')
def subcoord():
    return render_template('coord_submit.html')


def currentTime():
    x = datetime.datetime.now()
    return x.minute


# Handle POST request from /subcoord
@app.route('/subcoord', methods=['POST'])
def postcoord():
    if request.form['b_coords'] == "Subir datos" and request.form['pin'] == os.environ["PIN"]:
        coords = request.form['coords']
        incidents = request.form['incidents']
        notifications = request.form['notifications']
        if (coords == ""):
            return "No dejar el campo coordenadas vacio"
        else:
            proc = subprocess.Popen("php notify.php " + "\"" + notifications + "\"", shell=True, stdout=subprocess.PIPE)
            script_response = proc.stdout.read()
            db.atizapanCoords.update_one({"Coords": {"$exists": True}},
                                         {"$push": {"Coords": coords,
                                                    "Incidents": incidents,
                                                    "Notifications": notifications,
                                                    "Time": currentTime()}})
            db.atizapanCoords.update_one({"Incidents": {"$exists": True}},
                                         {"$push": {"Incidents": ""}})
            return "Coordenadas actualizadas"
    elif request.form['b_coords'] == "Borrar primer coordenada" and request.form['pin'] == os.environ["PIN"]:
        db.atizapanCoords.update_one({"Coords": {"$exists": True}},
                                     {"$pop": {"Coords": -1,
                                               "Incidents": -1,
                                               "Notifications": -1,
                                               "Time": -1}})
        db.atizapanCoords.update_one({"Incidents": {"$exists": True}},
                                     {"$pop": {"Incidents": -1}})
        return "Primer coordenada eliminada"
    return "PIN incorrecto"


# Return DB query
@app.route('/coords')
def readcoords():
    data = db.atizapanCoords.find()
    list_cur = list(data)
    json_data = dumps(list_cur)
    return json_data


if __name__ == '__main__':
    from waitress import serve
    app.run(use_reloader=True, port=5000, threaded=True)
    #serve(app, host="0.0.0.0", port=5000, url_scheme='https')
