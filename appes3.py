#realizzare un server web che permetta di conoscere capoluoghi di regione.
#l'utente inserisce il nome della regione e il programma restituisce il nome del capoluogo di regione 
#caricare i capoluoghi di regione e le regione in una opportuna struttura dati 
#modificare poi l' esercizio precedente per permettere all' utente di inserire un capoluogo e di avere la regione in cui si trova 
#l' utente sceglie se avere la regione o il capoluogo selezionando un radio button
from flask import Flask,render_template,request
app = Flask(__name__)
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('capoluoghi.html')
{'Lombardia': 'Milano', 'Campania':'Napoli','Lazio':'Roma',
'Basilicata':'Potenza','Abruzzo':'Aquila','Liguria':'Genova',
'Marche':'Ancona','Molise':'Campobasso','Piemonte':'Torino',
'Puglia':'Bari','Sardegna':'Cagliari','Toscana':'Firenze',
'Veneto':'Venezia', 'Trentino-Alto Adige':'Trento',
'Umbria':'Perugia','Valle d Aosta': 'Aosta',
'Emilia-Romagna':'Bologna',
'Friuli-Venezia Giulia':'Trieste','calabria':'Catanzaro','Sicilia':'Palermo'
}   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)