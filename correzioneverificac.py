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
linee = gpd.read_file("/workspace/Flask/tpl_percorsi_shp (4).zip")

@app.route('/', methods = ["GET"])
def homepage():
    return render_template("homeverificac.html")


@app.route("/selezione", methods=["GET"])
def selezione():
    scelta = request.args["scelta"]
    if scelta == "es1":
        return redirect(url_for("input"))
    elif scelta == "es2":
        return redirect(url_for("ricerca"))
    else:
        return redirect(url_for("mappa"))

@app.route("/input", methods=["GET"])
def input():
    return render_template("inputverificac.html")

@app.route("/elenco", methods=["GET"])
def elenco():
    Min = min(float(request.args["val1"]), float(request.args["val2"]))
    Max = max(float(request.args["val1"]), float(request.args["val2"]))
    linee_distanza = linee[(linee["lung_km"] > Min) & (linee["lung_km"] < Max)].sort_values("linea")
    return render_template("elencoverificac.html", tabella = linee_distanza.to_html())

@app.route("/ricerca", methods=["GET"])
def ricerca():
    return render_template("ricercaverificac.html")

@app.route("/lineequart", methods=["GET"])
def lineequart():
    quartiere = request.args["quartiere"]
    quartiereUtente = quartieri[quartieri["NIL"].str.contains(quartiere)]
    linee_quartiere = linee[linee.intersects(quartiereUtente.geometry.squeeze())].sort_values("linea")
    return render_template("lineequartverificac.html", tabella = linee_quartiere.to_html())

@app.route("/mappa", methods=["GET"])
def mappa():
    return render_template("tendinaverificac.html", linee = linee["linea"].drop_duplicates().sort_values(ascending=True))

@app.route("/linea", methods=["GET"])
def linea():
    global lineeUtente
    linea = int(request.args["linea"])
    lineeUtente = linee[linee["linea"] == linea]
    return render_template("mappaverificac.html", linea = linea)

@app.route("/mappa.png", methods=["GET"])
def mappapng():
    fig, ax = plt.subplots(figsize = (12,8))

    lineeUtente.to_crs(epsg=3857).plot(ax=ax, edgecolor="k")
    quartieri.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)