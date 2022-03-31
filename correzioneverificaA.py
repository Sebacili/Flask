from flask import Flask,render_template,request,send_file,make_response, url_for, Response,redirect
app = Flask(__name__)
import io
import geopandas
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
stazioni = pd.read_csv("/workspace/Flask/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv" ,sep = ";")
@app.route('/', methods=['GET'])
def home():
    return render_template("homeverifica1.html")

@app.route('/numero', methods=['GET'])
def numero():
#numero stazioni per ogni municio
    global risultato
    risultato = stazioni.groupby("MUNICIPIO")["OPERATORE"].count().reset_index()
    return render_template("link1.html",risultato = risultato.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    
    fig, ax = plt.subplots(figsize = (12,8))
    x = risultato.MUNICIPIO
    y = risultato.OPERATORE
    ax.bar(x,y,color = "#304C89")
    plt.xlabel("MUNICIPIO")
    plt.ylabel("OPERATORE")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta == "es1":
        return redirect(url_for("numero"))
    elif scelta == "es2":
        return redirect(url_for("input"))
    else:
        return redirect(url_for("dropdown"))
    return render_template("a.html")
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)