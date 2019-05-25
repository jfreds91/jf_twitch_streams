from flask import Flask

app = Flask(__name__)

from myapp import routes

# import function to run continuous query, start thread
from wrangling_scripts.sql_update import kickoff_sql_thread
kickoff_sql_thread()
