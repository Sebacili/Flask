
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



quartieri = gpd.read_file("/workspace/Flask/projectfineanno/files/NIL_WM.zip")
alloggiMilano = gpd.read_file("/workspace/Flask/projectfineanno/files/ds593_strutture-ricettive-alberghiere-e-extra-alberghier_cg7c-84a9_final_geojson.zip")

alloggiMilano = alloggiMilano[pd.notnull(alloggiMilano['geo_x'])]



@app.route('/', methods=['GET'])
def HomeP():
  return render_template("homepage.html", quartieri = quartieri.NIL.sort_values(ascending=True)) 

@app.route('/mappapaginainiziale', methods=['GET'])
def mappapaginainiziale():

  
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
    popup = "Name: " + alloggiMilano.iloc[i]['DENOMINAZIONE_STRUTTURA']
    folium.Marker(
      location=[alloggiMilano.iloc[i]['geo_x'], alloggiMilano.iloc[i]['geo_y']],
      popup=popup,
   ).add_to(marker_cluster)

  m.save("templates/mappapagin.html")
  return render_template("mappapagin.html")




@app.route('/servizio2', methods=['GET'])
def servizio2():
  alloggioinput = request.args["namealloggio"]
  if alloggioinput =="":
    return render_template("homepage.html", quartieri = quartieri.NIL)
  else:
    alloggio = alloggiMilano[alloggiMilano["DENOMINAZIONE_STRUTTURA"].str.contains(alloggioinput)]

    nome = alloggio["DENOMINAZIONE_STRUTTURA"].tolist()
    cate = alloggio["CATEGORIA"].tolist()
    ind = alloggio["INDIRIZZO"].tolist()
    quart = alloggio["NIL"].tolist()
    cap = alloggio["CAP"].tolist()
    classifi = alloggio["CLASSIFICAZIONE"].tolist()
    global latserv2, longserv2,nomeserv2
    latserv2 = alloggio["geo_x"].tolist()
    longserv2 = alloggio["geo_y"].tolist()
    nomeserv2 = alloggio["DENOMINAZIONE_STRUTTURA"].tolist()

    return render_template("responseserv2.html", quartieri = quartieri.NIL.sort_values(ascending=True), nome = nome[0], cate = cate[0], ind = ind[0], quart = quart[0], cap = cap[0], classifi = classifi[0]) 



@app.route('/mappaserv2', methods=['GET'])
def mappaserv2():
  m = folium.Map(location=[45.46, 9.20], max_zoom = 18, zoom_start = 12)
  # minimap
  minimap = plugins.MiniMap(toggle_display = True)
  m.add_child(minimap)
  # fullscreem
  plugins.Fullscreen(position="topright").add_to(m)
  # marker
  folium.Marker(location=[latserv2[0], longserv2[0]],popup=nomeserv2[0]).add_to(m)
  m.save("templates/mapserv2.html")
  return render_template("mapserv2.html")























@app.route('/servizio3', methods=['GET'])
def ricerca():

  quartiere = request.args["quartiere"]
  quartiereUtente = quartieri[quartieri["NIL"] == quartiere]
  # prendi gli alloggi all'interno del quartiere
  global Hotelquart
  Hotelquart = alloggiMilano[alloggiMilano.within(quartiereUtente.geometry.squeeze())]

  
  return render_template("responseserv3.html", quartieri = quartieri.NIL)



@app.route('/mappaserv3', methods=['GET'])
def mappaserv3():
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

  m.save("templates/mapserv3.html")
  return render_template("mapserv3.html")





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)