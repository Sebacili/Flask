#Realizzare un sito web che restituisca la mappa dei quartieri di Milano.
#Ci deve essere una homepage con un link "quartieri di milano": cliccando su questo link si deve visualizzare la mappa dei quartieri di Milano.
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

milano = geopandas.read_file("/workspace/Flask/NIL_WM.zip")
fontanelle = geopandas.read_file("/workspace/Flask/Fontanelle (1).zip")


@app.route('/', methods=['GET'])
def home():
    return render_template('home_quartieri.html')

@app.route('/visualizza', methods=("POST", "GET"))
def mappa():
    return render_template('plot.html')

@app.route('/plot.png', methods=['GET'])
def plot_png():
    fig, ax = plt.subplots(figsize = (12,8))

    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.6, edgecolor = "k")
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/ricerca', methods=("POST", "GET"))
def search():
    return render_template('quartiere.html')

@app.route('/quartiereInserito', methods=("POST", "GET"))
def qrtInserito():
    global user
    quartieri = [item for item in milano.NIL]
    user = request.args["Quartiere"]
    if user in quartieri:
        return render_template('plot_quartiere.html')
    else:
        return ("<h1>Errore, il quartiere inserito non esiste</h1>")

@app.route('/quartiereInserito.png', methods=['GET'])
def pngQuartiere():
    mappa_quartiere = milano[milano.NIL == user]

    fig, ax = plt.subplots(figsize = (12,8))
    mappa_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.6, edgecolor = "k")
    contextily.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/scelta', methods=("POST", "GET"))
def scegli():
    quart = milano.NIL
    return render_template('scelta_quartieri.html', quartiere = quart)

@app.route('/immagine_scelta', methods=("POST", "GET"))
def img_scelta():
    global input
    input = request.args["Scelta"]
    return render_template('plot_scelta.html')

@app.route('/scelta.png', methods=['GET'])
def dropdown():
    mappa_quartiere = milano[milano.NIL == input]

    fig, ax = plt.subplots(figsize = (12,8))
    mappa_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.6, edgecolor = "k")
    contextily.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/fontanelle", methods=["GET"])
def fontanelle1():
    return render_template("fontanelle.html", milano= milano["NIL"])

@app.route('/fontanelleres', methods=("POST", "GET"))
def fontanelleRes():
    global imgUtente, fontQuart
    
    quartiereUtente = request.args["Quartiere"]
    imgUtente = milano[milano["NIL"] == quartiereUtente]
    fontQuart = fontanelle[fontanelle.within(imgUtente.geometry.squeeze())]
    print(fontQuart)
    return render_template('fontanelleres.html', PageTitle = "Matplotlib", quartiere=quartiereUtente, tabella = fontQuart.to_html())

@app.route("/fontanelle.png", methods=["GET"])
def Fontanelle():
    fig, ax = plt.subplots(figsize = (12,8))

    imgUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    fontQuart.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)