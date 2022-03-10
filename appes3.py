#realizzare un server web che permetta di conoscere capoluoghi di regione.
#l'utente inserisce il nome della regione e il programma restituisce il nome del capoluogo di regione 
#caricare i capoluoghi di regione e le regione in una opportuna struttura dati 
#modificare poi l' esercizio precedente per permettere all' utente di inserire un capoluogo e di avere la regione in cui si trova 
#l' utente sceglie se avere la regione o il capoluogo selezionando un radio button
from flask import Flask, render_template, request
app = Flask(__name__)
capoluoghiRegione = {"Abruzzo" :"L'Aquila", "Basilicata" : "Potenza", "Calabria" : "Catanzaro", "Campania" : "Napoli", "Emilia-Romagna" :"Bologna", "Friuli-Venezia" : "Trieste", "Lazio" :	"Roma", "Liguria" :	"Genova", "Lombardia" :	"Milano", "Marche" : "Ancona", "Molise" :	"Campobasso", "Piemonte"	: "Torino", "Puglia" :	"Bari", "Sardegna" :	"Cagliari", "Sicilia" :	"Palermo", "Toscana"	: "Firenze", "Trentino-Alto Adige" :	"Trento", "Umbria" :	"Perugia", "Valle d'Aosta" :	"Aosta", "Veneto" :	"Venezia" }


@app.route('/', methods=['GET'])
def home_page():
    return render_template("Scelta.html")

@app.route('/data', methods=['GET'])
def Data():
    scelta = request.args["Scelta"]
    if scelta == "Regione":
        return render_template("capoluoghi.html")
    else:
        return render_template("regioni.html")
    

@app.route("/dataReg", methods=["GET"])
def dataReg():
    regione = request.args["Regione"]
    for key, value in capoluoghiRegione.items():
        if regione == key:
            capoluogo = value
            return render_template("risposta.html", ris = capoluogo)
    return render_template("errore.html")

@app.route("/dataCap", methods=["GET"])
def dataCap():
    capoluogo = request.args["Capoluogo"]
    for key, value in capoluoghiRegione.items():
        if capoluogo == value:
             regione = key
             return render_template("risposta.html", ris = regione)
    return render_template("errore.html")



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)