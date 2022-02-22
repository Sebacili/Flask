# realizzare un server web che visualizzi l' ora attuale e colori lo sfondo in base all' orario:  un colore per la mattina, uno per il pomeriggio, uno per la sera e uno per la notte
from flask import Flask,render_template
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date,timedelta
app = Flask(__name__)
today = date.today()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)