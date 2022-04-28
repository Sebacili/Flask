from flask import Flask, render_template, send_file, make_response, url_for, Response, request
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
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster


alloggilombardia = pd.read_csv("/workspace/Flask/projectfineanno/files/Lombardia.csv", sep=";", encoding='ISO-8859-1', on_bad_lines='skip')

@app.route('/', methods=['GET'])
def HomeP():
    map = folium.Map(location = [13.406,80.110])
    return map._repr_html_()

  







if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)