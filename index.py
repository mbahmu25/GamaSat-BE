from flask import Flask,jsonify
import rasterio
import calculate_raster
app = Flask(__name__)

@app.route("/")
def hello_world():
    citra = calculate_raster.getScenes()
    return jsonify(citra)