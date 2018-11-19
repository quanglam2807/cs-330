from flask import Flask
from flask import redirect, url_for
from flask import request, make_response
from flask import render_template
import records

app = Flask(__name__)

db = records.Database("postgresql://lamqu01:@knuth.luther.edu/world")

@app.route('/')
def index():
    return redirect(url_for('country'))

@app.route('/country', methods=['GET', 'POST'])
def country():
    optionsQuery = db.query("select code, name from country")
    if request.method == 'POST':
        code = request.form['code']
        resultsQuery = db.query("select *, city.name as capitalname from country left join city on country.capital = city.id where code='" + code + "' ")
        return render_template("shared.html", code=code, options=optionsQuery.all(), results=resultsQuery.all())
    return render_template("shared.html", options=optionsQuery.all())

@app.route('/region', methods=['GET', 'POST'])
def region():
    optionsQuery = db.query("select distinct region, region as dupregion from country")

    if request.method == 'POST':
        code = request.form['code']
        resultsQuery = db.query("select *, city.name as capitalname from country left join city on country.capital = city.id where region='" + code + "' ")
        return render_template("shared.html", code=code, options=optionsQuery.all(), results=resultsQuery.all())
    return render_template("shared.html", options=optionsQuery.all())

@app.route('/continent', methods=['GET', 'POST'])
def continent():
    optionsQuery = db.query("select distinct continent, continent as dupcontinent from country")

    if request.method == 'POST':
        code = request.form['code']
        resultsQuery = db.query("select *, city.name as capitalname from country left join city on country.capital = city.id where continent='" + code + "' ")
        return render_template("shared.html", code=code, options=optionsQuery.all(), results=resultsQuery.all())
    return render_template("shared.html", options=optionsQuery.all())





if __name__ == '__main__':
    app.run()
