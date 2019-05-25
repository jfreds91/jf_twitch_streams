import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Columns, Integer, String, MetaData, ForeignKey

import pandas as pd
import datetime
import time

import threading

import os
import psycopg2


def continuous_sql_update():
    '''
    This functions kicks off the SQL database update script
    
    RETURNS:
        engine (sqlalchemy engine): 
    '''
        
    # create database engine
    DATABASE_URL = os.environ['DATABASE_URL']
    
    metadata = MetaData()
    games = Table('Games', metadata,
                  Column('time', String),
                  Column('game', String),
                  Column('viewers', Integer),
                  Column('streams', Integer)
                 )
    engine = create_engine(DATABASE_URL)
    metadata.create_all(engine)
    
def get_sql_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    return DATABASE_URL
    