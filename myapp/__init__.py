from flask import Flask

app = Flask(__name__)

from myapp import routes

# import function to run continuous query, start thread
from wrangling_scripts.sql_update import get_sql_engine
