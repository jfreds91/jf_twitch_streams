from myapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figures
from wrangling_scripts.sql_update import get_sql_size


@app.route('/')
@app.route('/index')
def index():
    
    # figures info
    figures = return_figures()
    
    # sql info
    sql_size = get_sql_size()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           sql_size = sql_size,
                           ids=ids,
                           figuresJSON=figuresJSON)