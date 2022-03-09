#realizzare un sito web chhe permetta la registrazione degli utenti 
#l' utente inserisce il nome,username,passsword, la conferma della password e il sesso
#se le informazioni sono corrette il sito salva le informazioni in una struttura dati opportuna 
#prevedere la possibilità di fare il login inserendo username e password 
#se sono corrette fornire un messaggio di benvenuto diverso a seconda del sesso
from flask import Flask,render_template,request
app = Flask(__name__)
lista = []

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('es2.html')

@app.route('/data', methods=['GET'])
def data():
    username = request.args["username"]
    password = request.args["password"]
    name = request.args['Name']
    conferma_password = request.args['conferma_password']
    sex = request.args['Sex']
    if password == conferma_password:
        lista.append({'name':name,'username':username,'password':password,'sex':sex})
        return render_template('login.html')
    else:
        return render_template('errore.html')

@app.route('/login', methods=['GET'])
def login():
    username_log = request.args["username"]
    password_log = request.args["password"]
    for utente in lista:
        if utente['username'] == username_log and utente['password'] == password_log:
            if utente["sex"] == 'M':
                return render_template("welcome.html",nome_user = utente['name'])
            else:
                return render_template("benvenuta.html",nome_user = utente['name'])
            
    return render_template("errore.html",messaggio="username o password errate")        
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)