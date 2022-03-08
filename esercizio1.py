#1. Realizzare un server web che come home page presenti tre immagini della stessa dimensione una di fianco all'altra. La prima immagine deve avere a che fare con le previsioni del tempo, la seconda deve contenere un libro e la terza deve contenere un calendario. Utilizzare un file css per definire la grafica della pagina.
from flask import Flask, render_template
import random
from datetime import datetime
app = Flask(__name__)

@app.route('/', methods=['GET'])
def immagini():
    return render_template("immagini.html")

@app.route('/meteo', methods=['GET'])
def meteo():
  nran = random.randint(0,8)
  if nran <= 2:
        immagine = "static/images/pioggia.jpg"
        previsione = "Piovoso"
  elif nran <= 5:
        immagine = "static/images/nuvoloso.jpg"
        previsione = "Nuvoloso"
  else:
        immagine = "static/images/sole.jpg"
        previsione = "Soleggiato"
  return render_template("previsioni.html", meteo = immagine, testo = previsione)

@app.route('/frasicelebri', methods=['GET'])
def libro():
     frasi = [{"Autore": "Frida Kahlo" , "Frase": "Innamorati di te, della vita e dopo di chi vuoi." },
    {"Autore": "Dietrich Bonhoeffer" , "Frase": "Contro la stupidità non abbiamo difese."},
    {"Autore": "Charlie Chaplin" , "Frase": "Un giorno senza un sorriso è un giorno perso."},{"Autore": "Francesco Bacone" , "Frase": "Sapere è potere."},
    {"Autore": "Italo Calvino" , "Frase": "Il divertimento è una cosa seria."},{"Autore": "Lewis Carroll" , "Frase": "Qui siamo tutti matti."},
    {"Autore": "Johann Wolfgang von Goethe", "Frase": "Il dubbio cresce con la conoscenza."},{"Autore": "Luis Sepùlveda" , "Frase": "Vola solo chi osa farlo."},
    {"Autore": "Lucio Anneo Seneca", "Frase": "Se vuoi essere amato, ama."},{"Autore": "Voltaire", "Frase": "Chi non ha bisogno di niente non è mai povero."}]
    fraserandom = random.randint(0,9)
    return render_template("frasicelebri.html", autore = frasi[fraserandom]["Autore"], frase = frasi[fRandom]["Frase"])
@app.route("/quantomanca")
def calendario():
    now = datetime.now()
    school = datetime(2022,6,8)
    return render_template("calendario.html", data = (school - now).days)
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)