#1. Realizzare un server web che come home page presenti tre immagini della stessa dimensione una di fianco all'altra. La prima immagine deve avere a che fare con le previsioni del tempo, la seconda deve contenere un libro e la terza deve contenere un calendario. Utilizzare un file css per definire la grafica della pagina.
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
   return render_template("immagini.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)