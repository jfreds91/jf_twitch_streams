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


def get_sql_engine():
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
    
    #inspector = inspect(engine)
    #return inspector.get_columns('Games')
    
    return engine
    
def kickoff_sql_thread(max_size = 9000, sleep_time = 900):
    '''
    This function starts a thread which continuously updates the sql database
    This function is to be run once the app has compiled, one time
    
    INPUTS:
        max_size (int): maximum number of allowable rows in database
        sleep_time (int): number of seconds between twitch queries
    RETURNS: none
    '''
    
    def check_table_size(engine, max_size):
    # this function checks the number of rows in the table and deletes the oldest entires
    # if over max_size threshold
        c = engine.execute("SELECT COUNT(*) FROM Games")
        num_rows = c.fetchall()[0][0]
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

            c = engine.execute("SELECT COUNT(*) FROM Games")
            num_rows = c.fetchall()[0][0]
            c.close()
        
    
    def constant_query(engine, max_size, sleep_time):
        '''
        function which continuously adds to the Games table using the given SQL engine

        INPUTS:
            v5_client: the twitch v5 client
            engine: sql alchemy database engine
            max_size (int): the size at which the function begins deleting rows. Note that the actual
                            size of the database will be max_size + query num (10)
            sleep_time (int): the API query interval in seconds
        '''

        while True:
            if stop_threads:
                break

            check_table_size(engine, max_size)
            df = get_top_games() # this function is from twitch_api_funcs, imported
            df.to_sql('Games', engine, index=False, if_exists = 'append')

            print('timestamp: {}, length: {}'.format(datetime.datetime.now(), len(df)))
            time.sleep(sleep_time)

    # prepare to start thread
    engine = get_sql_engine()
    global stop_threads
    stop_threads = False

    # create and start thread
    t1 = threading.Thread(target=constant_query, args = (engine, max_size, sleep_time))
    t1.start()

    

    