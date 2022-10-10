from flask import Flask, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.json_util import dumps
import os
import urllib
import json

app = Flask(__name__)

client = MongoClient()

load_dotenv()

mongouri = "mongodb://Admin:" + urllib.parse.quote_plus(os.environ["PSSWD"]) + "@127.0.0.1:27017/"
client = MongoClient(mongouri)

db = client['atizapanCoords']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subcoord')
def subcoord():
    return render_template('coord_submit.html')


@app.route('/subcoord', methods=['POST'])
def postcoord():
    if request.form['b_coords'] == "Subir coordenadas":
        coords = request.form['coords']
        incidents = request.form['incidents']
        db.atizapanCoords.update_one({"Coords":{"$exists": True}}, {"$push":{"Coords":coords}})
        db.atizapanCoords.update_one({"Coords":{"exists": True}}, {"$push":{"Incidents":incidents}})
    elif request.form['b_coords'] == "Borrar primer coordenada":
        db.atizapanCoords.update_one({"Coords":{"$exists": True}}, {"$pop":{"Coords":-1}})
        db.atizapanCoords.update_one({"Coords":{"$exists": True}}, {"$pop":{"Incidents":-1}})
    return "Coordenadas actualizadas"

@app.route('/coords')
def readcoords():
    data = db.atizapanCoords.find()
    list_cur = list(data)
    json_data = dumps(list_cur)
    return json_data
    #coords_str = ""
    #for i in data:
    #    coords_str = i["Coords"]
    #return coords_str


if __name__ == '__main__':
    from waitress import serve
    #app.run(use_reloader=True, port=5000, threaded=True)
    serve(app, host="0.0.0.0", port=5000, url_scheme='https')
