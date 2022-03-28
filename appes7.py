from flask import Flask, render_template, request, send_file, make_response, url_for, Response
app = Flask(__name__)
import io
import geopandas
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
regioni = geopandas.read_file("/workspace/Flask/regioni.zip")
province = geopandas.read_file("/workspace/Flask/province.zip")
comuni = geopandas.read_file("/workspace/Flask/comuni.zip")

@app.route("/", methods=["GET"])
def home():
    return render_template("radReg.html", regioni = regioni["DEN_REG"])



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)