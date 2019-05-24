from twitch import TwitchClient
import sqlalchemy
from slalchemy import create_engine
from sqlalchemy import Table, Columns, Integer, String, MetaData, ForeignKey

import pandas as pd
import datetime
import time

import threading


def continuous_sql_update():
    '''
    This functions kicks off the SQL database update script
    
    RETURNS:
        engine (sqlalchemy engine): 
    '''
    
    # create v5 client
    client_id = 'o77c1kh7o8s52pt3dtzj8xaypu0699'
    v5_client  = TwitchClient(client_id=client_id)
    
    # create database engine
    metadata = MetaData()
    games = Table('Games', metadata,
                  Column('time', String),
                  Column('game', String),
                  Column('viewers', Integer),
                  Column('streams', Integer)
                 )
    engine = create_engine('sqlite:///twitch.db')
    metadata.create_all(engine)