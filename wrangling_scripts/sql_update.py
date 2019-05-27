import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect

import pandas as pd
import datetime
import time

import threading

import os
import psycopg2

from wrangling_scripts.twitch_api_funcs import get_top_games


def get_sql_engine(DATABASE_URL=None):
    '''
    This functions kicks off the SQL database update script
    
    RETURNS:
        engine (sqlalchemy engine): 
    '''
        
    # create database engine
    if DATABASE_URL is None:
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
    
    #inspector = inspect(engine)
    #return inspector.get_columns('Games')
    
    return engine
    
    
def kickoff_sql_thread(DATABASE_URL, max_size = 9000):
    '''
    This function starts a thread which continuously updates the sql database
    This function is to be run once the app has compiled, one time
    
    INPUTS:
        max_size (int): maximum number of allowable rows in database
        sleep_time (int): number of seconds between twitch queries
    RETURNS: none
    '''
    
    print('############## starting kickoff_sql_thread ###############')
    
    def check_table_size(engine, max_size):
    # this function checks the number of rows in the table and deletes the oldest entires
    # if over max_size threshold
        c = engine.execute('SELECT COUNT(*) FROM "Games";')
        num_rows = int(c.fetchall()[0][0])
        c.close()
        #print('table contains {} rows'.format(num_rows))

        while num_rows >= max_size:
            #print('\tmax table size reached, deleting oldest entries')
            df = pd.read_sql_table('Games', con = engine)
            df['time'] = pd.to_datetime(df['time'])
            mintime = df['time'].min().strftime('%Y-%m-%d %H:%M:%S.%f')

            del_statement = games.delete().where(games.c.time == mintime)
            connection = engine.connect()
            connection.execute(del_statement)
            connection.close()

            c = engine.execute('SELECT COUNT(*) FROM "Games"')
            num_rows = c.fetchall()[0][0]
            c.close()
            
            return num_rows

    try:
        # prepare to start thread
        engine = get_sql_engine(DATABASE_URL = DATABASE_URL) # worker appears to  be unable to get engine because database is not in local env vars
        
        while True:

            num_rows = check_table_size(engine, max_size)

            print('############################## Querying API #################################')
            df = get_top_games()
            df.to_sql('Games', engine, index=False, if_exists = 'append')
            #time.sleep(sleep_time)
    except Exception as e:
        print(e)
        #print('num_rows = {}, type = {}'.format(num_rows, type(num_rows)))
        #print('max_size = {}, type = {}'.format(max_size, type(max_size)))

    
def get_sql_size():
    engine = get_sql_engine()
    
    c = engine.execute('SELECT COUNT(*) FROM "Games";')
    num_rows = c.fetchall()[0][0]
    c.close()
    
    return num_rows