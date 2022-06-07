
from flask import Flask, render_template, send_file, make_response, url_for, Response, request, redirect
app = Flask(__name__)
import pandas as pd

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

##
import folium
from folium import plugins
from folium.plugins import MarkerCluster

# import ipywidgets
# import geocoder
# import geopy
# import numpy as np
# from vega_datasets import data as vds



alloggiMilano = gpd.read_file("/workspace/Flask/projectfineanno/files/ds593_strutture-ricettive-alberghiere-e-extra-alberghier_cg7c-84a9_final_geojson.zip", sep=";")
quartieri = gpd.read_file("/workspace/Flask/projectfineanno/files/NIL_WM.zip")

# alloggiMilano = alloggiMilano[alloggiMilano[['geo_x', 'geo_y']].notna()]
# prende i row che hanno valori nella colonna geo_x
alloggiMilano = alloggiMilano[pd.notnull(alloggiMilano['geo_x'])]


# # sessions
# # import requests module
# import requests
  
# # create a session object
# s = requests.Session()
  
# # make a get request
# s.get('https://httpbin.org / cookies / set / sessioncookie / 123456789')
  
# # again make a get request
# r = s.get('https://httpbin.org / cookies')



# pagina iniziale
@app.route('/', methods=['GET'])
def intro():
  return render_template("whoweare.html") 

# homepage
@app.route('/homepage', methods=['GET'])
def homepage():
  return render_template("homepage.html", quartieri = quartieri.NIL.sort_values(ascending = True)) 


# blocco di cod per la mappa della homepage
@app.route('/mappapaginainiziale', methods=['GET'])
def mappapaginainiziale():
  # crea la mappa
  m = folium.Map(location=[45.46, 9.20], max_zoom = 18, zoom_start = 12, min_zoom=7)
  # minimap
  minimap = plugins.MiniMap(toggle_display = True)
  m.add_child(minimap)
  # fullscreem
  plugins.Fullscreen(position="topright").add_to(m)
  # marker cluster
  marker_cluster = MarkerCluster().add_to(m)
  # marker
  for i in range(0,len(alloggiMilano)):
    #per il popup
    popup = "Name: " + alloggiMilano.iloc[i]['DENOMINAZIONE_STRUTTURA']
    #marker
    folium.Marker(
      location=[alloggiMilano.iloc[i]['geo_x'], alloggiMilano.iloc[i]['geo_y']],
      popup=popup,
   ).add_to(marker_cluster)
   # per salvare la mappa 
  m.save("templates/mappapagin.html")
  return render_template("mappapagin.html")


# link title
@app.route('/changeroute', methods=['GET'])
def changeroute():
  # usato per andare nel html dell'intro
  return render_template("whoweare.html")


# servizio 2
@app.route('/servizio2', methods=['GET'])
def servizio2():
  # prende l'alloggio messo scritto
  alloggioinput = request.args["namealloggio"]
  # controllare se è stato inserito un qualcosa dentro l'input 
  if alloggioinput =="":
    return render_template("homepage.html", quartieri = quartieri.NIL)
  else:
    # cerca nel df l'alloggio con le sue info
    alloggio = alloggiMilano[alloggiMilano["DENOMINAZIONE_STRUTTURA"].str.contains(alloggioinput)]
    # tutto questo serve per la tabella
    nome = alloggio["DENOMINAZIONE_STRUTTURA"].tolist()
    cate = alloggio["CATEGORIA"].tolist()
    ind = alloggio["INDIRIZZO"].tolist()
    quart = alloggio["NIL"].tolist()
    cap = alloggio["CAP"].tolist()
    classifi = alloggio["CLASSIFICAZIONE"].tolist()
    # per la mappa
    global latserv2, longserv2,nomeserv2
    latserv2 = alloggio["geo_x"].tolist()
    longserv2 = alloggio["geo_y"].tolist()
    nomeserv2 = alloggio["DENOMINAZIONE_STRUTTURA"].tolist()

    return render_template("responseserv2.html", quartieri = quartieri.NIL.sort_values(ascending = True), nome = nome[0], cate = cate[0], ind = ind[0], quart = quart[0], cap = cap[0], classifi = classifi[0]) 

# mappa servizio 2
@app.route('/mappaserv2', methods=['GET'])
def mappaserv2():
  # inizializzazione della mappa
  m = folium.Map(location=[45.46, 9.20], max_zoom = 18, zoom_start = 12)
  # minimap
  minimap = plugins.MiniMap(toggle_display = True)
  m.add_child(minimap)
  # fullscreem
  plugins.Fullscreen(position="topright").add_to(m)
  # marker
  folium.Marker(location=[latserv2[0], longserv2[0]],popup=nomeserv2[0]).add_to(m)
  # salvo la mappa
  m.save("templates/mapserv2.html")
  return render_template("mapserv2.html")





# servizio 3
@app.route('/servizio3', methods=['GET'])
def ricerca():
  # prendo il quartiere scelto
  quartiere = request.args["quartiere"]
  # cerco il quartiere nel df di tutti i quartieri per avere la sua geometry
  quartiereUtente = quartieri[quartieri["NIL"] == quartiere]
  # per la mappa 
  global Hotelquart
  # prendi gli alloggi all'interno del quartiere
  Hotelquart = alloggiMilano[alloggiMilano.within(quartiereUtente.geometry.squeeze())]
  return render_template("responseserv3.html", quartieri = quartieri.NIL.sort_values(ascending = True))

# mappa servizio 3
@app.route('/mappaserv3', methods=['GET'])
def mappaserv3():
  # inizializzazione della mappa
  m = folium.Map(location=[45.46, 9.20], max_zoom = 18, zoom_start = 12)
  # minimap
  minimap = plugins.MiniMap(toggle_display = True)
  m.add_child(minimap)
  # marker cluster
  marker_cluster = MarkerCluster().add_to(m)
  # marker
  for i in range(0,len(Hotelquart)):
    iframe = folium.IFrame("Name: " + Hotelquart.iloc[i]['DENOMINAZIONE_STRUTTURA'])
    popup = folium.Popup(iframe, min_width=175, max_width=175)
    # popup = "Name: " + Hotelquart.iloc[i]['DENOMINAZIONE_STRUTTURA']
    folium.Marker(
      location=[Hotelquart.iloc[i]['geo_x'], Hotelquart.iloc[i]['geo_y']],
      popup=popup,
   ).add_to(marker_cluster)
   # salvo la mappa
  m.save("templates/mapserv3.html")
  return render_template("mapserv3.html")


  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)