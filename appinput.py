from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    return render_template("form.html")

@app.route('/data', methods=['GET'])
def data_page():
    Name = request.args['Name']
    return render_template("welcome.html", Nome = Name)
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)