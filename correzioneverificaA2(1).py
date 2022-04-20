from flask import Flask, render_template, request, send_file, make_response, url_for, Response, redirect
app = Flask(__name__)
import io
import geopandas
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

comuni = geopandas.read_file("/workspace/Flask/NIL_WM.zip")
provincie = geopandas.read_file("/workspace/Flask/province.zip")
regioni = geopandas.read_file("/workspace/Flask/regioni.zip")
ripartizioni = geopandas.read_file("/workspace/Flask/georef-italy-ripartizione-geografica (1).geojson")

@app.route('/', methods=['GET'])
def home():
    return render_template("homeverifica2(1).html")

@app.route('/input', methods=['GET'])
def input():
    return render_template("inputverifica2(1).html")


@app.route('/comProv', methods=['GET'])
def comProv():
    global comuni_prov, mappa_prov
    provincia = request.args['Prov']

    mappa_prov = provincie[provincie['DEN_PROV'] == provincia]
    comuni_prov = comuni[comuni.within(mappa_prov.geometry.squeeze())]
    area = mappa_prov.geometry.area
    return render_template("comProverifica2(1).html", text = area)

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))

    mappa_prov.to_crs(epsg=3857).plot(ax=ax, alpha=0.2, edgecolor = "k")
    comuni_prov.to_crs(epsg=3857).plot(ax=ax, alpha=0.4, edgecolor = "r")
    contextily.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/dropdownReg', methods=['GET'])
def dropReg():
    return render_template("dropdownRegverifica2(1).html", regioni2 = regioni["DEN_REG"].sort_values(ascending = True))

@app.route('/dropdownProv', methods=['GET'])
def dropProv():
    regione = request.args['Regione']

    mappa_regione = regioni[regioni['DEN_REG'] == regione]
    prov_regione = provincie[provincie.within(mappa_regione.geometry.squeeze())]
    return render_template("dropdownProverifica2(1).html", province2 = prov_regione["DEN_PROV"].sort_values(ascending = True))

@app.route('/dropdownRip', methods=['GET'])
def dropRip():
    return render_template("dropdownRipverifica2(1).html", ripartizioni2 = ripartizioni["rip_name"].sort_values(ascending = True))

@app.route('/regRip', methods=['GET'])
def regRip():
    ripartizione = request.args['Ripartizione']

    mappa_rip = ripartizioni[ripartizioni['rip_name'] == ripartizione]
    reg_rip = regioni[regioni.within(mappa_rip.geometry.squeeze())]
    return render_template("regRipverifica2(1).html", regioni2 = reg_rip["DEN_REG"].sort_values(ascending = True))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)