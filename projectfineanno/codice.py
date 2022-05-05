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



hotellombardia = pd.read_csv("/workspace/Flask/projectfineanno/files/Lombardia.csv", sep=";", encoding='ISO-8859-1', on_bad_lines='skip')
province = geopandas.read_file("/workspace/Flask/projectfineanno/files/province.zip")
province = province.to_crs(epsg = 4326)

@app.route('/', methods=['GET'])
def HomeP():
  alberghi = hotellombardia[hotellombardia.Categoria == "Alberghiere"]
  return render_template("homepage.html",province=province["DEN_UTS"])

@app.route('/servizio3', methods=['GET'])
def servizio3():
    
    alloggio = request.args["alloggio"]
    alloggioUtente = hotellombardia[hotellombardia["Denominazione struttura"].str.contains(alloggio)]
  
    return render_template("homepage.html",servizionumero3 = alloggioUtente.to_html(), numero = hotellombardia["Telefono"],province=province["DEN_UTS"])

@app.route('/servizio2', methods=['GET'])
def servizio2():
  provincia = request.args["provincia"]
  provinciaUtente = province[province["DEN_UTS"] == provincia]
  HotelProv = province[province.within(hotellombardia.geometry.squeeze())]
  return render_template("homepage.html",provincia = provincia,tabella = HotelProv.to_html())

@app.route('/mappa', methods=['GET'])
def mappa():
  map = folium.map(location =[45,9])
  return map._repr._html_()








if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)