from myapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figures
from wrangling_scripts.sql_update import get_sql_connection

@app.route('/')
@app.route('/index')
def index():
    
    figures = return_figures()
    
    db_url = get_sql_connection()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           db_url = db_url,
                           ids=ids,
                           figuresJSON=figuresJSON)