from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)

import io
import os
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

quartieri = gpd.read_file("/workspace/Flask/NIL_WM.zip")
trasporti = gpd.read_file("/workspace/Flask/tpl_percorsi_shp (4).zip")

@app.route('/', methods = ["GET"])
def homepage():
    return render_template("homeverificac.html")



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)