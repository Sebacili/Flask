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

@app.route('/', methods=['GET'])
def HomeP():
  
  return render_template("homepage.html",quartieri1 = quartieri["NIL"])

@app.route('/servizio3', methods=['GET'])
def servizio3():
    
    alloggio = request.args["alloggio"]
    alloggioUtente = alloggimilano[alloggimilano["DENOMINAZIONE_STRUTTURA"].str.contains(alloggio)]
  
    return render_template("homepage.html",servizionumero3 = alloggioUtente.to_html(),quartieri1 = quartieri["NIL"])



@app.route('/mappa', methods=['GET'])
def mappa():
  map = folium.map(location =[45,9])
  return map._repr._html_()








if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)