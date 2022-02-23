# realizzare un server web che visualizzi l' ora attuale e colori lo sfondo in base all' orario:  un colore per la mattina, uno per il pomeriggio, uno per la sera e uno per la notte
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/",methods=["GET"])
def time():
  hour = datetime.now().hour
  if hour < 7:
    return render_template("orario.html", color = "DarkBlue", testo = "É notte, sono le " + str(hour))
  elif hour < 13:
    return render_template("orario.html", color = "red", testo = "É mattina, sono le " + str(hour))
  elif hour < 18:
    return render_template("orario.html", color = "orange", testo = "É pomeriggio, sono le " + str(hour))
  else:
    return render_template("orario.html", color = "blue", testo = "É sera, sono le " + str(hour))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)