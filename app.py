from flask import Flask, render_template, request, jsonify
import json
import ast
from flask_cors import CORS
from data_processing import Datasets
from optim_pulp import pulp_optimize

app = Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False

list_values = Datasets().all_values()
data, _, _ = Datasets().read_data()
data = data[data["Sous catégories dépenses"] !="nan"]["Sous catégories dépenses"].tolist()
#data = data[data["Sous catégories dépenses"].notna()]["Sous catégories dépenses"].unique().tolist()

@app.route("/")
def home():
    return render_template("index.html", languages=list_values, data=data)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST' or request.method == 'GET':
        budget = request.form['budget']
        services = request.form.getlist('choix')
        print(services)
        repartitions = pulp_optimize(int(budget), services)
        print(repartitions)
        #return jsonify(repartitions)
        response = jsonify(repartitions)
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response

    else:
        return render_template('after.html')

@app.route('/api/', methods=['GET', 'POST'])
def my_route():
  budget = request.args["budget"]#.get('budget', default = 1200000, type = int)
  services = request.args["services"]#.get('services', default = ["Traiteur", "Photo"], type = str)
  services = ast.literal_eval(services)
  invites = request.args.get('invites', default=100, type=int)
  print(f'services = {services}\nTypes = {type(services)}')
  repartitions = pulp_optimize(int(budget),  services)
  print(repartitions)
  #return jsonify(repartitions)
  response = jsonify(repartitions)
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run(debug=True, port=3000)
