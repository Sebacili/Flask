#realizzare un serveer web che permetta di effettuare il login 
#l' utente inseririsce username e password
#se lo user name è """admin"" e la password è "xxx123##" il sito ci saluta con messaggio di benvenuto altrimenti messaggio di errore
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    return render_template("login.html")
 @app.route('/data', methods=['GET'])
def data_page():
    nome = request.args['username']
    cognome = request.args['psw']
    if name == "admin" and password == "xxx123##":
        return render_template("login.html" , Nome = nome)
    else:
        return render_template("errore.html") 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)