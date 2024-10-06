from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin
import rasterio
import m2m_api
import koord
import calc_raster

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/getScenes/<lat>/<lon>/<cc>",methods=["GET"])
@cross_origin()
def GetScenes(lat,lon,cc):
    if request.method == "GET":
        citra = m2m_api.getScenes(float(lat),float(lon),float(cc))
        return jsonify(citra)

@app.route("/requestDownload")
def reqDownload():
    citra = m2m_api.getScenes(15)
    return jsonify(citra)

@app.route("/satNow",methods=["GET"])
def reqSatPos():
    if request.method == "GET":
        pos = koord.satNow()
        return jsonify(pos)

@app.route("/getStats/<scene>/<lat>/<lon>",methods=["POST","GET"])
@cross_origin()
def getStats(scene,lat,lon):
    if request.method == "GET":
        stats = calc_raster.getRasterStats(scene,float(lat),float(lon))
        return jsonify(stats)