from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)
import pandas as pd

import io
import geopandas 
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

##
import folium
from folium import plugins
# import ipywidgets
# import geocoder
# import geopy
# import numpy as np
# from vega_datasets import data as vds



quartieri = geopandas.read_file("/workspace/Flask/projectfineanno/files/NIL_WM.zip")
alloggimilano = geopandas.read_file("/workspace/Flask/projectfineanno/files/ds593_strutture-ricettive-alberghiere-e-extra-alberghier_cg7c-84a9_final_geojson.zip")
alloggimilano.dropna(inplace = True)
@app.route('/', methods=['GET'])
def HomeP():
  
  return render_template("homepage.html",quartiere = quartieri["NIL"])

@app.route('/servizio3', methods=['GET'])
def servizio3():
    
    alloggio = request.args["alloggio"]
    alloggioUtente = alloggimilano[alloggimilano["DENOMINAZIONE_STRUTTURA"].str.contains(alloggio)]
  
    return render_template("homepage.html",servizionumero3 = alloggioUtente.to_html(),quartiere = quartieri["NIL"])

@app.route('/mappa', methods=['GET'])
def mappa():
   alloggimilano.dropna()
   
   m = folium.Map(location=[45.5236, 9.6750])
   folium.Marker(
    [45.32, 9.11], popup="<b>Bresso</b>").add_to(m)

   
   m.save("templates/mappaservizio2.html")
   return render_template("mappaservizio2.html")

@app.route('/servizio2', methods=['GET'])
def servizio2():
  quartiere = request.args["quartiere"]
  quartiereUtente = quartieri[quartieri["NIL"] == quartiere]
  Hotelquart = alloggimilano[alloggimilano.within(quartiereUtente.geometry.squeeze())]
  return render_template("homepage.html", tabella = Hotelquart.to_html())









if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)