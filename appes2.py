#realizzare un sito web chhe permetta la registrazione degli utenti 
#l' utente inserisce il nome,username,passsword, la conferma della password e il sesso
#se le informazioni sono corrette il sito salva le informazioni in una struttura dati opportuna 
#prevedere la possibilità di fare il login inserendo username e password 
#se sono corrette fornire un messaggio di benvenuto diverso a seconda del sesso
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def casa():
     return render_template("login_appes2.html")

@app.route('/data', methods=['GET'])
def dati():
    Conferma = request.args['Conferma Password']
    Username = request.args['Username']
    password = request.args['Password']
    nome = request.args['Name']
    if password == Conferma :
        if nome == "" or Conferma = "" or password == "" or Username == "": 
            return render_template("errore.html")
            else:
                return render_template("welcome.html",Nome = nome)
if __name__ == '__main__':
app.run(host='0.0.0.0', port=3245, debug=True)