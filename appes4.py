#si vuole realizzare un sito web che permettta di visualizzare alcune informazioni sull' andamento 
#dell' epidemia di covid nel nostro paese a partire da i dati presenti
#nel file 
#l'utente sceglie la regione da un elenco (menù a tendina ),clicca su bottone e il sito deve visualizzare una tabella contenente le informazioni relative a quella regione
# i dati da inserire nel menù a tendina devono essere caricati automaticamente dalla pagina 

from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd 

df = pd.read_csv("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-addizionale-booster.csv")

@app.route('/', methods=['GET'])
def index():
    reg = df['nome_area'].drop_duplicates().to_list()
    return render_template('covid.html', reg=reg)

@app.route('/ris', methods=['GET'])
def risultato():
    regione = request.args['vaccini']
    df3 = df[df['nome_area']== regione]
    return render_template('rispostacovid.html', tables=[df3.to_html()], titles=[''])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)